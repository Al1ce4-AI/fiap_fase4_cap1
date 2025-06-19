import streamlit as st
import pandas as pd
import plotly.express as px
import os

def view():
    st.title("💧 Análise Interativa dos Sensores de Irrigação")

    data = pd.read_csv("assets/dataset_irrigacao.csv")
    df = pd.DataFrame(data)

    # Conversão da coluna de hora para datetime
    df["hora_leitura"] = pd.to_datetime(df["hora_leitura"], format="%I:%M:%S %p")
    df = df.sort_values("hora_leitura")

    # Filtro de intervalo de horários
    st.sidebar.header("⏰ Filtro de Intervalo de Horários")
    horarios_disponiveis = df["hora_leitura"].dt.strftime("%H:%M:%S").tolist()
    start_idx, end_idx = st.sidebar.select_slider(
        "Selecione o intervalo de horários:",
        options=list(range(len(horarios_disponiveis))),
        value=(0, len(horarios_disponiveis) - 1),
        format_func=lambda i: horarios_disponiveis[i]
    )
    df_filtrado = df.iloc[start_idx:end_idx + 1]

    # Tabela com os dados filtrados
    st.subheader("Dados dos Sensores no Intervalo Selecionado")
    st.dataframe(df_filtrado)

    # Gráficos interativos
    st.subheader("Visualização dos Sensores")
    sensores = [
        "sensor_1_Sensor Fósforo",
        "sensor_2_Sensor Potássio",
        "sensor_3_Sensor PH",
        "sensor_4_Sensor Umidade"
    ]
    sensor_escolhido = st.selectbox("Selecione o sensor para visualizar:", sensores)
    fig = px.line(df_filtrado, x="hora_leitura", y=sensor_escolhido, title=f"{sensor_escolhido} ao longo do tempo")
    st.plotly_chart(fig)

    # Gráficos individuais para cada sensor
    st.subheader("Gráficos Individuais dos Sensores")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(df_filtrado, x="hora_leitura", y="sensor_1_Sensor Fósforo", title="Sensor Fósforo")
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = px.line(df_filtrado, x="hora_leitura", y="sensor_3_Sensor PH", title="Sensor PH")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig3 = px.line(df_filtrado, x="hora_leitura", y="sensor_2_Sensor Potássio", title="Sensor Potássio")
        st.plotly_chart(fig3, use_container_width=True)
        fig4 = px.line(df_filtrado, x="hora_leitura", y="sensor_4_Sensor Umidade", title="Sensor Umidade")
        st.plotly_chart(fig4, use_container_width=True)

    # Estado do Relé
    st.subheader("Estado do Relé de Irrigação")
    fig_rele = px.line(df_filtrado, x="hora_leitura", y="sensor_5_Sensor Estado do Relé de Irrigação", title="Estado do Relé de Irrigação", markers=True)
    st.plotly_chart(fig_rele)


exploracao_de_dados = st.Page(
    view,
    title="Exploração de Dados",
    url_path="exploracao_de_dados",
)
