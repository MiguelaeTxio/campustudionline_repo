# Migración de reparación escrita a mano según com-migrations sección 1
# y sección 3 (reparación de tablas contra el estado real de la BD).
# Django 5.0.7 / MySQL 8.0.42 InnoDB.
#
# CONTEXTO — auditado en producción el 2026-07-29:
#
# Las migraciones orchestrator 0001 y 0002 figuran aplicadas el
# 2025-11-18 con 4 milisegundos de diferencia entre ambas. Crear una
# tabla de veinticuatro columnas y añadirle después tres constraints no
# ocurre en 4 ms: es la marca de un `migrate --fake`. Las tablas
# existían por otra vía y nunca recibieron ni sus claves ajenas ni las
# constraints declaradas en Meta. Las migraciones 0003 a 0006, aplicadas
# en diciembre con días de separación, sí se ejecutaron de verdad — por
# eso `last_error_api_key_id`, añadida en 0003, es la única clave ajena
# que sí existía en `orchestrator_pendingcontenttask`.
#
# La auditoría de la base devolvió 6 claves ajenas y 3 constraints
# ausentes, todas dentro de orchestrator. Ninguna tabla ausente, ningún
# índice de Meta ausente, resto de la base íntegro.
#
# DATOS VERIFICADOS ANTES DE ESCRIBIR ESTA MIGRACIÓN:
#   - 0 tareas activas y 0 duplicados: los índices únicos no pueden
#     fallar al crearse.
#   - 0 filas violan el check constraint.
#   - 5 de las 6 claves ajenas tienen integridad referencial perfecta.
#   - `generatedcontentchunk.task_id` tiene 13 huérfanos sobre 2703.
#     El modelo declara on_delete=CASCADE, de modo que esas filas
#     deberían haber desaparecido con su tarea; sobreviven solo porque
#     la clave ajena nunca existió. Se respaldan a un archivo JSON antes
#     de borrarlas.

import json
import os
from datetime import datetime

from django.db import migrations, models
from django.db.models import Case, F, Q, Value, When

FK_TARGETS = [
    ("ContentRequest", "subject"),
    ("PendingContentTask", "subject"),
    ("PendingContentTask", "assigned_to"),
    ("PendingContentTask", "content_material"),
    ("GeneratedContentChunk", "task"),
    ("FreeContentRequest", "requester"),
]

TASK_TYPE_CHECK = models.CheckConstraint(
    check=models.Q(
        models.Q(
            ("subject__isnull", False),
            ("course_title__exact", ""),
            ("prompt_text__exact", ""),
        ),
        models.Q(
            ("subject__isnull", True),
            models.Q(("course_title__exact", ""), _negated=True),
            models.Q(("prompt_text__exact", ""), _negated=True),
        ),
        _connector="OR",
    ),
    name="task_type_is_exclusive",
)


def _backup_directory():
    """
    Return a writable directory for the orphan-row backup.
    ---
    Devuelve un directorio donde volcar el respaldo de las filas
    huérfanas. Prefiere SWAP, que es el directorio de intercambio
    establecido del proyecto, y cae a /tmp si no puede escribir.
    """
    candidate = os.path.join(os.path.expanduser("~"), "SWAP")
    try:
        os.makedirs(candidate, exist_ok=True)
        probe = os.path.join(candidate, ".write_probe")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("")
        os.remove(probe)
        return candidate
    except OSError:
        return "/tmp"


def backup_and_delete_orphan_chunks(apps, schema_editor):
    """
    Back up and remove content chunks whose parent task no longer exists.
    ---
    Respalda y elimina los fragmentos de contenido cuya tarea padre ya
    no existe. Son inalcanzables por la aplicación y su __str__ revienta
    al resolver self.task.id. El respaldo se escribe antes del borrado y
    su ruta se imprime en el log del despliegue.
    """
    model = apps.get_model("orchestrator", "GeneratedContentChunk")
    parent = apps.get_model("orchestrator", "PendingContentTask")
    table = model._meta.db_table
    parent_table = parent._meta.db_table
    orphan_sql = (
        " FROM " + table + " WHERE task_id NOT IN "
        "(SELECT id FROM " + parent_table + ")"
    )
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*)" + orphan_sql)
        total = cursor.fetchone()[0]
        if not total:
            print("  [reparacion] sin fragmentos huerfanos que borrar")
            return
        cursor.execute("SELECT *" + orphan_sql)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(
            _backup_directory(),
            "orphan_content_chunks_" + stamp + ".json",
        )
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(rows, handle, ensure_ascii=False, default=str, indent=2)
        print(
            "  [reparacion] " + str(total)
            + " fragmentos huerfanos respaldados en " + path
        )
        cursor.execute("DELETE" + orphan_sql)
        print("  [reparacion] fragmentos huerfanos eliminados")


def noop_reverse(apps, schema_editor):
    """
    Irreversible step, kept explicit.
    ---
    Paso irreversible. El reverso no recrea las filas huérfanas: si
    hicieran falta, están en el archivo JSON del respaldo.
    """
    return None


