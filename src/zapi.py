import requests


def send_text_message(config: dict, phone: str, message: str):
    url = (
        f"https://api.z-api.io/instances/"
        f"{config['zapi_instance_id']}/token/"
        f"{config['zapi_instance_token']}/send-text"
    )

    headers = {
        "Client-Token": config["zapi_client_token"],
        "Content-Type": "application/json",
    }

    payload = {
        "phone": phone,
        "message": message,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)

    try:
        response_data = response.json()
    except ValueError:
        response_data = response.text

    if response.status_code >= 400:
        raise RuntimeError(f"Erro na Z-API: {response.status_code} - {response_data}")

    return response_data
