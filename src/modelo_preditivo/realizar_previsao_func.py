import joblib
import pandas as pd
from typing import Literal
from datetime import datetime
import os

def converte_data_leitura(hora_leitura: datetime) -> float:

    return  hora_leitura.hour * 60 + hora_leitura.minute + hora_leitura.second / 60 + hora_leitura.microsecond / 60_000_000


def carregar_modelo_e_realizar_previsao(path_arquivo: str, *,
                                        hora_leitura: datetime,
                                        fosforo: int,
                                        potassio: int,
                                        ph: int,
                                        umidade: float,
                                        ) -> Literal["Não", "Sim"]:
    """
    Carrega o modelo, scaler e label encoder salvos, aplica o scaler ao novo dado,
    realiza a previsão e converte o resultado para a categoria original (texto).

    :param hora_leitura: Hora da leitura do sensor.
    :param fosforo: Estado do fósforo (0 ou 1).
    :param potassio: Estado do potássio (0 ou 1).
    :param ph: Estado do pH (0 ou 1).
    :param umidade: Umidade do solo.

    """

    # Carregando modelo, scaler e label encoder salvos
    modelo_load = joblib.load(path_arquivo)


    modelo = modelo_load['modelo']
    print(modelo.feature_names_in_)
    scaler = modelo_load['scaler']
    le = modelo_load['label_encoder']  # Carregando o LabelEncoder

    data_convertido = converte_data_leitura(hora_leitura)
    data_convertido_scaled = scaler.transform([[data_convertido, fosforo, potassio, ph, umidade]])
    print(f"Data convertida: {data_convertido}, Data convertida escalada: {data_convertido_scaled}")


    data_frame_prever = pd.DataFrame({
        'hora_leitura': [data_convertido_scaled[0][0]],
        'Fósforo': [fosforo],
        'Potássio': [potassio],
        'PH': [ph],
        'Umidade': [data_convertido_scaled[0][4]]
    })


    # Aplicando o scaler ao novo dado
    novo_dado_scaled = scaler.transform(data_frame_prever)

    # Fazendo a previsão
    previsao = modelo.predict(novo_dado_scaled)

    # Convertendo o resultado para a categoria original (texto)
    previsao_texto = le.inverse_transform(previsao)

    return previsao_texto[0]

def realizar_previsao_modelo_padrao(
        hora_leitura: datetime,
        fosforo: int,
        potassio: int,
        ph: int,
        umidade: float
) -> Literal["Não", "Sim"]:
    """
    Realiza a previsão usando o modelo padrão.

    :param hora_leitura: Hora da leitura do sensor.
    :param fosforo: Estado do fósforo (0 ou 1).
    :param potassio: Estado do potássio (0 ou 1).
    :param ph: Estado do pH (0 ou 1).
    :param umidade: Umidade do solo.
    """

    caminho = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(caminho, 'modelos_otimizados_salvos', 'SVMrbf.pkl')

    return carregar_modelo_e_realizar_previsao(
        path_arquivo=caminho,
        hora_leitura=hora_leitura,
        fosforo=fosforo,
        potassio=potassio,
        ph=ph,
        umidade=umidade
    )


if __name__ == "__main__":
    # modelo_load = joblib.load(r"E:\PythonProject\fiap_fase4_cap1\src\modelo_preditivo\modelos_otimizados_salvos\ExtraTrees100.pkl")
    #
    # modelo:ExtraTreesClassifier = modelo_load['modelo']
    # print(modelo.feature_names_in_)
    # scaler = modelo_load['scaler']
    # print(scaler)
    # le:LabelEncoder = modelo_load['label_encoder']
    #
    # print(le.classes_)

    print(carregar_modelo_e_realizar_previsao(
        path_arquivo=r"modelos_otimizados_salvos\SVMrbf.pkl",
        hora_leitura=datetime.now(),
        fosforo=1,
        potassio=1,
        ph=7,
        umidade=45.5
    ))