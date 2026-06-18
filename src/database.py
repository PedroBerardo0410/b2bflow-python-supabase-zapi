from supabase import create_client


def get_supabase_client(config: dict):
    return create_client(config["supabase_url"], config["supabase_key"])


def get_contacts(config: dict) -> list[dict]:
    client = get_supabase_client(config)

    response = (
        client.table(config["supabase_table"])
        .select("id,nome_contato,telefone,ativo")
        .eq("ativo", True)
        .limit(config["max_contacts"])
        .execute()
    )

    return response.data or []
