# Generador de Personas con IA (Streamlit)

Aplicación web educativa para generar 3–5 buyer personas a partir de la descripción de un producto y su mercado objetivo. Usa un LLM (OpenAI o Hugging Face Inference) y muestra los perfiles en una interfaz simple con Streamlit.

## Requisitos

- Python 3.9+
- Cuenta y API Key de uno de:
  - OpenAI (`OPENAI_API_KEY`)
  - Hugging Face Inference (`HF_API_TOKEN` + nombre de modelo de texto)

## Instalación

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env  # en Windows
```

Edita `.env` y define tu proveedor:

```env
# Uno de: openai | huggingface
LLM_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Hugging Face
HF_API_TOKEN=hf_...
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

## Ejecutar

```bash
streamlit run app.py
```

Abre el navegador en `http://localhost:8501`.

## Notas pedagógicas

- Compara y critica las personas generadas.
- Ajusta el prompt (archivo `prompt.py`) para explorar distintos enfoques.
- Cambia el número de perfiles y el tono para observar variaciones.

## Estructura

```
persona-generator/
├─ app.py
├─ llm_client.py
├─ prompt.py
├─ persona_schema.py
├─ utils.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

## Privacidad
No se almacenan entradas ni salidas. Las claves se leen desde variables de entorno. Revisa las políticas de tu proveedor de IA.

