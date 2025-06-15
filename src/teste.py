from src.database.generator.criar_dados_leitura import criar_dados_leitura
from src.database.generator.gerar_sensores_e_dados import criar_dados_sample
from src.database.login.iniciar_database import iniciar_database
from src.database.models.sensor import LeituraSensor, Sensor
from src.database.reset_contador_ids import reset_contador_ids, get_sequences_from_db
from src.database.tipos_base.database import Database
from src.logger.config import configurar_logger
from datetime import datetime, timedelta
import pandas as pd

def gerar_mer_e_ddl():
    """Gera o MER e DDL do banco de dados."""
    Database.init_sqlite("../database.db")
    Database.create_all_tables(drop_if_exists=False)
    ddl = Database.generate_ddl()

    with open("../assets/export.ddl", "w") as f:
        f.write(ddl)

    mer = Database.generate_mer()

    with open("../assets/export.mer", "w") as f:
        f.write(mer)


def teste():
    """Função teste do programa."""
    Database.init_sqlite("../database.db")
    Database.create_all_tables(drop_if_exists=False)
    ddl = Database.generate_ddl()
    pd.set_option('display.width', 200)  # aumenta a largura total em caracteres
    pd.set_option('display.max_columns', 20)

    hoje = datetime.now()

    data_inicial = hoje - timedelta(days=30)

    leituras = criar_dados_sample(
        data_inicial=data_inicial,
        data_final=hoje,
        total_leituras=1000
    )

    todas_leituras = []

    for sensor, l in leituras:
        todas_leituras = todas_leituras + l

    print(f"Salvando {len(todas_leituras)} leituras na database.")
    with Database.get_session() as session:
        session.add_all(todas_leituras)
        session.commit()

    print(LeituraSensor.count())

    sensores = Sensor.all()

    print(f"Total de sensores: {len(sensores)}")

    df_ml = LeituraSensor.get_dataset_for_machine_learning(
        sensor_ids=[sensor.id for sensor in sensores],
        data_inicial=data_inicial,
        data_final=hoje
    )

    print(df_ml)


if __name__ == "__main__":
    gerar_mer_e_ddl()
    teste()