from sqlalchemy import Sequence, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.fazenda import Plantio
from src.database.models.unidade import Unidade
from src.database.tipos_base.model import Model
from datetime import datetime

class TipoSensor(Model):
    """Representa um tipo de sensor que pode ser utilizado em uma plantação."""

    __tablename__ = 'TIPO_SENSOR'

    @classmethod
    def display_name(cls) -> str:
        return "Tipo de Sensor"

    @classmethod
    def display_name_plural(cls) -> str:
        return "Tipos de Sensores"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
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
        comment="Ex.: ESP32, Arduino, Raspberry Pi"
    )

    sensors: Mapped[list['Sensor']] = relationship('Sensor', back_populates='tipo_sensor')

    def __str__(self):
        return f"{self.id} - {self.nome}"

class Sensor(Model):
    """Representa um sensor que pode ser utilizado em uma plantação."""

    __tablename__ = 'SENSOR'

    @classmethod
    def display_name_plural(cls) -> str:
        return "Sensores"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
        primary_key=True,
        autoincrement=True,
        nullable=False
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

    def __str__(self):
        return f"{self.id} - {self.nome}"

class LeituraSensor(Model):
    """Representa uma leitura de um sensor em um determinado momento."""

    __tablename__ = 'LEITURA_SENSOR'

    @classmethod
    def display_name(cls) -> str:
        return "Leitura de Sensor"

    @classmethod
    def display_name_plural(cls) -> str:
        return "Leituras de Sensores"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
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

    plantio_id: Mapped[int] = mapped_column(
        ForeignKey('PLANTIO.id'),
        nullable=False,
        info={
            'label': 'Plantio'
        },
        comment="ID do plantio associado"
    )

    plantio: Mapped[Plantio] = relationship('Plantio', back_populates='leituras_sensores')

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