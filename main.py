from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from sqlalchemy import text
from database import engine
import pandas as pd  # Importa Pandas
from fastapi.middleware.cors import CORSMiddleware
from modelos import GetCliente, ResponseModel, SaveCliente, Vehiculo, GetOrden, GetVehiculo, SaveOrden, DatosLogin, Token, OrdenCompleta, Roles, Estatus, SaveUsuario, saveVehiculo, ImageData
from fastapi.responses import JSONResponse
import json
from typing import List
from negocios import Negocios
from datetime import timedelta
from utils import utilsclass
import os
import pdfkit
import base64
from PIL import Image
from io import BytesIO

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
options = {
    'page-size': 'A4',
    'margin-top': '1cm',
    'margin-right': '1cm',
    'margin-bottom': '1cm',
    'margin-left': '1cm',
}

@app.post(
    path="/api/seguridad/iniciarsesion",
    name='Inicio de sesion}',
    tags=['Seguridad'],
    description='Metodo para iniciar sesion}',
    response_model=Token
)
async def login(payload: DatosLogin):
    _negocios = Negocios()
    user = await _negocios.getusuario(payload)
    if not user:
        return JSONResponse(status_code=401, content={"Id_Resultado": 0, "Respuesta": "Datos de acceso incorrectos"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await utilsclass.create_access_token(
        # data={"sub": payload.d.usuario}, expires_delta=access_token_expires
        data={"sub": payload.usuario, "idUsuario": 1, "idRol": 1}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# app.get(
#         path="/api/cliente",
#         name='Obtener clien',
#         tags=['Cliente'],
#         description='Método para obtener la informacion de un cliente',
#         response_model=GetCliente
# )
# def getcliente(IdCliente = int):
#     query = f"exec Clientes.clienteinsupdel @Accion = 4,@IdCliente ={IdCliente}"
#     roles_df = pd.read_sql(query, engine)
#     resultado = roles_df.to_dict(orient="records")
#     return JSONResponse(status_code=200,content=resultado)
# @app.get(
#         path="/api/clientes",
#         name='Obtener clientes',
#         tags=['Cliente'],
#         description='Método para obtener la informacion del cliente',
#         response_model=List[GetCliente]
# )
# def getclientes(busqueda = ""):
#     query = f"exec Clientes.clienteinsupdel @Accion = 2,@ParametroBusqueda = '{busqueda}' "
#     roles_df = pd.read_sql(query, engine)
#     resultado = roles_df.to_dict(orient="records")
#     return JSONResponse(status_code=200,content=resultado)

@app.get(
        path="/api/cliente",
        name='Obtener cliente',
        tags=['Cliente'],
        description='Método para obtener la informacion de un cliente',
        response_model=List[GetCliente]
)
def getcliente(idCliente = 0):
    query = f"exec Clientes.clienteinsupdel @Accion = 4,@IdCliente ={idCliente}"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    resultado = resultado[0]
    return JSONResponse(status_code=200,content=resultado)

@app.get(
        path="/api/clientes",
        name='Obtener clientes',
        tags=['Cliente'],
        description='Método para obtener la informacion de todos los clientes',
        response_model=List[GetCliente]
)
def getclientes(busqueda = ""):
    query = f"exec Clientes.clienteinsupdel @Accion = 2,@ParametroBusqueda = '{busqueda}' "
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)


@app.post(
        path="/api/cliente",
        name='Guardar cliente',
        tags=['Cliente'],
        description='Método para guardar la informacion del cliente}',
        response_model=ResponseModel
)
def saveCliente(payload: SaveCliente ):
    query = f"EXEC clientes.clienteinsupdel \
    @Nombre='{payload.Nombre}', \
    @Calle='{payload.Calle}',  \
    @Colonia='{payload.Colonia}', \
    @Ciudad='{payload.Ciudad}', \
    @Estado='{payload.Estado}', \
    @Tel='{payload.Tel}', \
    @Cel='{payload.Cel}', \
    @Email='{payload.Email}', \
    @RFC='{payload.RFC}', \
    @Autorizacion_ext='{payload.Autorizacion_ext}', \
    @No_int='{payload.No_int}', \
    @Facturar_a='{payload.Facturar_a}', \
    @IdUsuarioEmpleado='{payload.Id_empleado}', @Accion = 1" 
    print(query)

    with engine.begin() as conn:
        conn.execution_options(autocommit = True)
        roles_df = pd.read_sql(query, conn)
    dumpp = ResponseModel(id_resultado=1,respuesta="El cliente se guardo de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)


@app.get(
        path="/api/vehiculo",
        name='Obtener vehiculo',
        tags=['Vehiculo'],
        description='Método para obtener la informacion de todos los vehiculos',
        response_model=List[GetVehiculo]
)
def getvehiculos(idVehiculo = 0):
    query = f"exec [dbo].[ObtenerVehiculo] @IdVehiculo = {idVehiculo}"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado[0])


@app.get(
    path="/api/vehiculos",
        name='Obtener vehiculos',
        tags=['Vehiculo'],
        description='Método para obtener la informacion de un vehiculo',
        response_model=GetVehiculo
)
def getvehiculos(parametro = ""):
    query = f"exec [dbo].[ObtenerVehiculo] @ParametroBusqueda = '{parametro}'"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)

@app.post(
        path="/api/vehiculo",
        name='Guarda vehiculo',
        tags=['Vehiculo'],
        description='Método para guardar la informacion de los vehiculos del cliente}',
    response_model=ResponseModel
)
def guardarVehiculo(payload: saveVehiculo):
    try: 
        
        query = f"exec dbo.InsertarVehiculo @Id_Cliente = {payload.IdCliente}, @Id_Empleado = {payload.Id_empleado},@Marca = '{payload.Marca}' \
        ,@Modelo = '{payload.Modelo}', @Color = '{payload.Color}', @No_serie ='{payload.No_serie}',@Placa = '{payload.Placa}',@Tipo = '{payload.Tipo}' \
        ,@Motor = '{payload.Motor}', @Kms = '{payload.Kms}', @Espejo_retrovisor = {payload.Espejo_retrovisor},@Espejo_izquierdo = {payload.Espejo_izquierdo}, \
        @Antena			   = {payload.Antena}, \
        @Tapones_ruedas	   = {payload.Tapones_ruedas}, \
        @Radio		   = {payload.Radio}, \
        @Encendedor		   = {payload.Encendedor}, \
        @Gato			   = {payload.Gato}, \
        @Herramienta   = {payload.Herramienta}, \
        @Llanta_refaccion  ={payload.Llanta_refaccion}, \
        @Limpiadores	   ={payload.Limpiadores}, \
        @Pintura_rayada	   ={payload.Pintura_rayada}, \
        @Cristales_rotos   ={payload.Cristales_rotos}, \
        @Golpes		={payload.Golpes}, \
        @Tapetes	={payload.Tapetes}, \
        @Extintor	={payload.Extintor}, \
        @Tapones_gasolina  ={payload.Tapones_gasolina}, \
        @Calaveras_rotas   ={payload.Calaveras_rotas}, \
        @Molduras_completas ={payload.Molduras_completas}, \
        @Espejo_retrovisor_foto	 = '{payload.Espejo_retrovisor_foto}',\
        @Espejo_izquierdo_foto 	 = '{payload.Espejo_izquierdo_foto}',\
        @Antena_foto			 = '{payload.Antena_foto}',\
        @Tapones_ruedas_foto	 = '{payload.Tapones_ruedas_foto}',\
        @Radio_foto				 = '{payload.Radio_foto}',\
        @Encendedor_foto		 = '{payload.Encendedor_foto}',\
        @Gato_foto				 = '{payload.Gato_foto}',\
        @Herramienta_foto		 = '{payload.Herramienta_foto}',\
        @Llanta_refaccion_foto	 = '{payload.Llanta_refaccion_foto}',\
        @Limpiadores_foto		 = '{payload.Limpiadores_foto}',\
        @Pintura_rayada_foto	 = '{payload.Pintura_rayada_foto}',\
        @Cristales_rotos_foto	 = '{payload.Cristales_rotos_foto}',\
        @Golpes_foto			 = '{payload.Golpes_foto}',\
        @Tapetes_foto			 = '{payload.Tapetes_foto}',\
        @Extintor_foto			 = '{payload.Extintor_foto}',\
        @Tapones_gasolina_foto	 = '{payload.Tapones_ruedas_foto}',\
        @Calaveras_rotas_foto	 = '{payload.Calaveras_rotas_foto}',\
        @Molduras_completas_foto = '{payload.Molduras_completas_foto}'"
        print(query)
        with engine.begin() as conn:
            conn.execution_options(autocommit = True)
            roles_df = pd.read_sql(query, conn)
        dumpp = ResponseModel(id_resultado=1,respuesta="Se guardó la información del vehiculo de manera correcta")
        dict = dumpp.model_dump()
        return JSONResponse(status_code=200, content=dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put(
        path="/api/vehiculo",
        name='Actualizar vehiculo',
        tags=['Vehiculo'],
        description='Método para actualizar la informacion de los vehiculos del cliente}',
    response_model=ResponseModel
)
def updateVehiculo(payload: GetVehiculo):
    dumpp = ResponseModel(id_resultado=1,respuesta="Se actualizó la información del vehiculo de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.put(
        path="/api/cliente",
        name='Actualizar cliente',
        tags=['Cliente'],
        description='Método para actualizar la informacion del cliente}',
        response_model=ResponseModel
)
def putcliente(payload: GetCliente ):
    query = f"exec [Clientes].[clienteinsupdel] @Accion = 3, @idCliente = {payload.ID}, @Nombre = '{payload.Nombre}', @Calle = '{payload.Calle}' \
        ,@Colonia = '{payload.Colonia}', @Ciudad = '{payload.Ciudad}',  @Estado = '{payload.Estado}', @Tel = '{payload.Tel}', @Cel = '{payload.Cel}' \
        ,@Email = '{payload.Email}', @RFC = '{payload.RFC}', @Autorizacion_ext = '{payload.Autorizacion_ext}', @No_int = '{payload.No_int}',@Facturar_a = '{payload.Facturar_a}' \
        ,@IdUsuarioEmpleado = '{payload.Id_empleado}'"
    with engine.begin() as conn:
        conn.execution_options(autocommit = True)
        roles_df = pd.read_sql(query, conn)
    dumpp = ResponseModel(id_resultado=1,respuesta="El cliente se actualizo de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.post(
    path="/api/ordenserviciofull",
        name='Guardar orden}',
        tags=['Orden'],
        description='Método para guardan la orden}',
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
        description='Método para obtener los roles}',
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
        description='Método para obtener los estatus}',
    response_model=Estatus
)
def obtener_roles():
    query = "SELECT * FROM Catalogos.Estatus"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)

@app.post(
    path="/api/usuarios",
    name='crear usuario',
    tags=['Seguridad'],
    description='Método para crear usuarios',
    response_model=ResponseModel
)
async def crearusuario(payload: SaveUsuario):
    passhash = await utilsclass.get_password_hash(payload.Password)
    query = f"exec Seguridad.usuariosinsupdel @Nombre = '{payload.Nombre}', @Password = '{passhash}', @Rol = {payload.Rol}, @Estatus = {payload.Estatus}, @Accion = 1"
    with engine.begin() as conn:
        conn.execution_options(autocommit = True)
        roles_df = pd.read_sql(query, conn)
    dumpp = ResponseModel(id_resultado=1,respuesta="Se agregó el usuario de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.get(
    path="/api/ordenserviciopdf",
    name='obtener pdf de la orden de servicio',
    tags=['Orden'],
    description='Método para obtener el pdf de la orden de servicio',
    response_model=ResponseModel
)
def convert_html_to_pdf():
    query = f"exec [Clientes].[ordendeservicio]"
    with engine.begin() as conn:
        conn.execution_options(autocommit = True)
        roles_df = pd.read_sql(query, conn)
    resultado = roles_df.to_dict(orient="records")
    htmlstring = resultado[0]["Tabla"]
    img = "\\img1.jpg"
    pdf_path = "example.pdf"
    # pdfkit.from_string('Hello!', 'out.pdf')
    path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path)    
    pdfkit.from_string(htmlstring, 'out.pdf', configuration=config)
    # with open(pdf_path, "wb") as pdf_file:
    #     pisa_status = pisa.CreatePDF(htmlstring, dest=pdf_file, options=options)
    # pdf_filepath = os.path.join('./',pdf_path, )
    return JSONResponse(status_code=200,content=resultado)

