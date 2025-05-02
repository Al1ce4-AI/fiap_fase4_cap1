import logging

from src.database.tipos_base.model import Model
from src.database.input_validation import input_bool
from datetime import datetime
import json
from src.settings import EXPORTS_DIR


def exportar_json_generico(
    model: type[Model],
):

    instances = model.all()

    if len(instances) == 0:
        logging.warning(f'Nenhum item {model.display_name()} encontrado na base de dados!')
        return

    data_frame = model.get_dataframes(instances)

    logging.info(f"Instâncias de {model.display_name()} obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()

    print("Deseja exportar os dados para um arquivo JSON?")
    exportar = input_bool("Exportar", modo='S')

    if not exportar:
        logging.info('Cancelando exportação, voltando para o menu anterior...')
        return

    now = datetime.now()

    nome_arquivo = f"{EXPORTS_DIR}/{model.display_name_plural()}-{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"

    print(f"Exportando dados para o arquivo {nome_arquivo}...")

    data = []

    for i in instances:
        data.append(i.to_dict())

    json_string = json.dumps(data, indent=4)

    try:
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(json_string)
    except Exception as e:
        logging.error(f"Erro ao exportar dados para o arquivo {nome_arquivo}: {e}, tente novamente mais tarde!")
        return

    logging.info(f"Dados exportados com sucesso para o arquivo {nome_arquivo}!")


