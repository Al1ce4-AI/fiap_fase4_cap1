import streamlit as st
from typing import List

from src.dashboard.database.exportar import exportar_db_page
from src.dashboard.database.importar import importar_db_page
from src.dashboard.generic.table_view import TableView
from src.dashboard.plots.views import grafico_umidade_view, grafico_estado_do_rele, grafico_ph, grafico_fosforo, \
    grafico_potassio
from src.dashboard.principal import get_principal_page
from src.database.dynamic_import import import_models
from src.database.models.cultura import Cultura
from src.database.models.fazenda import Propriedade, Campo, Plantio
from src.database.models.irrigacao import Irrigacao
from src.database.models.nutriente import Nutriente
from src.database.models.sensor import TipoSensor, Sensor, LeituraSensor
from src.database.models.unidade import Unidade

def crud_menu():
    """
    Função para exibir o menu lateral do aplicativo.
    Cria as páginas de CRUD para os modelos do banco de dados.
    """

    st.sidebar.header("Cadastro de Fazendas")

    menu_fazenda:List[TableView] = [
        TableView(Propriedade),
        TableView(Campo),
        TableView(Cultura),
        TableView(Plantio),
        TableView(Nutriente),
    ]

    for i in menu_fazenda:
        st.sidebar.page_link(i.get_table_page())

    st.sidebar.header("Cadastro de Sensores")

    menu_sensor:List[TableView] = [
        TableView(TipoSensor),
        TableView(Sensor),
        TableView(LeituraSensor),
        TableView(Irrigacao),
    ]
    for i in menu_sensor:
        st.sidebar.page_link(i.get_table_page())

    menu_models_already_used = set(map(lambda x: x.model, [*menu_fazenda, *menu_sensor]))


    # Importa os modelos do banco de dados e filtra os que já estão no menu

    models = import_models()

    items = list(models.items())
    items = list(filter(lambda x: x[1] not in menu_models_already_used, items))
    items.sort(key=lambda x: x[1].display_name())

    if len(items) > 0:
        st.sidebar.header("Cadastro de Outros Modelos")

        for model_name, model in items:
            view = TableView(model)

            st.sidebar.page_link(view.get_table_page())

def plot_menu():
    """
    Função para exibir o menu lateral do aplicativo.
    Cria as páginas de gráficos para os modelos do banco de dados.
    """

    st.sidebar.header("Gráficos")
    st.sidebar.page_link(grafico_umidade_view.get_page())
    st.sidebar.page_link(grafico_estado_do_rele.get_page())
    st.sidebar.page_link(grafico_ph.get_page())
    st.sidebar.page_link(grafico_fosforo.get_page())
    st.sidebar.page_link(grafico_potassio.get_page())

def export_import_menu():
    """
    Função para exibir o menu lateral do aplicativo.
    Cria as páginas de exportação e importação do banco de dados.
    """

    st.sidebar.header("Exportar/Importar")
    st.sidebar.page_link(exportar_db_page)
    st.sidebar.page_link(importar_db_page)

def menu():
    """
    Função para exibir o menu lateral do aplicativo.
    É necessário pois como temos muitas subpáginas que não vão no menu lateral,
    temos que dizer exatamente quais são as páginas que vão no menu lateral.
    """

    st.sidebar.page_link(get_principal_page())
    crud_menu()
    plot_menu()
    export_import_menu()