# @app.post(
#     path="/api/images",
#     name="guardar imagen",
#     tags=['Image'],
#     description='Método para guardar imagenes',
#     response_model=ResponseModel
# )
# async def guardar_imagen(
#     archivo: List[UploadFile] = File(...),
#     idCliente: int = Form(...),
#     idVehiculo: int = Form(...),
#     idCheckVehiculo: List[str] = Form(...)
# ):
#     try:
#         results = []
#         resultado = []
#         for i, file in enumerate(archivo):
#             contents = await file.read()
#             image = Image.open(BytesIO(contents))
#             first_element = idCheckVehiculo[0] 
#             buffered = BytesIO()
#             image.save(buffered, format="JPEG")
#             img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
#             id_cliente = idCliente
#             id_vehiculo = idVehiculo
#             values = first_element.split(',')
#             id_check_vehiculo = values[i]
#             query = f"exec GuardaImagen @Imagen = '{img_str}'"
#             with engine.begin() as conn:
#                 conn.execution_options(autocommit = True)
#                 roles_df = pd.read_sql(query, conn)
#             resultado = roles_df.to_dict(orient="records")
#             base64_image = resultado[0]["Imagen"]
#             results.append({
#                 "idCliente": id_cliente,
#                 "idVehiculo": id_vehiculo,
#                 "idCheck": id_check_vehiculo,
#                 "imagen": base64_image
                
#             })
#         return JSONResponse(status_code=200, content=results)
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Imprimir el error para depuración
#         raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == '__main__':
    app.run()