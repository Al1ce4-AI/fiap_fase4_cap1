import logging
import datetime
import streamlit as st
import os

from src.modelo_preditivo.realizar_previsao_func import carregar_modelo_e_realizar_previsao
from src.settings import DEBUG


def modelo_preditivo_view():
    """
    View para realizar previsões manuais com o modelo preditivo.
    :return:
    """

    st.title("🔮 Previsão Manual com Modelo Preditivo")

    st.write("Nesta página, você pode realizar previsões manuais utilizando o modelo preditivo treinado.")

    #pega os modelos em src/modelo_preditivo/modelos_otimizados_salvos

    if not os.path.exists("src/modelo_preditivo/modelos_otimizados_salvos"):
        st.error("⚠️ Modelo preditivo não encontrado. Por favor, treine o modelo antes de realizar previsões.")
        return

    modelos_paths = [f for f in os.listdir("src/modelo_preditivo/modelos_otimizados_salvos") if f.endswith('.pkl')]

    # Carrega o modelo preditivo
    modelo_selecionado = st.selectbox(
        "Selecione o modelo preditivo:",
        options=modelos_paths,
        format_func=lambda x: x.replace('.pkl', '')  # Exibe o nome do modelo sem a extensão
    )

    if not modelo_selecionado:
        st.error("⚠️ Nenhum modelo selecionado.")
        return

    modelo_selecionado_full_path = os.path.join("src/modelo_preditivo/modelos_salvos", modelo_selecionado)

    data_leitura = st.date_input("Data da leitura:", value=datetime.date.today())
    hora_leitura = st.time_input("Hora da leitura:", value=datetime.datetime.now().time())
    fosforo = st.number_input("Fósforo (0 ou 1):", min_value=0, max_value=1, value=1)
    potassio = st.number_input("Potássio (0 ou 1):", min_value=0, max_value=1, value=1)
    ph = st.number_input("pH (0 ou 1):", min_value=0, max_value=1, value=1)
    umidade = st.number_input("Umidade do solo:", min_value=0.0, value=45.5)

    # Combina data e hora em um datetime
    hora_leitura_dt = datetime.datetime.combine(data_leitura, hora_leitura)

    if st.button("Realizar Previsão"):
        try:
            previsao = carregar_modelo_e_realizar_previsao(
                modelo_selecionado_full_path,
                hora_leitura=hora_leitura_dt,
                fosforo=fosforo,
                potassio=potassio,
                ph=ph,
                umidade=umidade
            )
            st.success(f"🔮 Previsão realizada com sucesso!\nPrecisa Irrigar?: {previsao}")
        except Exception as e:
            st.error(f"⚠️ Erro ao realizar a previsão: {str(e)}")
            logging.error(e)
            if DEBUG:
                raise

previsao_manual_page = st.Page(
    modelo_preditivo_view,
    title="Previsão Manual",
    url_path="previsao_manual"
)