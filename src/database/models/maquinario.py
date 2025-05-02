from sqlalchemy import Sequence, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.models.compartilhado import FormatoArea, UnidadesInsumo
from src.database.models.fazenda import Fazenda
from src.database.tipos_base.model import Model
import matplotlib.pyplot as plt
from datetime import datetime
from src.settings import EXPORTS_DIR
import logging


class Maquinario(Model):

    @classmethod
    def display_name(cls) -> str:
        return "Maquinário"

    __tablename__ = "MAQUINARIO"

    id: Mapped[int] = mapped_column(
        Sequence(f"{__tablename__}_seq_id"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do Maquinário"
    )

    largura: Mapped[float] = mapped_column(
        nullable=False,
        comment="Largura do Maquinário (m)",
        info={
            'label': 'Largura (m)',
        }
    )

    profundidade: Mapped[float] = mapped_column(
        nullable=False,
        comment="Profundidade do Maquinário (m)",
        info={
            'label': 'Profundidade (m)',
        }
    )

    velocidade_maxima: Mapped[float] = mapped_column(
        nullable=False,
        comment="Velocidade Máxima do Maquinário (km/h)",
        info={
            'label': 'Velocidade Máx. (km/h)',
        }
    )

    consumo: Mapped[float] = mapped_column(
        nullable=False,
        comment="Consumo de combustível (km/l)",
        info={
            'label': 'Consumo (km/l)',
        }
    )

    def _calcular_rota_retangulo(self, largura: float, altura: float, largura_carro: float) -> list[tuple]:
        """Calcula a rota mais curta para cobrir um retângulo."""
        rota = []
        y = 0
        sentido = 1  # 1 para direita, -1 para esquerda

        while y < altura:
            if sentido == 1:
                rota.append((0, y))
                rota.append((largura, y))
            else:
                rota.append((largura, y))
                rota.append((0, y))

            y += largura_carro
            sentido *= -1  # Inverte o sentido

        return rota

    def _calcular_rota_triangulo(self, base: float, altura: float, largura_carro: float) -> list[tuple]:
        """Calcula a rota mais curta para cobrir um triângulo."""
        rota = []
        y = 0
        sentido = 1  # 1 para direita, -1 para esquerda

        while y < altura:
            largura_atual = (base / altura) * (altura - y)  # Largura do triângulo na altura atual
            if sentido == 1:
                rota.append((0, y))
                rota.append((largura_atual, y))
            else:
                rota.append((largura_atual, y))
                rota.append((0, y))

            y += largura_carro
            sentido *= -1  # Inverte o sentido

        return rota

    def calcular_rota(self, fazenda:Fazenda):

        if fazenda.formato == FormatoArea.TRIANGULO:
            return self._calcular_rota_triangulo(fazenda.base, fazenda.altura, self.largura)
        elif fazenda.formato == FormatoArea.RETANGULO:
            return self._calcular_rota_retangulo(fazenda.base, fazenda.altura, self.largura)
        else:
            raise NotImplementedError(f"Formato {fazenda.formato.name} não implementado")

    def calcular_e_salvar_rota(self, fazenda:Fazenda):
        """Calcula a rota e salva a imagem."""
        rota = self.calcular_rota(fazenda)
        self.desenhar_rota(rota, titulo=f"Rota {self.nome} - {fazenda.nome}")
        return rota

    def calcular_distancia(self, rota: list[tuple]) -> float:
        """Calcula a distância total percorrida com base na rota."""
        distancia_total = 0.0
        for i in range(1, len(rota)):
            x1, y1 = rota[i - 1]
            x2, y2 = rota[i]
            distancia_total += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 1/2
        return distancia_total

    def calcular_consumo(self, distancia: float, consumo_por_km: float) -> float:
        """Calcula o consumo de combustível com base na distância e eficiência."""
        if consumo_por_km <= 0:
            raise ValueError("O consumo por km deve ser maior que zero.")
        return distancia / consumo_por_km

    @staticmethod
    def desenhar_rota(rota, titulo="Rota"):
        """Desenha a rota em um gráfico."""
        x, y = zip(*rota)  # Separa as coordenadas x e y

        plt.figure(figsize=(8, 8))
        plt.plot(x, y, marker='o', linestyle='-', color='blue')  # Desenha a rota
        plt.title(titulo)
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.grid(True)
        now = datetime.now()

        filename = f"{EXPORTS_DIR}/{titulo}_{now.strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        plt.close()

        logging.info(f"Rota salva no arquivo: {filename}")

