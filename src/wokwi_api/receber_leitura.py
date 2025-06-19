from src.database.tipos_base.database import Database
from src.database.models.sensor import Sensor, TipoSensor, TipoSensorEnum, LeituraSensor
from datetime import datetime
from fastapi import APIRouter

from src.wokwi_api.base.leitura_request import LeituraRequest

receber_router = APIRouter()

@receber_router.post("/")
def receber_leitura(request: LeituraRequest):

    print(f"Recebendo leitura para o sensor com serial: {request.serial}", request)

    now = datetime.now()

    with Database.get_session() as session:
        sensores = session.query(Sensor).filter(Sensor.cod_serial == request.serial).filter().all()

        if not sensores:
            return {
                "status": "error",
                "message": f"Sensor com serial '{request.serial}' não encontrado."
            }

        for sensor in sensores:

            tipo = session.query(TipoSensor).filter(TipoSensor.id == sensor.tipo_sensor_id).first()

            if not tipo:
                return {
                    "status": "error",
                    "message": f"Tipo de sensor para o sensor com serial '{request.serial}' não encontrado."
                }

            if tipo.tipo == TipoSensorEnum.UMIDADE and request.umidade is not None:
                nova_leitura = LeituraSensor(
                    sensor_id=sensor.id,
                    data_leitura=now,
                    valor= request.umidade
                )
            elif tipo.tipo == TipoSensorEnum.PH and request.ph is not None:
                nova_leitura = LeituraSensor(
                    sensor_id=sensor.id,
                    data_leitura=now,
                    valor=request.ph
                )
            elif tipo.tipo == TipoSensorEnum.POTASSIO and request.estado_potassio is not None:
                nova_leitura = LeituraSensor(
                    sensor_id=sensor.id,
                    data_leitura=now,
                    valor=request.estado_potassio
                )
            elif tipo.tipo == TipoSensorEnum.FOSFORO and request.estado_fosforo is not None:
                nova_leitura = LeituraSensor(
                    sensor_id=sensor.id,
                    data_leitura=now,
                    valor=request.estado_fosforo
                )
            elif tipo.tipo == TipoSensorEnum.RELE and request.estado_irrigacao is not None:
                nova_leitura = LeituraSensor(
                    sensor_id=sensor.id,
                    data_leitura=now,
                    valor=request.estado_irrigacao
                )
            else:
                continue
            session.add(nova_leitura)
            print('Nova leitura salva:', nova_leitura)

        session.commit()


    return {
        "status": "success",
        "message": "Leitura recebida com sucesso",
    }
