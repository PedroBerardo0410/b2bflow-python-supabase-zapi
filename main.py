import logging
import sys

from src.config import get_config, validate_config
from src.database import get_contacts
from src.zapi import send_text_message


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def build_message(nome_contato: str) -> str:
    return f"Olá, {nome_contato} tudo bem com você?"


def main() -> None:
    try:
        config = get_config()
        validate_config(config)

        if config["dry_run"]:
            logging.info("Modo de execução: DRY_RUN, apenas simulação.")
        else:
            logging.info("Modo de execução: ENVIO REAL via Z-API.")

        logging.info("Buscando contatos ativos na tabela '%s'...", config["supabase_table"])

        contacts = get_contacts(config)

        if not contacts:
            logging.warning("Nenhum contato ativo encontrado no Supabase.")
            return

        logging.info("%s contato(s) encontrado(s).", len(contacts))

        for contact in contacts:
            nome_contato = str(contact.get("nome_contato", "")).strip()
            telefone = str(contact.get("telefone", "")).strip()

            if not nome_contato or not telefone:
                logging.warning("Contato ignorado por falta de nome ou telefone: %s", contact)
                continue

            message = build_message(nome_contato)

            if config["dry_run"]:
                logging.info("[DRY_RUN] Simulando envio para %s: %s", telefone, message)
            else:
                response = send_text_message(config, telefone, message)
                logging.info("Resposta da Z-API para %s: %s", telefone, response)

    except Exception as error:
        logging.error("Erro ao executar o projeto: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
