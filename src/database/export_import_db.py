from sqlalchemy.exc import DatabaseError
from src.database.dynamic_import import import_models, get_model_by_table_name
import io
import zipfile
import pandas as pd
from src.database.tipos_base.model import Model
from typing import List


def convert_database_to_dataframes() -> list[tuple[Model, pd.DataFrame]]:
    """
    Converte um modelo em um DataFrame do pandas.
    :param model:
    :return:
    """

    response = []

    models = import_models()

    for model_name, model_class in models.items():
        try:
            dataframe = model_class.as_dataframe()
            response.append((model_class, dataframe))
        except DatabaseError as e:
            if e.code == " DPY-4011":
                dataframe = model_class.as_dataframe()
                response.append((model_class, dataframe))
            else:
                print(e.code)

                raise


    return response

def create_database_zip_export() -> io.BytesIO:
    """
    Cria um buffer zip com os dados do banco de dados.
    :return: Buffer contendo o arquivo zip.
    """
    dataframes = convert_database_to_dataframes()
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for model_name, df in dataframes:
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            zip_file.writestr(f"{model_name.__tablename__}.csv", csv_buffer.getvalue())

    zip_buffer.seek(0)  # Retorna o ponteiro do buffer para o início
    return zip_buffer

def import_database_zip(zip_file: io.BytesIO) -> list[tuple[Model, List[Model]]]:
    """
    Importa um arquivo zip contendo arquivos CSV para o banco de dados.
    :param zip_file: Buffer do arquivo zip.
    """

    response = []

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file:
                df = pd.read_csv(file)
                model_class = get_model_by_table_name(file_name[:-4])
                response.append((model_class, model_class.from_dataframe(df)))

    return response

