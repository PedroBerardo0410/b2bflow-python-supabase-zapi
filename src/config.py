import os
from dotenv import load_dotenv

load_dotenv()


def get_config():
      """Carrega e valida as variaveis de ambiente."""
      config = {
          # Supabase
          "supabase_url": os.getenv("SUPABASE_URL", ""),
          "supabase_key": os.getenv("SUPABASE_KEY", ""),
          "supabase_table": os.getenv("SUPABASE_TABLE", "contatos"),
          # Z-API
          "zapi_instance_id": os.getenv("ZAPI_INSTANCE_ID", ""),
          "zapi_instance_token": os.getenv("ZAPI_INSTANCE_TOKEN", ""),
          "zapi_client_token": os.getenv("ZAPI_CLIENT_TOKEN", ""),
          # Configuracoes
          "dry_run": os.getenv("DRY_RUN", "true").lower() == "true",
          "max_contacts": int(os.getenv("MAX_CONTACTS", "3")),
      }
      return config


def validate_config(config):
      """Valida se as variaveis obrigatorias estao presentes."""
      errors = []

    if not config["supabase_url"]:
              errors.append("SUPABASE_URL nao definido")
          if not config["supabase_key"]:
                    errors.append("SUPABASE_KEY nao definido")

    if not config["dry_run"]:
              if not config["zapi_instance_id"]:
                            errors.append("ZAPI_INSTANCE_ID nao definido")
                        if not config["zapi_instance_token"]:
                                      errors.append("ZAPI_INSTANCE_TOKEN nao definido")
                                  if not config["zapi_client_token"]:
                                                errors.append("ZAPI_CLIENT_TOKEN nao definido")

    return errors
