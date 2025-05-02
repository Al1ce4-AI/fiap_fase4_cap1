from contextlib import contextmanager
from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import json

from src.settings import SQL_ALCHEMY_DEBUG

DEFAULT_DSN = "oracle.fiap.com.br:1521/ORCL"

class Database:

    engine:Engine
    session:sessionmaker

    @staticmethod
    def init_oracledb(user:str, password:str, dsn:str=DEFAULT_DSN):
        '''
        Inicializa a conexão com o banco de dados Oracle.
        :param user: Nome do usuário do banco de dados.
        :param password: Senha do usuário do banco de dados.
        :param dsn: DSN do banco de dados.
        :return:
        '''

        # Cria o engine de conexão
        engine = create_engine(f"oracle+oracledb://{user}:{password}@{dsn}", echo=SQL_ALCHEMY_DEBUG)

        # Testa a conexão
        with engine.connect() as _:
            print("Conexão bem-sucedida ao banco de dados Oracle!")
        Database.engine = engine
        Database.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def init_from_session(engine:Engine, session:sessionmaker):
        """
        Inicializa a conexão com o banco de dados a partir de um engine e sessionLocal já existentes.
        :param engine: Engine do banco de dados.
        :param session: SessionLocal do banco de dados.
        :return:
        """
        Database.engine = engine
        Database.session = session

    @staticmethod
    def init_oracledb_from_file(path:str = r"E:\PythonProject\fiap_fase3_cap1\login.json"):

        """
        Inicializa a conexão com o banco de dados Oracle a partir de um arquivo JSON.
        :param path: Caminho do arquivo JSON com as credenciais do banco de dados.
        :return:
        """
        with open(path, "r") as file:
            data = json.load(file)
            user = data["user"]
            password = data["password"]

        Database.init_oracledb(user, password)

    @staticmethod
    @contextmanager
    def get_session() -> Generator[Session, None, None]:
        db = Database.session()
        try:
            yield db
        finally:
            db.close()

    @classmethod
    def list_tables(cls) -> list[str]:
        """
        Lista as tabelas do banco de dados.
        :return: List[str] - Lista com os nomes das tabelas.
        """
        engine = cls.engine
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tables = metadata.tables.keys()
        return list(tables)

    @classmethod
    def list_sequences(cls):
        """
        Lista todas as sequences do banco de dados.
        :return: Lista com os nomes das sequences.
        """
        metadata = MetaData()
        metadata.reflect(bind=cls.engine)
        sequences = [seq.name for seq in metadata._sequences.values()]
        return sequences

    @classmethod
    def create_all_tables(cls, drop_if_exists:bool=False):
        """
            Cria todas as tabelas do banco de dados que herdam de Model.
            ATENÇÃO: Para isso funcionar deve-se carregar todos os models na memória.
            :param drop_if_exists: Se True, remove as tabelas existentes antes de criar novas.
        """

        if drop_if_exists:
            cls.drop_all_tables()

        from src.database.tipos_base.model import Model
        from src.database.dynamic_import import import_models

        import_models()

        try:
            Model.metadata.create_all(bind=cls.engine)
            print("Tabelas criadas com sucesso.")
        except Exception as e:
            print("Erro ao criar tabelas no banco de dados.")
            raise

    @classmethod
    def drop_all_tables(cls):
        """
            Dropa todas as tabelas do banco de dados.
            ATENÇÃO: Para isso funcionar deve-se carregar todos os models na memória.
        """
        from src.database.tipos_base.model import Model
        from src.database.dynamic_import import import_models

        import_models()

        try:
            Model.metadata.drop_all(bind=cls.engine)
            print("Tabelas removidas com sucesso.")
        except Exception as e:
            print("Erro ao remover tabelas do banco de dados.")
            raise
