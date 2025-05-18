import streamlit as st
from src.database.models.fazenda import Plantio
from src.database.models.irrigacao import Irrigacao
from src.database.tipos_base.database import Database
from src.dashboard.global_messages import add_global_message



def get_irrigacao_page():
    st.title("💧 Controle de Irrigação Inteligente")

    with Database.get_session() as session:
        plantios = session.query(Plantio).all()
        if not plantios:
            st.warning("Nenhum plantio cadastrado!")
            return

        plantio = st.selectbox(
            "Selecione o plantio:",
            plantios,
            format_func=lambda p: f"{p.nome} (Campo: {p.campo.identificador})"
        )

        if st.button("Analisar Necessidade de Irrigação", type="primary"):
            deve_irrigar, dados = Irrigacao.decidir_irrigacao(plantio.id)

            st.subheader("📊 Dados Atuais")
            cols = st.columns(3)
            cols[0].metric("Umidade Solo", f"{dados['umidade']}%",
                "Baixa" if dados['umidade'] < 30 else "Adequada")
            cols[1].metric("pH", dados['ph'],
                "Ideal" if 5.5 <= dados['ph'] <= 7.0 else "Fora da faixa")
            cols[2].metric("Previsão Chuva",
                "Sim" if dados['clima']['chuva'] else "Não")

            st.subheader("Recomendação")
            if deve_irrigar:
                st.success("IRRIGAR AGORA - Solo seco e condições favoráveis")
                if st.button("Acionar Irrigação", key="irrigar"):
                    add_global_message(f"Irrigação acionada para {plantio.nome}!")
            else:
                st.error("NÃO IRRIGAR - Condições não satisfeitas")


irrigacao_page = st.Page(get_irrigacao_page, title="Irrigação", url_path="irrigacao2", icon="💧")
