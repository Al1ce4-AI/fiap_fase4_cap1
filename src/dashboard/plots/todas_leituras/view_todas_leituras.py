import streamlit as st
from enum import Enum
from src.dashboard.plots.generic.grafico_barras import get_grafico_barras
from src.dashboard.plots.generic.grafico_degrau import get_grafico_degrau
from src.dashboard.plots.generic.grafico_linha import get_grafico_linha
from src.dashboard.plots.generic.utils import get_sensores_por_tipo, get_leituras_for_sensor
from src.dashboard.plots.todas_leituras.plot_todas_leituras_linha import get_grafico_linha_todas_leituras
from src.database.models.sensor import TipoSensorEnum, LeituraSensor, Sensor
from datetime import datetime, timedelta


class PlotAllView:

    def __init__(self,
                    title: str,
                    url_path: str,
                 ):
        self.title = title
        self.url_path = url_path

    def view(self):
        """
        Função para exibir a página principal do aplicativo.
        :return:
        """
        st.title(self.title)

        sensores_selecionados = {}

        for tipo in TipoSensorEnum:

            sensores = get_sensores_por_tipo(tipo)

            sensores_selecionados[tipo.value] = st.selectbox(
                label=f"Selecione um sensor de f{str(tipo)}",
                options=sensores,
                format_func=lambda x: str(x),
                # index=[opt[0] for opt in sensores].index(current_value) if current_value else None,
                # help=field.comment,
            )

        data_inicial = st.date_input("Data inicial", value=datetime.now(), format="DD/MM/YYYY")
        data_final = st.date_input("Data final", value=datetime.now() + timedelta(days=7), format="DD/MM/YYYY")

        if None not in list(sensores_selecionados.values()) and data_inicial is not None and data_final is not None:

            sensor_umidade = sensores_selecionados[TipoSensorEnum.UMIDADE.value]
            sensor_rele = sensores_selecionados[TipoSensorEnum.RELE.value]
            sensor_ph = sensores_selecionados[TipoSensorEnum.PH.value]
            sensor_fosforo = sensores_selecionados[TipoSensorEnum.FOSFORO.value]
            sensor_potassio = sensores_selecionados[TipoSensorEnum.POTASSIO.value]

            leituras_umidade = get_leituras_for_sensor(sensor_umidade.id, data_inicial, data_final)
            leituras_rele = get_leituras_for_sensor(sensor_rele.id, data_inicial, data_final)
            leituras_ph = get_leituras_for_sensor(sensor_ph.id, data_inicial, data_final)
            leituras_fosforo = get_leituras_for_sensor(sensor_fosforo.id, data_inicial, data_final)
            leituras_potassio = get_leituras_for_sensor(sensor_potassio.id, data_inicial, data_final)

            if len(leituras_umidade) == 0 and len(leituras_rele) == 0 and len(leituras_ph) == 0 and len(leituras_fosforo) == 0 and len(leituras_potassio) == 0:
                st.warning("Nenhum dado encontrado para os sensores selecionados entre as datas informadas.")
            else:
                get_grafico_linha_todas_leituras(
                    leituras_umidade,
                    leituras_rele,
                    leituras_ph,
                    leituras_fosforo,
                    leituras_potassio,
                    f"Gráfico de todas as leituras entre {data_inicial} e {data_final}"
                )


        else:
            st.warning("Selecione os sensores e as datas para gerar o gráfico.")

    def get_page(self) -> st.Page:
        """
        Função para retornar a página de gráfico de umidade.
        :return: st.Page - A página para gerar o gráfico de umidade do aplicativo.
        """
        return st.Page(
            self.view,
            title=self.title,
            url_path=self.url_path
        )

