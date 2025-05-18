from src.database.login.iniciar_database import iniciar_database
from src.database.tipos_base.database import Database
from src.logger.config import configurar_logger

def main():
    """Função principal do programa."""
    configurar_logger()
    iniciar_database()
    Database.create_all_tables(drop_if_exists=False)
    print(Database.generate_ddl())
    print(Database.generate_mer())

main()