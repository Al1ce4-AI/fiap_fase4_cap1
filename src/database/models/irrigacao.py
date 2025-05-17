from sqlalchemy import Sequence, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.fazenda import Plantio
from src.database.models.unidade import Unidade
from src.database.models.sensor import Sensor
from src.database.tipos_base.model import Model
from datetime import datetime

class Irrigacao(Model):
    """Representa uma irrigação que pode ser utilizada em uma plantação."""

    __tablename__ = 'IRRIGACAO'

    @classmethod
    def display_name(cls) -> str:
        return "Irrigação"

    @classmethod
    def display_name_plural(cls) -> str:
        return "Irrigações"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    #plantio_id : Mapped[int] = mapped_column(
    #    ForeignKey('PLANTIO.id'),
    #    nullable=False,
    #    info={
    #        'label': 'Plantio'
    #    },
    #    comment="ID do plantio associado"
    #)

    #plantio: Mapped[Plantio] = relationship('Plantio', back_populates='irrigacoes')

    #unidade_id: Mapped[int] = mapped_column(
    #    ForeignKey('UNIDADE.id'),
    #    nullable=True,
    #    info={
    #        'label': 'Unidade'
    #    },
    #    comment="ID da unidade associada"
    #)

    #unidade: Mapped[Unidade] = relationship('Unidade', back_populates='irrigacoes')

    quantidade_total: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        unique=False,
        info={
            'label': 'Quantidade'
        },
        comment="Quantidade de irrigação aplicada"
    )

    #data_inicio : Mapped[datetime] = mapped_column(
    #    DateTime,
    #    nullable=False,
    #    info={
    #        'label': 'Data de Início'
    #    },
    #    comment="Data de início da irrigação"
    #)

    data_hora : Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        info={
            'label': 'Data e Hora que o sensor foi ativado'
        },
        comment="Data de fim da irrigação"
    )

    observacao: Mapped[str] = mapped_column(
        Text(1000),
        nullable=True,
        unique=False,
        info={
            'label': 'Observação'
        },
        comment="Observação sobre a irrigação"
    )

    sensor_id : Mapped[int] = mapped_column(
        #ForeignKey('SENSOR.id'),
        nullable=False,
        info={
            'label': 'Sensor'
        },
        comment="ID do sensor associado"
    )

    #sensor: Mapped[Plantio] = relationship('Sensor', back_populates='irrigacoes')