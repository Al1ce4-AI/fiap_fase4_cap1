from enum import StrEnum
from typing import List, Union, Any
from sqlalchemy import Sequence, String, Text, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.fazenda import Plantio
from src.database.models.unidade import Unidade
from src.database.tipos_base.database import Database
from src.database.tipos_base.model import Model
from datetime import datetime, date, time, timedelta
from typing import Self, Optional
import pandas as pd
from random import choice, randrange
import numpy as np

class TipoSensorEnum(StrEnum):
    FOSFORO = "P"
    POTASSIO = "K"
    PH = "pH"
    UMIDADE = "H"
    RELE = "Rele"

    def __str__(self):

        if self.value == "P":
            return "Fósforo"
        if self.value == "K":
            return "Potássio"
        if self.value == "pH":
            return "PH"
        if self.value == "H":
            return "Umidade"
        if self.value == "Rele":
            return "Estado do Relé"

        return super().name

    def get_type_for_generation(self) -> Union[type[float], type[int], type[bool]]:

        match self:
            case TipoSensorEnum.FOSFORO:
                return bool
            case TipoSensorEnum.POTASSIO:
                return bool
            case TipoSensorEnum.PH:
                return float
            case TipoSensorEnum.UMIDADE:
                return float
            case TipoSensorEnum.RELE:
                return bool

        return float



    def get_range_for_generation(self) -> Union[tuple[float, float], None]:
        match self:
            case TipoSensorEnum.PH:
                return 0.0 , 14.0
            case TipoSensorEnum.UMIDADE:
                return 0.0 , 100.0

        return 0, 100.0

    def get_valor_escalado(self, valor) -> Any:
        """
        Retorna o valor escalado de acordo com o tipo do sensor.
        :param valor: Valor a ser escalado.
        :return: Valor escalado.
        """

        return valor


class TipoSensor(Model):
    """Representa um tipo de sensor que pode ser utilizado em uma plantação."""

    __tablename__ = 'TIPO_SENSOR'
    __menu_group__ = "Sensores"
    __menu_order__ = 1
    __database_import_order__ = 10

    @classmethod
    def display_name(cls) -> str:
        return "Tipo de Sensor"

    @classmethod
    def display_name_plural(cls) -> str:
        return "Tipos de Sensores"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_SEQ_ID"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        info={
            'label': 'Nome'
        },
        comment="Ex.: Fósforo, Potássio, pH, Umidade, Rele"
    )

    tipo: Mapped[TipoSensorEnum] = mapped_column(
        Enum(TipoSensorEnum, length=15),
        nullable=False,
        unique=False,
        info={
            'label': 'Tipo'
        },
        comment="Tipo do sensor, Ex.: Fósforo, Potássio, pH, Umidade, Rele"
    )

    sensors: Mapped[list['Sensor']] = relationship('Sensor', back_populates='tipo_sensor')

    def __str__(self):
        return f"{self.id} - {self.nome}"

class Sensor(Model):
    """Representa um sensor que pode ser utilizado em uma plantação."""

    __tablename__ = 'SENSOR'
    __menu_group__ = "Sensores"
    __menu_order__ = 2
    __database_import_order__ = 11

    @classmethod
    def display_name_plural(cls) -> str:
        return "Sensores"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_SEQ_ID"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    cod_serial: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        unique=False,
        info={
            'label': 'Código Serial'
        },
        comment="Código serial do sensor, utilizado para identificação"
    )

    tipo_sensor_id: Mapped[int] = mapped_column(
        ForeignKey('TIPO_SENSOR.id'),
        nullable=False,
        info={
            'label': 'Tipo de Sensor'
        },
        comment="ID do tipo de sensor associado"
    )

    tipo_sensor: Mapped[TipoSensor] = relationship('TipoSensor', back_populates='sensors')

    plantio_id: Mapped[int] = mapped_column(
        ForeignKey('PLANTIO.id'),
        nullable=True,
        info={
            'label': 'Plantio'
        },
        comment="ID do plantio associado"
    )

    plantio: Mapped[Plantio] = relationship('Plantio', back_populates='sensores')

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        info={
            'label': 'Nome'
        },
        comment="Nome do sensor"
    )

    descricao: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        unique=False,
        info={
            'label': 'Descrição'
        },
        comment="Descrição do sensor"
    )

    data_instalacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        unique=False,
        info={
            'label': 'Data de Instalação'
        },
        comment="Data de instalação do sensor"
    )

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey('UNIDADE.id'),
        nullable=True,
        info={
            'label': 'Unidade'
        },
        comment="ID da unidade de medida associada"
    )

    unidade: Mapped[Unidade] = relationship('Unidade', back_populates='sensors')

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        unique=False,
        info={
            'label': 'Latitude'
        },
        comment="Latitude do sensor"
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        unique=False,
        info={
            'label': 'Longitude'
        },
        comment="Longitude do sensor"
    )


    leituras: Mapped[list['LeituraSensor']] = relationship('LeituraSensor', back_populates='sensor')

    irrigacoes: Mapped[list['Irrigacao']] = relationship('Irrigacao', back_populates='sensor')

    def __str__(self):
        return f"{self.id} - {self.nome}"

    @classmethod
    def filter_by_tiposensor(cls, tipo_sensor: TipoSensorEnum) -> List['Sensor']:
        """Retorna o tipo de sensor correspondente ao enum."""
        with Database.get_session() as session:
            # pega os tipos de sensores de umidade
            tipo_sensor = session.query(TipoSensor).filter(TipoSensor.tipo == tipo_sensor).all()
            tipo_ids = [ts.id for ts in tipo_sensor]

            sensores = session.query(Sensor).filter(Sensor.tipo_sensor_id.in_(tipo_ids)).all()

            return sensores


