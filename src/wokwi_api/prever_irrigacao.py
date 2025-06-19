from src.database.models.fazenda import Plantio, Propriedade, Campo
from src.database.tipos_base.database import Database
from src.database.models.sensor import Sensor
from datetime import datetime, timedelta
from fastapi import APIRouter

from src.modelo_preditivo.realizar_previsao_func import realizar_previsao_modelo_padrao
from src.service.get_weather import obter_dados_clima
from src.wokwi_api.base.leitura_request import LeituraRequest

irrigar_router = APIRouter()

CIDADE_PADRAO = "São Paulo"

dados_ultima_leitura = None
data_ultima_leitura:datetime or None = None

@irrigar_router.post("/")
def prever_irrigacao(request: LeituraRequest):

    now = datetime.now()

    cidade = CIDADE_PADRAO

    with Database.get_session() as session:
        sensores = session.query(Sensor).filter(Sensor.cod_serial == request.serial).filter().all()

        if not sensores:
            return {
                "status": "error",
                "message": f"Sensor com serial '{request.serial}' não encontrado."
            }


        for sensor in sensores:
            if sensor.plantio_id:
                plantio = Plantio.get_from_id(sensor.plantio_id)
                campo = Campo.get_from_id(plantio.campo_id)
                propriedade = Propriedade.get_from_id(campo.propriedade_id)

                if propriedade.cidade is not None:
                    cidade = propriedade.cidade
                    break

    dados_climaticos = dados_ultima_leitura

    if dados_climaticos is not None and data_ultima_leitura is not None and (now - data_ultima_leitura) < timedelta(days=1):
        print("Usando dados da última leitura")
    else:
        dados_climaticos = obter_dados_clima(cidade)

    if dados_climaticos['chuva']:
        print("Chuva detectada, não irrigar")
        return {
            "status": "success",
            "irrigar": False,
        }

    irrigar = realizar_previsao_modelo_padrao(
        hora_leitura=now,
        fosforo=request.estado_fosforo,
        potassio=request.estado_potassio,
        umidade=request.umidade,
        ph=request.ph,
    )

    if irrigar == "Sim":
        print("Irrigar")
        return  {
            "status": "success",
            "irrigar": True,
        }
    else:
        print("Não irrigar")
        return {
            "status": "success",
            "irrigar": False,
        }
