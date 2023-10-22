from typing import Optional
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    id_resultado : int
    respuesta : str

class SaveCliente(BaseModel):
    Facturar_a : str
    Nombre : str
    Calle : str
    No_int : int
    Colonia : str
    Ciudad : str
    Estado : str
    Tel : str
    Cel : str
    Email : str
    RFC : str
    Autorizacion_ext : str

class GetCliente(SaveCliente):
    ID : int

class SaveOrden(BaseModel):
    ID : int
    No_orden : int
    Fecha_recepcion : str
    Fecha_entrega : str
    Hora_de_compromiso : str
    Hora_de_entrega : str
    Motivo_de_visita : str
    Medio : str

class GetOrden(SaveOrden):
    ID : int

class Vehiculo(BaseModel):
    Marca : str
    Modelo : str
    Color : str
    No_serie : str
    Placa : str
    Tipo : str
    Motor : str
    Kms : str
    Espejo_retrovisor : int
    Espejo_izquierdo : int
    Espejo_derecho : int
    Antena : int
    Tapones_ruedas : int
    Radio : int
    Encendedor : int
    Gato : int
    Herramienta : int
    Llanta_refaccion : int
    Limpiadores : int
    Pintura_rayada : int
    Cristales_rotos : int
    Golpes : int
    Tapetes : int
    Extintor : int
    Tapones_gasolina : int
    Calaveras_rotas : int
    Molduras_completas : int

class GetVehiculo(Vehiculo):
    ID : int