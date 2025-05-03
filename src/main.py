import logging
from src.database.login.iniciar_database import iniciar_database
from src.database.models.fazenda import Fazenda
from src.database.tipos_base.database import Database
from src.logger.config import configurar_logger
from src.menu.menu_principal import menu_principal
import pandas as pd
import traceback

def main():
    configurar_logger()
    iniciar_database()
    Database.create_all_tables(drop_if_exists=False)

    #necessário para o panda não truncar os dados
    pd.options.display.max_rows = 99
    pd.options.display.max_columns = 99
    pd.options.display.width = 200

    while True:

        try:
            sair = menu_principal()

            if sair:
                break
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")
            break

        except SystemExit:
            print("\n\nSaindo do sistema...")
            break

        except Exception as e:
            stacktrace = traceback.format_exc()
            logging.critical(f'{e}\n{stacktrace}\nErro inesperado saindo do sistema...')
            raise

main()