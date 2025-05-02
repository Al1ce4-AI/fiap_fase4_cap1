import logging
from src.database.tipos_base.model import Model


def listar_generico(model:type[Model]):
    try:
        instances = model.all()
    except Exception as e:
        logging.warning(f'Erro ao buscar instâncias de {model.display_name()} na base de dados: {e}\nTente novamente mais tarde!')
        return

    if len(instances) == 0:
        logging.warning(f'Nenhuma instância de {model.display_name()} encontrada na base de dados!')
        return

    data_frame = model.get_dataframes(instances)

    logging.info(f"Instâncias de {model.display_name_plural()} obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()
    input("Pressione qualquer ENTER para continuar...")
