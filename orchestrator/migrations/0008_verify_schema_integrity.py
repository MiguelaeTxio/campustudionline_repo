# Migración de verificación. No modifica nada: audita el esquema real
# contra lo que los modelos declaran y aborta el despliegue si algo
# falta.
#
# Motivo de existir: la incidencia que repara 0007 no fue un error
# ruidoso, fue una omisión silenciosa. Django marcó como aplicadas unas
# migraciones que nunca crearon sus claves ajenas ni sus constraints, y
# eso pasó nueve meses sin que nadie lo notara. Esta migración convierte
# esa clase de fallo en un despliegue rojo.
#
# Es segura de repetir: no ejecuta DDL. Si falla, 0007 ya quedó
# registrada como aplicada, de modo que el reintento solo repite esta
# comprobación.

from django.apps import apps as global_apps
from django.db import migrations


def _table_names(connection, cursor):
    """
    Return every base table present in the schema.
    ---
    Devuelve todas las tablas existentes en el esquema.
    """
    return {
        info.name
        for info in connection.introspection.get_table_list(cursor)
        if info.type == "t"
    }


def audit_schema_matches_models(apps, schema_editor):
    """
    Fail loudly if any declared database object is missing.
    ---
    Aborta si falta cualquier objeto declarado por los modelos: claves
    ajenas, constraints de Meta, índices de Meta o unique_together. Se
    audita la base entera, no solo la app reparada, porque una omisión
    silenciosa en cualquier otra app sería el mismo defecto.
    """
    connection = schema_editor.connection
    if connection.vendor != "mysql":
        return
    problems = []
    with connection.cursor() as cursor:
        existing_tables = _table_names(connection, cursor)
        for model in global_apps.get_models():
            meta = model._meta
            if meta.proxy or not meta.managed:
                continue
            table = meta.db_table
            if table not in existing_tables:
                problems.append("tabla ausente: " + table)
                continue
            found = connection.introspection.get_constraints(cursor, table)
            fk_columns = set()
            unique_column_sets = []
            names = set(found)
            for info in found.values():
                columns = tuple(info.get("columns") or ())
                if info.get("foreign_key"):
                    fk_columns.update(columns)
                if info.get("unique"):
                    unique_column_sets.append(frozenset(columns))
            for field in meta.local_fields:
                if not (field.is_relation and field.db_constraint):
                    continue
                if field.column not in fk_columns:
                    problems.append(
                        "clave ajena ausente: " + table + "." + field.column
                    )
            for constraint in meta.constraints:
                if constraint.name not in names:
                    problems.append(
                        "constraint ausente: " + table + " -> "
                        + constraint.name
                    )
            for index in meta.indexes:
                if index.name not in names:
                    problems.append(
                        "indice ausente: " + table + " -> " + index.name
                    )
            for group in meta.unique_together:
                columns = frozenset(
                    meta.get_field(name).column for name in group
                )
                if columns not in unique_column_sets:
                    problems.append(
                        "unique_together ausente: " + table + " -> "
                        + ", ".join(sorted(columns))
                    )
    if problems:
        raise RuntimeError(
            "El esquema real no coincide con los modelos. "
            + str(len(problems))
            + " objeto(s) declarado(s) no existen en la base de datos:\n  "
            + "\n  ".join(problems)
        )
    print("  [auditoria] esquema coherente con los modelos")


class Migration(migrations.Migration):

    dependencies = [
        ("orchestrator", "0007_repair_faked_schema_and_active_task_keys"),
        ("media_library", "0002_seed_catalogs_and_licenses"),
    ]

    operations = [
        migrations.RunPython(
            audit_schema_matches_models,
            migrations.RunPython.noop,
        ),
    ]
