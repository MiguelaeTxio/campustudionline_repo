# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_STRUCTURE.md
# V06DOC_STRUCTURE - ARQUITECTURA DE SOFTWARE SEGREGADA Y COMERCIAL (V1.0)

## 1. DESLINDE DE COMPETENCIAS
*   ORCHESTRATOR: Gestiona tráfico, colas Celery, control de costes (API) y usuarios.
*   ASSESSMENT_V2: Contiene la lógica pedagógica, el motor de calificación y la UI.

## 2. ESTRUCTURA DE DIRECTORIOS (assessent_v2)
assessment_v2/
├── models/
│   ├── main.py       # Exam, Submissions
│   ├── tracking.py   # TokenUsage, CostLogs
│   └── plans.py      # SubscriptionPlan, UserSubscription
├── admin.py
├── services/
│   ├── badges.py     # Lógica de indicadores visuales
│   ├── quotas.py     # Validador de límites (lee de 'plans.py')
│   └── engine/
│       ├── factory.py
│       └── strategies/
│           └── base.py, languages.py, ...
├── context_processors.py
└── ...

## 3. PROTOCOLO DE ORQUESTACIÓN
1.  Petición del usuario.
2.  `quotas.py` valida contra el `SubscriptionPlan` del usuario.
3.  `orchestrator` encola la tarea.
4.  `engine` genera el "Exam Contract" JSON.
5.  Frontend renderiza los Widgets.
6.  `engine` califica la entrega con la Estrategia específica.
7.  `tracking.py` registra el consumo de tokens.
8.  `badges.py` actualiza el estado visual del usuario.

## 4. PROTOCOLOS OPERATIVOS ADICIONALES
*   BADGES: Sistema de señalización global (NavBar/SideBar) y local (lista de copias) para los estados: 'Generando', 'Pendiente', 'Corrigiendo', 'Calificado'.
*   CUOTAS: Lógica de límites diarios/semanales desacoplada en `models/plans.py` para futura integración Premium.
*   API KEY DE PAGO: Mecanismo de bypass para usar una clave específica de pago y registro detallado de consumo en `models/tracking.py`.
