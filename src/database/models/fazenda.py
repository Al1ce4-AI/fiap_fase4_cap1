from sqlalchemy import Sequence, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database.models.compartilhado import TipoCultura, FormatoArea
from src.database.tipos_base.model import Model

class Fazenda(Model):

    __tablename__ = 'FAZENDA'

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome da Fazenda"
    )

    tipo: Mapped[TipoCultura] = mapped_column(
        Enum(TipoCultura, length=50),
        nullable=False,
        comment="Tipo de Cultura da Fazenda",
        info = {
            'label': 'Tipo de Cultura'
        }
    )

    formato: Mapped[FormatoArea] = mapped_column(
        Enum(FormatoArea, length=15),
        nullable=False,
        comment="Formato da Área da Fazenda"
    )

    base: Mapped[float] = mapped_column(
        nullable=False,
        comment="Base da Fazenda (m²)",
        info = {
            'label': 'Base (m²)'
        }
    )

    altura: Mapped[float] = mapped_column(
        nullable=False,
        comment="Altura da Fazenda (m²)",
        info = {
            'label': 'Altura (m²)'
        }
    )

    def area(self) -> float:
        """
        Calcula a área da fazenda com base no formato e nas dimensões fornecidas.
        :return: Área da fazenda em m².
        """
        if self.formato == FormatoArea.RETANGULO:
            return self.base * self.altura
        elif self.formato == FormatoArea.TRIANGULO:
            return (self.base * self.altura) / 2
        else:
            raise ValueError("Formato desconhecido")
