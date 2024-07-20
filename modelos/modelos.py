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
    Id_empleado: int

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
    Id_empleado: int
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

class saveVehiculo(Vehiculo):
    IdCliente: int
    
class GetVehiculo(Vehiculo):
    ID : int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
class DatosLogin(BaseModel):
    usuario: str = Field(
        ...,
        min_length=1
    )
    contrasena: str = Field(
        ...,
        min_length=1
    )

class OrdenCompleta(Vehiculo, SaveOrden, SaveCliente):
    Id_empleado: int

class Roles(BaseModel):
    Id_Rol: int
    Descripcion: str
    Estatus: int

class Estatus(BaseModel):
    Id_Estatus: int
    Descripcion: str

class SaveUsuario(BaseModel):
    Nombre: str
    Password: str
    Rol: int
    Estatus: int

class OrdenServicio(BaseModel):
	IdOrden:int


class SaveOrdenServicio(OrdenServicio):
    Nombre:str
Calle:str
Colonia:str
Ciudad:str
Estado:str
Tel:str
Cel:str
Email:str
RFC:str
Autorizacion_ext:str
No_int:str
Usuario:str
Facturar_a:str
Marca:str
Modelo:str
Color:str
No_serie:str
Placa:str
Tipo:str
Motor:str
Kms:str
Espejo_retrovisor:str
Espejo_izquierdo:str
Antena:str
Tapones_ruedas:str
Radio:str
Encendedor:str
Gato:str
Herramienta:str
Llanta_refaccion:str
Limpiadores:str
Pintura_rayada:str
Cristales_rotos:str
Golpes:str
Tapetes:str
Extintor:str
Tapones_gasolina:str
Calaveras_rotas:str
Molduras_completas:str