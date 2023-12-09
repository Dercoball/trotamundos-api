from fastapi import FastAPI
from sqlalchemy import text
from database import engine
import pandas as pd  # Importa Pandas
from fastapi.middleware.cors import CORSMiddleware
from modelos import GetCliente, ResponseModel, SaveCliente, Vehiculo, GetOrden, GetVehiculo, SaveOrden, DatosLogin, Token, OrdenCompleta, Roles, Estatus
from fastapi.responses import JSONResponse
import json
from typing import List
from negocios import Negocios
from datetime import timedelta
from utils import utilsclass
ACCESS_TOKEN_EXPIRE_MINUTES = 480

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    path="/api/seguridad/iniciarsesion",
    name='Inicio de sesion',
    tags=['Seguridad'],
    description='Metodo para iniciar sesion',
    response_model=Token
)
async def login(payload: DatosLogin):
    _negocios = Negocios()
    user = await _negocios.getusuario(payload)
    # if not user:
    #     return JSONResponse(status_code=401, content={"Id_Resultado": 0, "Respuesta": "Datos de acceso incorrectos"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await utilsclass.create_access_token(
        # data={"sub": payload.usuario}, expires_delta=access_token_expires
        data={"sub": payload.usuario, "idUsuario": 1, "idRol": 1}, expires_delta=access_token_expires

    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get(
        path="/api/cliente",
        name='Obtener cliente',
        tags=['Cliente'],
        description='Método para obtener la informacion del cliente',
        response_model=GetCliente
)
def getcliente(idCliente = 0):
    return JSONResponse(status_code=200, content={
  "Facturar_a": "string",
  "Nombre": "string",
  "Calle": "string",
  "No_int": 0,
  "Colonia": "string",
  "Ciudad": "string",
  "Estado": "string",
  "Tel": "string",
  "Cel": "string",
  "Email": "string",
  "RFC": "string",
  "Autorizacion_ext": "string",
  "ID": idCliente
})


@app.post(
        path="/api/cliente",
        name='Guardar cliente',
        tags=['Cliente'],
        description='Método para guardar la informacion del cliente',
        response_model=ResponseModel
)
def getcliente(payload: SaveCliente ):
    dumpp = ResponseModel(id_resultado=1,respuesta="El cliente se guardo de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)


@app.get(
        path="/api/vehiculos",
        name='Obtener vehiculos',
        tags=['Vehiculo'],
        description='Método para obtener la informacion de los vehiculos del cliente',
        response_model=List[GetVehiculo]
)
def getvehiculos(idCliente = 0):
    pass


@app.get(
    path="/api/vehiculo",
        name='Obtener vehiculo',
        tags=['Vehiculo'],
        description='Método para obtener la informacion de un vehiculo',
        response_model=GetVehiculo
)
def getvehiculos(idVehiculo = 0):
    pass


@app.put(
        path="/api/vehiculo",
        name='Actualizar vehiculo',
        tags=['Vehiculo'],
        description='Método para actualizar la informacion de los vehiculos del cliente',
    response_model=ResponseModel
)
def updateVehiculo(payload: GetVehiculo):
    dumpp = ResponseModel(id_resultado=1,respuesta="Se actualizó la información del vehiculo de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.put(
        path="/api/cliente",
        name='Guardar cliente',
        tags=['Cliente'],
        description='Método para actualizar la informacion del cliente',
        response_model=ResponseModel
)
def getcliente(payload: GetCliente ):
    dumpp = ResponseModel(id_resultado=1,respuesta="El cliente se actualizo de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.post(
    path="/api/ordenserviciofull",
        name='Guardar orden',
        tags=['Orden'],
        description='Método para guardan la orden',
        response_model=ResponseModel
)
def saveorden(payload: OrdenCompleta):
    dumpp = ResponseModel(id_resultado=1,respuesta="Se guardo la orden")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.get(
        path="/api/roles",
        name='Obtener roles',
        tags=['Catalogos'],
        description='Método para obtener los roles',
        response_model=Roles
)
def obtener_roles():
    query = "SELECT * FROM Catalogos.Roles"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)

@app.get(
        path="/api/estatus",
        name='Obtener estatus',
        tags=['Catalogos'],
        description='Método para obtener los estatus',
    response_model=Estatus
)
def obtener_roles():
    query = "SELECT * FROM Catalogos.Estatus"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)

# @app.post(
#     path="/api/usuarios",
#     name='crear usuario',
#     tags=['Seguridad'],
#     description='Método para crear usuarios',
#     response_model=ResponseModel
# )
# def crearusuario()
if __name__ == '__main__':
    print(pyodbc.drivers())
    app.run()