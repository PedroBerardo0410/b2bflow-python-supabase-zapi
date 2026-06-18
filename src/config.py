import os
from dotenv import load_dotenv


def _str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes", "y", "sim", "s")


def get_config() -> dict:
    load_dotenv()

    try:
        max_contacts = int(os.getenv("MAX_CONTACTS", "3"))
    except ValueError:
        max_contacts = 3

    max_contacts = max(1, min(max_contacts, 3))

    return {
        "supabase_url": os.getenv("SUPABASE_URL", "").strip(),
        "supabase_key": os.getenv("SUPABASE_KEY", "").strip(),
        "supabase_table": os.getenv("SUPABASE_TABLE", "contatos").strip(),
        "zapi_instance_id": os.getenv("ZAPI_INSTANCE_ID", "").strip(),
        "zapi_instance_token": os.getenv("ZAPI_INSTANCE_TOKEN", "").strip(),
        "zapi_client_token": os.getenv("ZAPI_CLIENT_TOKEN", "").strip(),
        "dry_run": _str_to_bool(os.getenv("DRY_RUN", "true")),
        "max_contacts": max_contacts,
    }


def validate_config(config: dict) -> None:
    errors = []

    if not config["supabase_url"]:
        errors.append("SUPABASE_URL não foi configurado no .env")

    if not config["supabase_key"]:
        errors.append("SUPABASE_KEY não foi configurado no .env")

    if not config["supabase_table"]:
        errors.append("SUPABASE_TABLE não foi configurado no .env")

    if not config["dry_run"]:
        if not config["zapi_instance_id"]:
            errors.append("ZAPI_INSTANCE_ID não foi configurado no .env")

        if not config["zapi_instance_token"]:
            errors.append("ZAPI_INSTANCE_TOKEN não foi configurado no .env")

        if not config["zapi_client_token"]:
            errors.append("ZAPI_CLIENT_TOKEN não foi configurado no .env")

    if errors:
        raise ValueError("\n".join(errors))
