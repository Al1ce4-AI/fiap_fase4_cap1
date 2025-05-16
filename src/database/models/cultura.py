from sqlalchemy import Sequence, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.tipos_base.model import Model

class Cultura(Model):
    """A cultura que será plantada em um campo."""

    __tablename__ = 'CULTURA'
    __menu_group__ = "Fazenda"
    __menu_order__ = 3

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
        comment="Nome da Cultura"
    )

    observacao: Mapped[str] = mapped_column(
        Text(1000),
        nullable=True,
        unique=False,
        info={
            'label': 'Observação'
        }
    )

    plantios = relationship('Plantio', back_populates='cultura')

    def __str__(self):
        return f"{self.id} - {self.nome}"

