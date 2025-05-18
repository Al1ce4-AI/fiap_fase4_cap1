from sqlalchemy import Sequence, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.service.get_weather import obter_dados_clima
from src.database.models.fazenda import Plantio
from src.database.models.unidade import Unidade
from src.database.models.sensor import LeituraSensor, Sensor, TipoSensor
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
        Sequence(f"{__tablename__}_SEQ_ID"),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    quantidade_total: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        unique=False,
        info={
            'label': 'Quantidade'
        },
        comment="Quantidade de irrigação aplicada"
    )

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
        ForeignKey('SENSOR.id'),
        nullable=False,
        info={
            'label': 'Sensor'
        },
        comment="ID do sensor associado"
    )

    sensor: Mapped[Sensor] = relationship('Sensor', back_populates='irrigacoes')

    @classmethod
    def decidir_irrigacao(cls, plantio_id: int) -> tuple[bool, dict]:
        """Lógica centralizada no modelo"""
        from src.database.tipos_base.database import Database
        with Database.get_session() as session:
            plantio = session.query(Plantio).get(plantio_id)
            sensores = {
                'umidade': cls._get_ultima_leitura(session, plantio_id, 'H'),
                'ph': cls._get_ultima_leitura(session, plantio_id, 'pH'),
                'clima': obter_dados_clima("São Paulo")
            }

            deve_irrigar = (
                sensores['umidade'] < 30 and
                not sensores.get('clima', {}).get('chuva') and
                5.5 <= sensores['ph'] <= 7.0
            )
            return deve_irrigar, sensores

    @staticmethod
    def _get_ultima_leitura(session, plantio_id: int, tipo_sensor: str) -> float:
        """Método auxiliar para leituras de sensores"""

        tipo_sensor_instance = session.query(TipoSensor).filter(
            TipoSensor.tipo == tipo_sensor
        ).first()


        sensor = session.query(Sensor).join(Sensor.tipo_sensor).filter(
            Sensor.plantio_id == plantio_id,
            Sensor.tipo_sensor_id == tipo_sensor_instance.id
        ).first()

        if sensor:
            leitura = session.query(LeituraSensor).filter(
                LeituraSensor.sensor_id == sensor.id
            ).order_by(LeituraSensor.data_leitura.desc()).first()
            return leitura.valor if leitura else 0.0
        return 0.0