def _existing_fk_columns(schema_editor):
    """
    Return the (table, column) pairs that already carry a foreign key.
    ---
    Devuelve los pares (tabla, columna) que ya tienen clave ajena. MySQL
    no revierte DDL, así que la reparación tiene que poder repetirse sin
    romper.
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT TABLE_NAME, COLUMN_NAME "
            "FROM information_schema.KEY_COLUMN_USAGE "
            "WHERE CONSTRAINT_SCHEMA = DATABASE() "
            "AND REFERENCED_TABLE_NAME IS NOT NULL"
        )
        return {(row[0], row[1]) for row in cursor.fetchall()}


def add_missing_foreign_keys(apps, schema_editor):
    """
    Create the foreign keys that the faked migrations never created.
    ---
    Crea las claves ajenas que las migraciones faked nunca crearon. Usa
    el generador de SQL del propio schema editor en lugar de un ALTER
    TABLE escrito a mano, para que el nombre de cada constraint salga
    idéntico al que Django habría puesto. MySQL crea además, por su
    cuenta, el índice que le falta a la columna referenciante.
    """
    if schema_editor.connection.vendor != "mysql":
        return
    existing = _existing_fk_columns(schema_editor)
    for model_name, field_name in FK_TARGETS:
        model = apps.get_model("orchestrator", model_name)
        field = model._meta.get_field(field_name)
        if (model._meta.db_table, field.column) in existing:
            continue
        schema_editor.execute(
            schema_editor._create_fk_sql(
                model, field, "_fk_%(to_table)s_%(to_column)s"
            )
        )
        print(
            "  [reparacion] clave ajena creada en "
            + model._meta.db_table + "." + field.column
        )


def drop_repaired_foreign_keys(apps, schema_editor):
    """
    Drop the foreign keys created by this migration.
    ---
    Retira las claves ajenas creadas por esta migración.
    """
    if schema_editor.connection.vendor != "mysql":
        return
    for model_name, field_name in FK_TARGETS:
        model = apps.get_model("orchestrator", model_name)
        field = model._meta.get_field(field_name)
        for name in schema_editor._constraint_names(
            model, [field.column], foreign_key=True
        ):
            schema_editor.execute(schema_editor._delete_fk_sql(model, name))


def _constraint_exists_sql(schema_editor, table_name, constraint_name):
    """
    Look the constraint up in information_schema by name.
    ---
    Busca la constraint por nombre en information_schema.
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS "
            "WHERE CONSTRAINT_SCHEMA = DATABASE() "
            "AND TABLE_NAME = %s AND CONSTRAINT_NAME = %s",
            [table_name, constraint_name],
        )
        return cursor.fetchone()[0] > 0


def add_missing_check_constraint(apps, schema_editor):
    """
    Recreate the check constraint declared in 0002 but never applied.
    ---
    Repone el check constraint que 0002 declaró y que nunca llegó a la
    base de datos. Verificado antes: 0 filas lo violan.
    """
    if schema_editor.connection.vendor != "mysql":
        return
    model = apps.get_model("orchestrator", "PendingContentTask")
    if _constraint_exists_sql(
        schema_editor, model._meta.db_table, TASK_TYPE_CHECK.name
    ):
        return
    schema_editor.add_constraint(model, TASK_TYPE_CHECK)
    print("  [reparacion] check constraint task_type_is_exclusive repuesto")


def drop_repaired_check_constraint(apps, schema_editor):
    """
    Drop the check constraint restored by this migration.
    ---
    Retira el check constraint repuesto por esta migración.
    """
    if schema_editor.connection.vendor != "mysql":
        return
    model = apps.get_model("orchestrator", "PendingContentTask")
    if not _constraint_exists_sql(
        schema_editor, model._meta.db_table, TASK_TYPE_CHECK.name
    ):
        return
    schema_editor.remove_constraint(model, TASK_TYPE_CHECK)


class Migration(migrations.Migration):

    dependencies = [
        ("orchestrator", "0006_automationsettings_is_mass_generation_enabled"),
    ]

    operations = [
        migrations.RunPython(
            backup_and_delete_orphan_chunks,
            noop_reverse,
        ),
        migrations.RunPython(
            add_missing_foreign_keys,
            drop_repaired_foreign_keys,
        ),
        migrations.RunPython(
            add_missing_check_constraint,
            drop_repaired_check_constraint,
        ),
        migrations.RemoveConstraint(
            model_name="pendingcontenttask",
            name="unique_active_academic_task_per_subject",
        ),
        migrations.RemoveConstraint(
            model_name="pendingcontenttask",
            name="unique_active_free_task_per_title",
        ),
        migrations.AddField(
            model_name="pendingcontenttask",
            name="active_subject_key",
            field=models.GeneratedField(
                db_persist=True,
                expression=Case(
                    When(
                        Q(
                            (
                                "status__in",
                                ["COMPLETED", "FAILED", "FAILED_FATAL"],
                            ),
                            _negated=True,
                        ),
                        then=F("subject"),
                    ),
                    default=Value(None),
                    output_field=models.CharField(max_length=32),
                ),
                output_field=models.CharField(max_length=32, null=True),
                verbose_name="Clave de Tarea Académica Activa",
            ),
        ),
        migrations.AddField(
            model_name="pendingcontenttask",
            name="active_free_title_key",
            field=models.GeneratedField(
                db_persist=True,
                expression=Case(
                    When(
                        Q(
                            Q(
                                (
                                    "status__in",
                                    ["COMPLETED", "FAILED", "FAILED_FATAL"],
                                ),
                                _negated=True,
                            ),
                            ("subject__isnull", True),
                        ),
                        then=F("course_title"),
                    ),
                    default=Value(None),
                    output_field=models.CharField(max_length=255),
                ),
                output_field=models.CharField(max_length=255, null=True),
                verbose_name="Clave de Curso Libre Activo",
            ),
        ),
        migrations.AddConstraint(
            model_name="pendingcontenttask",
            constraint=models.UniqueConstraint(
                fields=("active_subject_key",),
                name="unique_active_academic_task_per_subject",
            ),
        ),
        migrations.AddConstraint(
            model_name="pendingcontenttask",
            constraint=models.UniqueConstraint(
                fields=("active_free_title_key",),
                name="unique_active_free_task_per_title",
            ),
        ),
    ]
