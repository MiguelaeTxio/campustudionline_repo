# VARIABLES DE SESIÓN DE PROYECTOS
# Este archivo centraliza la configuración para todos los proyectos gestionados.
# El protocolo PISA lo utiliza para parametrizar el entorno de la sesión.

---

## CAMPUSTUDIONLINE

- **PROJECT_ID**: CampuStudiOnline
- **GEN_SERVER_ROOT**: /home/MiguelAeTxio/
- **APP_SERVER_ROOT**: PROJECTS/CampuStudiOnline/
- **SERVER_ROOT**: {GEN_SERVER_ROOT}{APP_SERVER_ROOT}
- **LOCAL_CLONE_PATH**: /home/claude/repo/CampuStudiOnline (workspace del modelo, flujo NFS — añadida 2026-07-24, ausente hasta ahora pese a estar referenciada por el flujo NFS)
- **CAMPUSTUDIONLINE_GITHUB_REPO**: https://github.com/MiguelaeTxio/campustudionline_repo.git
- **LOCAL_SWAP**: SWAP/
- **LOCAL_VENV**: "C:/Users/numme/Documents/AvanzadoPython/Proyecto Fin de Curso Python Avanzado/campustudionline/"
- **SERVER_VENV**: campus_pa_env_py3.10
- **SFTP_CONNECTION**: MiguelAeTxio@ssh.pythonanywhere.com:PROJECTS/CampuStudiOnline
- **DB_NAME**: MiguelAeTxio$campustudi
- **GENERAL_MASTER_DOC_PATH**: /home/MiguelAeTxio/SYSTEM_DOCS/GENERAL_MASTER_DOCUMENT.md
- **PROJECT_MASTER_DOC_PATH**: /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_MASTER_DOCUMENT.md
- **PROJECT_DIRECTORY_PATH**: /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/SESSION/CAMPUSTUDIONLINE_PROJECT_DIRECTORY.txt
- **PROJECT_ATTACHMENTS_PATH**: /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/
- **PROJECT_SESSION_DATA_PATH**: {SERVER_ROOT}DOCS/SESSION/
- **PROJECT_GEMINI_HISTORY**: {PROJECT_SESSION_DATA_PATH}GEMINI_SESSIONS_HISTORY.md
- **PROJECT_TEMP_HISTORY**: {PROJECT_SESSION_DATA_PATH}TEMP_SESSIONS_HISTORY.md
- **PROJECT_COMPLETED_SESSIONS_DIR**: {PROJECT_SESSION_DATA_PATH}COMPLETED/

### LOGS — Archivos no versionados del servidor

Fuente de verdad para el PVR de `com-file-request`. Rutas confirmadas
por Miguel Ángel el 2026-07-27 contra el panel de PythonAnywhere
(sección "Log files" de la web app y ficheros de Always-on Tasks).
Los logs rotan periódicamente; los históricos quedan en `/var/log/`
con sufijo de fecha. Mecanismo obligatorio de lectura: `tail -n {N}`
volcado a SWAP y descarga desde SWAP — nunca `get` directo del log.

- **LOG_WEB_ACCESS**: /var/log/www.campustudionline.com.access.log
- **LOG_WEB_ERROR**: /var/log/www.campustudionline.com.error.log
- **LOG_WEB_SERVER**: /var/log/www.campustudionline.com.server.log
- **LOG_ALWAYSON_PRIMARIO**: /var/log/alwayson-log-182748.log (Always-on Task Primario, cola `high_priority`, worker `hp_worker`)
- **LOG_ALWAYSON_PESADO**: /var/log/alwayson-log-209547.log (Always-on Task Pesado, cola `default`, worker `heavy_worker`)
