import streamlit as st

from src.dashboard.principal import get_principal_page
from src.dashboard.generic.table_view import TableView
from src.database.dynamic_import import import_models
from src.dashboard.menu import menu


def get_generic_pages() -> list:
    """
    Função para importar dinamicamente os módulos e retornar uma lista de páginas genéricas que fazem o CRUD.
    """

    rotas = []

    models = import_models()


    items = list(models.items())
    items.sort(key=lambda x: x[1].display_name())
    for model_name, model in items:
        view = TableView(model)
        rotas.extend(view.get_routes())
    return rotas

def navigation():
    """
    Função para exibir a página principal do aplicativo.
    :return:
    """

    current_page = st.navigation([
        get_principal_page(),
        *get_generic_pages()
    ])

    menu()

    current_page.run()

