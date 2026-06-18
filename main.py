import logging
import sys

from src.config import get_config, validate_config
from src.database import get_supabase_client, get_active_contacts
from src.zapi import build_message, send_whatsapp_message, send_message_dry_run


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("=" * 50)
    logger.info("Iniciando b2bflow - Envio de mensagens via Z-API")
    logger.info("=" * 50)

    config = get_config()
    errors = validate_config(config)

    if errors:
        for error in errors:
            logger.error(f"Configuracao invalida: {error}")
        logger.error("Configure o .env corretamente e tente novamente.")
        sys.exit(1)

    mode = "DRY_RUN (simulacao)" if config["dry_run"] else "ENVIO REAL"
    logger.info(f"Modo: {mode}")
    logger.info(f"Maximo de contatos: {config['max_contacts']}")

    client = get_supabase_client(config["supabase_url"], config["supabase_key"])
    contacts = get_active_contacts(client, config["supabase_table"], config["max_contacts"])

    if not contacts:
        logger.warning("Nenhum contato ativo encontrado. Encerrando.")
        sys.exit(0)

    success_count = 0
    error_count = 0

    for contact in contacts:
        nome = contact.get("nome_contato", "")
        telefone = contact.get("telefone", "")
        contact_id = contact.get("id", "")

        if not nome or not telefone:
            logger.warning(f"Contato ID {contact_id} com dados incompletos. Pulando.")
            error_count += 1
            continue

        message = build_message(nome)
        logger.info(f"Processando contato: {nome} ({telefone})")

        try:
            if config["dry_run"]:
                send_message_dry_run(telefone, message)
            else:
                send_whatsapp_message(
                    instance_id=config["zapi_instance_id"],
                    instance_token=config["zapi_instance_token"],
                    client_token=config["zapi_client_token"],
                    phone=telefone,
                    message=message,
                )
            success_count += 1
        except Exception as e:
            logger.error(f"Falha ao enviar para {nome} ({telefone}): {e}")
            error_count += 1

    logger.info("-" * 50)
    logger.info(f"Resumo: {success_count} enviado(s), {error_count} falha(s)")
    logger.info("Processo finalizado!")


if __name__ == "__main__":
    main()
