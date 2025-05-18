from src.database.login.iniciar_database import iniciar_database
from src.database.tipos_base.database import Database
from src.logger.config import configurar_logger

def main():
    """Função principal do programa."""
    configurar_logger()
    iniciar_database()
    Database.create_all_tables(drop_if_exists=False)
    ddl = Database.generate_ddl()

    with open("export.ddl", "w") as f:
        f.write(ddl)

    mer = Database.generate_mer()

    with open("export.mer", "w") as f:
        f.write(mer)

main()