class LeituraSensor(Model):
    """Representa uma leitura de um sensor em um determinado momento."""

    __tablename__ = 'LEITURA_SENSOR'
    __menu_group__ = "Sensores"
    __menu_order__ = 3
    __database_import_order__ = 12

    @classmethod
    def display_name(cls) -> str:
        return "Leitura de Sensor"

    @classmethod
    def display_name_plural(cls) -> str:
        return "Leituras de Sensores"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_SEQ_ID"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey('SENSOR.id'),
        nullable=False,
        info={
            'label': 'Sensor'
        },
        comment="ID do sensor associado"
    )

    sensor: Mapped[Sensor] = relationship('Sensor', back_populates='leituras')

    data_leitura: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        info={
            'label': 'Data da Leitura'
        },
        comment="Data da leitura do sensor"
    )

    valor : Mapped[float] = mapped_column(
        Float,
        nullable=False,
        info={
            'label': 'Valor'
        },
        comment="Valor da leitura do sensor"
    )

    def __str__(self):
        return f"Sensor_id: {self.sensor_id} - {self.data_leitura.strftime('%Y-%m-%d %H:%M:%S')} - {self.valor}"

    @classmethod
    def get_leituras_for_sensor(cls, sensor_id: int, data_inicial: date, data_final: date):
        with Database.get_session() as session:
            leituras = session.query(LeituraSensor).filter(
                LeituraSensor.sensor_id == sensor_id,
                LeituraSensor.data_leitura >= datetime.combine(data_inicial, time(0, 0, 0)),
                LeituraSensor.data_leitura <= datetime.combine(data_final, time(23, 59, 59, 999999))
            ).order_by(LeituraSensor.data_leitura).all()

            return leituras

    @classmethod
    def get_dataset_for_machine_learning(cls, sensor_ids:List[int], data_inicial: date, data_final: date):
        """
        Obtém um dataset de leituras de sensor para machine learning.
        :param sensor_ids: IDs do sensor.
        :param data_inicial: Data inicial do intervalo.
        :param data_final: Data final do intervalo.
        :return: Lista de dicionários com os dados de leitura.
        """

        df = pd.DataFrame()

        for sensor_id in sensor_ids:
            sensor = Sensor.get_from_id(sensor_id)
            leituras = cls.get_leituras_for_sensor(sensor_id, data_inicial, data_final)
            if not leituras:
                continue

            df_sensor = pd.DataFrame([{
                'data_leitura': leitura.data_leitura,
                'valor': leitura.valor
            } for leitura in leituras])

            df_sensor.set_index('data_leitura', inplace=True)
            df_sensor.sort_index(inplace=True)

            df = pd.concat([df, df_sensor], axis=1)
            #renomear a coluna do novo sensor para o nome do sensor
            df.rename(columns={'valor': f'sensor_{sensor_id}_{sensor.nome}'}, inplace=True)

        return df

    @classmethod
    def criar_dados_leitura(
            cls,
            data_inicial: datetime,
            data_final: datetime,
            sensor_id: int,
            total_leituras: int,
            tipo: TipoSensorEnum,
    ) -> list[Self]:
        """
        Cria dados de leitura um sensor específico em um intervalo de datas.

        Args:
            data_inicial (datetime): Data inicial do intervalo.
            data_final (datetime): Data final do intervalo.
            sensor_id (int): ID do sensor.
            total_leituras (int): Total de leituras a serem geradas.
            tipo (TipoSensorEnum): Tipo de dado a ser gerado.

        Returns:
            list: Lista de dicionários com os dados de leitura gerados.
        """

        assert (data_inicial < data_final), "A data inicial deve ser anterior à data final."
        leituras = []

        for i in range(total_leituras):
            data_leitura = data_inicial + (data_final - data_inicial) * (i / total_leituras)
            if tipo.get_type_for_generation() == bool:
                valor = choice([0, 1])
            elif tipo.get_type_for_generation() == int:
                valor = randrange(*tipo.get_range_for_generation())
            elif tipo.get_type_for_generation() == float:
                valor = np.random.uniform(*tipo.get_range_for_generation())
            else:
                raise ValueError(f"Tipo {tipo.get_type_for_generation()} inválido. Deve ser 'bool' ou 'range'.")
            leituras.append(LeituraSensor(
                sensor_id=sensor_id,
                data_leitura=data_leitura,
                valor=valor
            ))

        print(f"Geradas {len(leituras)} leituras para o sensor {sensor_id} entre {data_inicial} e {data_final}.")

        return leituras

