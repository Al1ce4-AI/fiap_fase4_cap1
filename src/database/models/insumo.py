from sqlalchemy import Sequence, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database.models.compartilhado import TipoCultura, FormatoArea, UnidadesInsumo
from src.database.tipos_base.model import Model

class Insumo(Model):

    __tablename__ = 'INSUMO'

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do Insumo"
    )

    tipo: Mapped[TipoCultura] = mapped_column(
        Enum(TipoCultura, length=50),
        nullable=False,
        comment="Tipo de Cultura da Fazenda",
        info={
            'label': 'Tipo de Cultura'
        }
    )

    unidade: Mapped[UnidadesInsumo] = mapped_column(
        Enum(UnidadesInsumo, length=10),
        nullable=False,
        comment="Unidade de Medida do Insumo",
        info={
            'label': 'Unidade de Medida'
        }
    )

    consumo : Mapped[float] = mapped_column(
        nullable=False,
        comment="Consumo do Insumo por hectare",
        info={
            'label': 'Consumo por hectare'
        }
    )

    custo : Mapped[float] = mapped_column(
        nullable=False,
        comment="Custo do Insumo por unidade de medida",
        info={
            'label': 'Custo por unidade de medida'
        }
    )

    def custo_total(self, area: float) -> float:
        """
        Calcula o custo total do insumo com base na área e no consumo.
        :param area: Área em m2.
        :return: Custo total.
        """

        area_hectare = area / 10000  # Convertendo m² para hectares

        return self.consumo * area_hectare * self.custo
