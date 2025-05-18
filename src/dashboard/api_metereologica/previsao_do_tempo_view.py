import logging

import streamlit as st
from enum import Enum
from src.dashboard.plots.generic.grafico_barras import get_grafico_barras
from src.dashboard.plots.generic.grafico_degrau import get_grafico_degrau
from src.dashboard.plots.generic.grafico_linha import get_grafico_linha
from src.dashboard.plots.generic.utils import get_sensores_por_tipo, get_leituras_for_sensor
from src.database.generator.criar_dados_leitura import criar_dados_litura_para_sensor
from src.database.models.sensor import TipoSensorEnum, LeituraSensor, Sensor
from datetime import datetime, timedelta

from src.service.get_weather import obter_dados_clima


class PrevisaoDoTempoView:

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

        cidade_input = st.text_input(
            label="Digite o nome da cidade",
            help="Digite o nome da cidade para obter a previsão do tempo.",
        )

        if cidade_input is None:
            return


        if st.button("Obter previsão do tempo"):

            if len(cidade_input.strip()) > 0:
                # spinner para obter a previsão do tempo

                previsao = None

                try:
                    with st.spinner("Obtendo a previsão do tempo..."):
                        previsao = self.obter_previsao_do_tempo(cidade_input)
                except Exception as e:
                    logging.error(e)
                    st.error(f"Erro ao obter a previsão do tempo: {e}")
                    return
                if previsao is None:
                    st.error("Não foi possível obter a previsão do tempo.")
                    return

                # exibir a previsão do tempo
                st.subheader(f"Previsão do tempo para {cidade_input}")
                st.write(f"Temperatura: {previsao['temperatura']}°C")
                st.write(f"Umidade do ar: {previsao['umidade_ar']}%")
                st.write(f"Condição: {previsao['condicao'].capitalize()}")
                st.write(f"Chuva prevista: {'Sim' if previsao['chuva'] else 'Não'}")


    def obter_previsao_do_tempo(self, cidade: str) -> dict:
        """
        Função para obter a previsão do tempo para uma cidade específica.
        :param cidade: str - Nome da cidade.
        :return: dict - Previsão do tempo.
        """
        return obter_dados_clima(cidade=cidade)

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

