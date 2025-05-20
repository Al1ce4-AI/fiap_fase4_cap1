from sqlalchemy import Sequence, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.tipos_base.database import Database
from src.service.get_weather import obter_dados_clima
from src.database.models.fazenda import Plantio
from src.database.models.sensor import LeituraSensor, Sensor, TipoSensor
from src.database.tipos_base.model import Model
from datetime import datetime
import logging


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
    def decidir_irrigacao(cls, plantio_id: int, cidade: str) -> tuple[bool, dict]:        
        with Database.get_session() as session:
            try:
                plantio = session.query(Plantio).get(plantio_id)
                if not plantio:
                    return False, {'erro': 'Plantio não encontrado'}

                try:
                    umidade = cls._get_ultima_leitura(session, plantio_id, 'H')
                except Exception as umidade_error:
                    umidade = 100
                    logging.warning(f"Falha ao obter umidade: {str(umidade_error)}")

                try:
                    ph = cls._get_ultima_leitura(session, plantio_id, 'pH')
                except Exception as ph_error:
                    ph = 7.0 
                    logging.warning(f"Falha ao obter pH: {str(ph_error)}")

                try:
                    clima = obter_dados_clima(cidade)
                except Exception as clima_error:
                    clima = {'chuva': True}
                    logging.warning(f"Falha ao obter clima: {str(clima_error)}")

                deve_irrigar = (
                    (umidade < 30 or
                    5.5 <= ph <= 7.0) and
                    not clima.get('chuva', True)

                )
                
                return deve_irrigar, {
                    'umidade': umidade,
                    'ph': ph,
                    'clima': clima
                }

            except Exception as main_error:
                logging.error(f"Erro geral na decisão de irrigação: {str(main_error)}")
                return False, {
                    'erro': str(main_error),
                    'umidade': 100,
                    'ph': 7.0,
                    'clima': {'chuva': True}
                }

    @staticmethod
    def _get_ultima_leitura(session, plantio_id: int, tipo_sensor: str) -> float:
        try:
            tipo = session.query(TipoSensor).filter(
                TipoSensor.tipo == tipo_sensor
            ).one()

            sensor = session.query(Sensor).filter(
                Sensor.plantio_id == plantio_id,
                Sensor.tipo_sensor_id == tipo.id
            ).first()

            if not sensor:
                raise ValueError(f"Nenhum sensor {tipo_sensor} cadastrado para este plantio")

            leitura = session.query(LeituraSensor).filter(
                LeituraSensor.sensor_id == sensor.id,
                LeituraSensor.valor.isnot(None)
            ).order_by(LeituraSensor.data_leitura.desc()).first()

            if not leitura:
                raise ValueError(f"Nenhuma leitura registrada para sensor {sensor.nome}")

            return float(leitura.valor)

        except Exception as e:
            logging.error(f"Erro ao obter leitura {tipo_sensor}: {str(e)}")
            raise