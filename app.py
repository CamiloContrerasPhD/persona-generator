import os
import json
import streamlit as st

from utils import load_env
from llm_client import LLMClient
from persona_schema import PersonaBundle


load_env()
st.set_page_config(page_title="Generador de Personas con IA", page_icon="🧠", layout="wide")

st.title("🧠 Generador de Personas con IA")
st.caption("Ingresa tu producto y mercado objetivo. Obtén buyer personas en segundos.")

with st.sidebar:
    st.header("Configuración")
    provider = os.getenv("LLM_PROVIDER", "openai")
    st.write(f"Proveedor: `{provider}`")
    default_num = 4
    num_personas = st.slider("Cantidad de personas", min_value=3, max_value=5, value=default_num)

product = st.text_area("Describe tu producto", height=120, placeholder="Ej.: App móvil de hábitos para profesionales ocupados...")
target = st.text_area("Describe tu mercado objetivo", height=100, placeholder="Ej.: Hombres y mujeres 25-40 en ciudades grandes que...")

col1, col2 = st.columns([1, 2])
with col1:
    generate = st.button("Generar personas")

placeholder = st.container()

# ===== Helpers UX =====
def _mk_kv_table(rows):
    # rows: list of (label, value)
    clean = [(k, v) for k, v in rows if v not in (None, "", [])]
    if not clean:
        return ""
    header = "| Campo | Detalle |\n|---|---|"
    body = "\n".join([f"| {k} | {v} |" for k, v in clean])
    return f"{header}\n{body}"


def _mk_bullets(items, icon="•"):
    if not items:
        return ""
    return "\n".join([f"- {icon} {it}" for it in items])


def _mk_segmentation_table(levels):
    if not levels:
        return ""
    header = "| Nivel | Etiqueta | Criterios |\n|---|---|---|"
    rows = []
    for lvl in levels:
        if not isinstance(lvl, dict):
            continue
        level_name = lvl.get("level", "")
        label = lvl.get("label", "")
        criteria = lvl.get("criteria", [])
        crit = ", ".join(criteria) if isinstance(criteria, list) else str(criteria or "")
        rows.append(f"| {level_name} | {label} | {crit} |")
    if not rows:
        return ""
    return f"{header}\n" + "\n".join(rows)


