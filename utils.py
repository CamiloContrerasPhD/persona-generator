import os
from dotenv import load_dotenv


def load_env() -> None:
    # Load from local .env if present (no error if missing)
    load_dotenv(override=False)
    # Normalize provider casing
    if os.getenv("LLM_PROVIDER"):
        os.environ["LLM_PROVIDER"] = os.getenv("LLM_PROVIDER").strip().lower()

