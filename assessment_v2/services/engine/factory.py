# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/factory.py
from .strategies.languages import LanguagesStrategy

class ExamFactory:
    """
    Factoría para instanciar la estrategia de examen adecuada según el arquetipo.
    Alineado con V06DOC_ARCHETYPES y V06DOC_LOGIC_MAPPING.
    """
    ARCH_LANG = 'ARCH_LANG'
    ARCH_HEALTH = 'ARCH_HEALTH'
    ARCH_TECH = 'ARCH_TECH'
    ARCH_SOC = 'ARCH_SOC'
    ARCH_HUM = 'ARCH_HUM'
    ARCH_GEN = 'ARCH_GEN'

    @staticmethod
    def get_strategy(archetype_id, **kwargs):
        """
        Retorna una instancia de la estrategia correspondiente.
        """
        if archetype_id == ExamFactory.ARCH_LANG:
            return LanguagesStrategy(**kwargs)
        
        # Por ahora, el resto de arquetipos usan la lógica genérica 
        # o lanzan error hasta que sus estrategias específicas sean creadas.
        # Según Roadmap Hito 6, estamos consolidando la base primero.
        
        if archetype_id in [ExamFactory.ARCH_HEALTH, ExamFactory.ARCH_TECH, 
                            ExamFactory.ARCH_SOC, ExamFactory.ARCH_HUM, ExamFactory.ARCH_GEN]:
            # Fallback a LanguagesStrategy temporalmente o lanzar error de implementación
            # Para cumplir con el flujo, permitimos el flujo pero notificamos.
            return LanguagesStrategy(**kwargs) 
            
        raise ValueError(f"Arquetipo {archetype_id} no reconocido o no implementado.")