if generate:
    if not product.strip() or not target.strip():
        st.warning("Por favor completa producto y mercado objetivo.")
    else:
        with st.spinner("Generando personas..."):
            try:
                client = LLMClient()
                bundle: PersonaBundle = client.generate_personas(product, target, num_personas)
            except Exception as e:
                st.error(f"Error al generar: {e}")
                st.stop()

        with placeholder:
            if not bundle.personas:
                st.info("No se recibieron personas. Ajusta el prompt o intenta de nuevo.")
            else:
                for idx, p in enumerate(bundle.personas, start=1):
                    with st.expander(f"Persona {idx}: {p.name}", expanded=(idx == 1)):
                        cols = st.columns(3)
                        with cols[0]:
                            st.markdown("### 👤 Demográficos")
                            demo_table = _mk_kv_table([
                                ("Edad", p.age_range),
                                ("Género", p.gender),
                                ("Ubicación", p.location),
                                ("Ocupación", p.occupation),
                                ("Ingresos", p.income_range),
                                ("Educación", p.education),
                            ])
                            if demo_table:
                                st.markdown(demo_table)
                            if getattr(p, "behavioral_signals", None):
                                st.markdown("### 🧭 Señales conductuales")
                                st.markdown(_mk_bullets(getattr(p, "behavioral_signals"), icon="🧩"))
                        with cols[1]:
                            st.markdown("### 🧠 Psicográficos")
                            if p.psychographics.values:
                                st.markdown("**Valores**")
                                st.markdown(_mk_bullets(p.psychographics.values, icon="💎"))
                            if p.psychographics.interests:
                                st.markdown("**Intereses**")
                                st.markdown(_mk_bullets(p.psychographics.interests, icon="🎯"))
                            if p.psychographics.lifestyle:
                                st.markdown("**Estilo de vida**")
                                st.markdown(_mk_bullets(p.psychographics.lifestyle, icon="🌱"))
                            st.markdown("### 🚀 Motivaciones")
                            if p.motivations:
                                st.markdown(_mk_bullets(p.motivations, icon="⚡"))
                            st.markdown("### 🛑 Frustraciones")
                            if p.frustrations:
                                st.markdown(_mk_bullets(p.frustrations, icon="❗"))
                        with cols[2]:
                            st.markdown("### 📣 Canales y Mensaje")
                            if p.preferred_channels:
                                st.markdown("**Canales preferidos**")
                                st.markdown(_mk_bullets(p.preferred_channels, icon="📡"))
                            if p.messaging_tone:
                                st.markdown(f"**Tono recomendado**: ✨ {p.messaging_tone}")
                            if getattr(p, "segmentation_levels", None):
                                st.markdown("**🔎 Segmentación multinivel**")
                                seg_table = _mk_segmentation_table(getattr(p, "segmentation_levels"))
                                if seg_table:
                                    st.markdown(seg_table)
                            if getattr(p, "creative_brief", None):
                                st.markdown("**📝 Brief narrativo**")
                                st.info(getattr(p, "creative_brief"))
                        # Narrative and frameworks
                        st.markdown("### 🧩 Canvas de Valor")
                        vc = getattr(p, "value_canvas", None)
                        if isinstance(vc, dict) and any(vc.get(k) for k in ["customer_jobs", "pains", "gains", "value_props", "pain_relievers", "gain_creators"]):
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                if vc.get("customer_jobs"):
                                    st.markdown("**👔 Customer jobs**")
                                    st.markdown(_mk_bullets(vc.get("customer_jobs"), icon="🧰"))
                                if vc.get("value_props"):
                                    st.markdown("**💡 Value props**")
                                    st.markdown(_mk_bullets(vc.get("value_props"), icon="💡"))
                            with c2:
                                if vc.get("pains"):
                                    st.markdown("**😣 Pains**")
                                    st.markdown(_mk_bullets(vc.get("pains"), icon="❌"))
                                if vc.get("pain_relievers"):
                                    st.markdown("**🩹 Pain relievers**")
                                    st.markdown(_mk_bullets(vc.get("pain_relievers"), icon="🩹"))
                            with c3:
                                if vc.get("gains"):
                                    st.markdown("**📈 Gains**")
                                    st.markdown(_mk_bullets(vc.get("gains"), icon="✅"))
                                if vc.get("gain_creators"):
                                    st.markdown("**🚀 Gain creators**")
                                    st.markdown(_mk_bullets(vc.get("gain_creators"), icon="🚀"))
                        em = getattr(p, "empathy_map", None)
                        if isinstance(em, dict) and any(em.get(k) for k in ["think", "feel", "see", "say_do", "pains", "gains"]):
                            st.markdown("### 🤝 Mapa de empatía")
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                if em.get("think"):
                                    st.markdown("**🧠 Piensa**")
                                    st.markdown(_mk_bullets(em.get("think"), icon="🧠"))
                                if em.get("feel"):
                                    st.markdown("**💓 Siente**")
                                    st.markdown(_mk_bullets(em.get("feel"), icon="💓"))
                            with c2:
                                if em.get("see"):
                                    st.markdown("**👀 Ve**")
                                    st.markdown(_mk_bullets(em.get("see"), icon="👀"))
                                if em.get("say_do"):
                                    st.markdown("**🗣️ Dice/Hace**")
                                    st.markdown(_mk_bullets(em.get("say_do"), icon="🗣️"))
                            with c3:
                                if em.get("pains"):
                                    st.markdown("**⚠️ Dolores**")
                                    st.markdown(_mk_bullets(em.get("pains"), icon="⚠️"))
                                if em.get("gains"):
                                    st.markdown("**🏆 Ganancias**")
                                    st.markdown(_mk_bullets(em.get("gains"), icon="🏆"))
                        if p.summary:
                            st.markdown("### 🧾 Resumen ampliado")
                            st.success(p.summary)
                st.divider()
                with st.expander("Ver respuesta JSON (opcional)"):
                    st.code(json.dumps(bundle.model_dump(), ensure_ascii=False, indent=2), language="json")

