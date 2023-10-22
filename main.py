from fastapi import FastAPI
from sqlalchemy import text
from database import engine
import pandas as pd  # Importa Pandas
from fastapi.middleware.cors import CORSMiddleware
from modelos import GetCliente, ResponseModel, SaveCliente
from fastapi.responses import JSONResponse
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# @app.get("/api/query/")
# def get_query_result():
#     query = text("SELECT * FROM tabla1")

#     # Ejecutar la consulta utilizando el motor de conexión
#     with engine.connect() as connection:
#         result = connection.execute(query)
#         rows = result.fetchall()

#     # Convierte los resultados en un DataFrame de Pandas
#     df = pd.DataFrame(rows, columns=result.keys())

#     # Convierte el DataFrame en una lista de diccionarios
#     result_list = df.to_dict(orient="records")

#     return result_list[0]

if __name__ == '__main__':
    app.run()