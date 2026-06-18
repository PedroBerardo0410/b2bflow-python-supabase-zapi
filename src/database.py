import logging
  from supabase import create_client, Client

    logger = logging.getLogger(__name__)


    def get_supabase_client(url: str, key: str) -> Client:
    """Cria e retorna um cliente Supabase."""
          try:
              client = create_client(url, key)
              logger.info("Conexao com Supabase estabelecida com sucesso")
              return client
          except Exception as e:
        logger.error(f"Erro ao conectar no Supabase: {e}")
                  raise


          def get_active_contacts(client: Client, table: str, limit: int = 3) -> list:
    """Busca contatos ativos no Supabase."""
          try:
              logger.info(f"Buscando contatos na tabela '{table}' (limite: {limit})...")
              response = (
                  client.table(table)
                  .select("id, nome_contato, telefone")
                  .eq("ativo", True)
                  .limit(limit)
                  .execute()
              )
              contacts = response.data
              logger.info(f"{len(contacts)} contato(s) encontrado(s)")
              return contacts
          except Exception as e:
        logger.error(f"Erro ao buscar contatos no Supabase: {e}")
                  raise
