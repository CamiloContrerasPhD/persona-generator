from typing import Optional


SYSTEM_PROMPT = (
    "Eres un estratega de marketing senior. Genera buyer personas realistas, "+
    "diversas y útiles para planificación de marketing. Devuelve SIEMPRE JSON válido."
)


def build_user_prompt(product_description: str, target_market: str, num_personas: int = 4,
                     constraints: Optional[str] = None) -> str:
    hints = constraints or (
        "Incluye demográficos, psicográficos, motivaciones, frustraciones, señales conductuales; "+
        "segmentación multinivel por TIPO (elige hasta 3 entre Geográfica, Demográfica, Psicográfica, Conductual) "+
        "con etiquetas y criterios claros; "+
        "canales preferidos y tono; un brief narrativo claro (mensaje clave, propuesta de valor, "+
        "prueba social, objeciones y tratamiento, CTA y racional creativo) dirigido a quien ejecuta "+
        "la campaña; y un resumen ampliado que funcione como Canvas de Valor y Mapa de Empatía."
    )
    return (
        "Contexto: El estudiante describe un producto y su mercado objetivo.\n"
        f"Producto: {product_description}\n"
        f"Mercado objetivo: {target_market}\n"
        f"Cantidad de personas: {num_personas}\n"
        "Tarea: Genera buyer personas en formato JSON con la clave 'personas' (lista).\n"
        "Esquema sugerido para cada persona: {\n"
        "  'name': str, 'age_range': str, 'gender': str?, 'location': str?, 'occupation': str?,\n"
        "  'income_range': str?, 'education': str?, 'motivations': [str], 'frustrations': [str],\n"
        "  'preferred_channels': [str], 'messaging_tone': str?,\n"
        "  'psychographics': {'values': [str], 'interests': [str], 'lifestyle': [str]},\n"
        "  'behavioral_signals': [str],\n"
        "  'segmentation_levels': [\n"
        "     {'level': 'Geográfica'|'Demográfica'|'Psicográfica'|'Conductual', 'label': str, 'criteria': [str]}\n"
        "     // Máximo 3 entradas combinando tipos para hallar los mejores targets\n"
        "  ],\n"
        "  'creative_brief': str,\n"
        "  'value_canvas': { 'customer_jobs': [str]?, 'pains': [str]?, 'gains': [str]?,\n"
        "                    'value_props': [str]?, 'pain_relievers': [str]?, 'gain_creators': [str]? },\n"
        "  'empathy_map': { 'think': [str]?, 'feel': [str]?, 'see': [str]?, 'say_do': [str]?, 'pains': [str]?, 'gains': [str]? },\n"
        "  'summary': str?\n"
        "}\n"
        f"Criterios: {hints}\n"
        "Responde SOLO con JSON."
    )

