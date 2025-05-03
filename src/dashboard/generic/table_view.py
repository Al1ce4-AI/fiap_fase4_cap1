import streamlit as st
from src.dashboard.generic.edit_view import EditView
from src.database.tipos_base.model import Model


class TableView:
    """
    View que exibe uma tabela de um modelo e permite a edição dos registros.
    """

    def __init__(self, model: type[Model]):
        self.model = model

    def get_table_page(self) -> st.Page:
        return st.Page(
                self.table_view,
                title=self.model.display_name(),
                url_path=self.model.__name__.lower()
            )

    def get_edit_page(self) -> st.Page:
        return st.Page(
                self.edit_view,
                title=f"Editar {self.model.display_name()}",
                # De acordo com a documentação do Streamlit, o url_path não pode ter /
                url_path=f"{self.model.__name__.lower()}_edit"
            )

    def get_routes(self) -> list:

        rotas = [
            self.get_table_page(),
            self.get_edit_page(),
        ]

        return rotas


    def table_view(self):

        st.title(self.model.display_name_plural())

        # criar colunas
        col1, col2 = st.columns([5, 1])  # Tabela (col1) maior, botão "Novo" (col2) menor

        with col2:
            # Criar um novo registro
            if st.button("Novo"):
                st.switch_page(self.get_edit_page())
                # st.rerun()

        with col1:
            # Mostrar tabela
            data = self.model.all()
            if len(data) > 0:
                for index, row in data.iterrows():
                    if st.button(f"Editar {row['id']}"):  # Botão para cada item
                        st.session_state['edit_id'] = row['id']
                        print(row['id'])  # Redirecionar para edição
            else:
                st.write("Nenhum dado disponível.")

    def edit_view(self, model_id: int|None = None):
        """
        Função para exibir o formulário de edição.
        :param model_id:
        :return:
        """
        edit_instance = EditView(self.model, model_id, )
        return edit_instance.get_cadastro_view()