import streamlit as st

from src.dashboard.generic.table_view import TableView
from src.dashboard.principal import get_principal_page
from src.database.dynamic_import import import_models


def menu():
    """
    Função para exibir o menu lateral do aplicativo.
    É necessário pois como temos muitas subpáginas que não vão no menu lateral,
    temos que dizer exatamente quais são as páginas que vão no menu lateral.
    """

    st.sidebar.page_link(get_principal_page())

    models = import_models()


    items = list(models.items())
    items.sort(key=lambda x: x[1].display_name())
    for model_name, model in items:
        view = TableView(model)
        st.sidebar.page_link(view.get_table_page())

