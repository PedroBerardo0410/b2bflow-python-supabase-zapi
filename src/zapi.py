import logging
import requests

logger = logging.getLogger(__name__)

ZAPI_BASE_URL = "https://api.z-api.io/instances/{instance_id}/token/{instance_token}"


def build_message(nome_contato: str) -> str:
      """Formata a mensagem personalizada com o nome do contato."""
      return f"Ola, {nome_contato} tudo bem com voce?"


def send_whatsapp_message(
      instance_id: str,
      instance_token: str,
      client_token: str,
      phone: str,
      message: str,
) -> dict:
      """Envia mensagem WhatsApp via Z-API."""
      url = (
          ZAPI_BASE_URL.format(
              instance_id=instance_id,
              instance_token=instance_token,
          )
          + "/send-text"
      )

    headers = {
              "Content-Type": "application/json",
              "Client-Token": client_token,
    }

    payload = {
              "phone": phone,
              "message": message,
    }

    try:
              response = requests.post(url, json=payload, headers=headers, timeout=30)
              response.raise_for_status()
              logger.info(f"Mensagem enviada para {phone} com sucesso")
              return response.json()
except requests.exceptions.HTTPError as e:
          logger.error(f"Erro HTTP ao enviar para {phone}: {e} - Resposta: {e.response.text}")
          raise
except requests.exceptions.RequestException as e:
          logger.error(f"Erro de conexao ao enviar para {phone}: {e}")
          raise


def send_message_dry_run(phone: str, message: str) -> None:
      """Simula envio de mensagem (modo DRY_RUN)."""
      logger.info(f"[DRY_RUN] Simulando envio para {phone}: '{message}'")
