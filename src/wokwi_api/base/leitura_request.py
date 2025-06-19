from pydantic import BaseModel

class LeituraRequest(BaseModel):
    serial: str
    umidade: float or None
    ph: float or None
    estado_fosforo: int or None
    estado_potassio: int or None
    estado_api: int or None # não utilizado
    estado_irrigacao: int or None
