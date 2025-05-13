from sqlalchemy import Sequence, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.tipos_base.model import Model
from datetime import datetime

class Nutriente(Model):
    """Representa um nutriente que pode ser aplicado em uma cultura."""

    __tablename__ = 'NUTRIENTE'

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
        comment="Nome do nutriente"
    )

    observacao: Mapped[str] = mapped_column(
        Text(1000),
        nullable=True,
        unique=False,
        info={
            'label': 'Observação'
        }
    )

class AplicacaoNutriente:
    """
    Representa a aplicação de um nutriente em um plantio.
    """

    __tablename__ = 'APLICACAO_NUTRIENTE'

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    plantio_id: Mapped[int] = mapped_column(
        ForeignKey('PLANTIO.id'),
        nullable=False,
        info={
            'label': 'Plantio'
        },
        comment="ID do plantio associado"
    )

    plantio: Mapped['Plantio'] = relationship('Plantio', back_populates='aplicacoes_nutrientes')

    nutriente_id: Mapped[int] = mapped_column(
        ForeignKey('NUTRIENTE.id'),
        nullable=False,
        info={
            'label': 'Nutriente'
        },
        comment="ID do nutriente associado"
    )

    nutriente: Mapped['Nutriente'] = relationship('Nutriente', back_populates='aplicacoes_nutrientes')

    unidade_id : Mapped[int] = mapped_column(
        ForeignKey('UNIDADE.id'),
        nullable=False,
        info={
            'label': 'Unidade'
        },
        comment="ID da unidade de medida associada"
    )

    data_aplicacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        info={
            'label': 'Data da Aplicação'
        }
    )

    quantidade: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        info={
            'label': 'Quantidade'
        },
        comment="Quantidade de nutriente aplicada"
    )

    observacao: Mapped[str] = mapped_column(
        Text(1000),
        nullable=True,
        unique=False,
        info={
            'label': 'Observação'
        }
    )

