from datetime import datetime
from random import randrange, choice
from typing import Literal, Optional
from src.database.models.sensor import LeituraSensor


def criar_dados_leitura(
        data_inicial:datetime,
        data_final:datetime,
        sensor_id:int,
        total_leituras:int,
        tipo:Literal['bool', 'range'],
        minimo:Optional[float],
        maximo:Optional[float]
) -> list[LeituraSensor]:
    """
    Cria dados de leitura um sensor específico em um intervalo de datas.

    Args:
        data_inicial (datetime): Data inicial do intervalo.
        data_final (datetime): Data final do intervalo.
        sensor_id (int): ID do sensor.
        total_leituras (int): Total de leituras a serem geradas.
        tipo (Literal['bool', 'range']): Tipo de leitura a ser gerada ('bool' ou 'range').
        minimo (float or None): Valor mínimo para o tipo 'range'. Ignorado se tipo for 'bool'.
        maximo (float or None): Valor máximo para o tipo 'range'. Ignorado se tipo for 'bool'.

    Returns:
        list: Lista de dicionários com os dados de leitura gerados.
    """

    assert (data_inicial < data_final), "A data inicial deve ser anterior à data final."
    assert (tipo == 'bool' or tipo == 'range'), "O tipo deve ser 'bool' ou 'range'."
    assert (tipo != 'range' or (minimo is not None and maximo is not None)), "O tipo 'range' requer valores mínimo e máximo."
    assert (minimo is None or maximo is None or minimo < maximo), "O valor mínimo deve ser menor que o máximo."

    leituras = []

    for i in range(total_leituras):
        data_leitura = data_inicial + (data_final - data_inicial) * (i / total_leituras)
        if tipo == 'bool':
            valor = choice([0, 1])
        elif tipo == 'range':
            valor = randrange(minimo, maximo)
        else:
            raise ValueError("Tipo inválido. Deve ser 'bool' ou 'range'.")
        leituras.append(LeituraSensor(
            sensor_id=sensor_id,
            data_leitura=data_leitura,
            valor=valor
        ))

    return leituras
