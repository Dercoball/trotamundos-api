from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from sqlalchemy import text
from database import engine
import pandas as pd  # Importa Pandas
from fastapi.middleware.cors import CORSMiddleware
from modelos import GetCliente, ResponseModel, SaveCliente, Vehiculo, GetOrden, GetVehiculo, SaveOrden, DatosLogin, Token, OrdenCompleta, Roles, Estatus, SaveUsuario, saveVehiculo, ImageData, Empleado, Checklist
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

@app.post(
    path="/api/ordenserviciopdf",
    name='obtener pdf de la orden de servicio',
    tags=['Orden'],
    description='Método para obtener el pdf de la orden de servicio',
    response_model=ResponseModel
)
def convert_html_to_pdf(clienteId: int):
    try:
        query = f"exec [Clientes].[ordendeservicio]  @idCliente = {clienteId}"
        with engine.begin() as conn:
            conn.execution_options(autocommit=True)
            roles_df = pd.read_sql(query, conn)

        # Asegúrate de que hay al menos dos filas en el DataFrame
        
            # Accede al valor en la segunda fila de la columna 'Nombre'
            

            # Construye el HTML con el valor obtenido
        orden = roles_df['idOrden'].iloc[0]
        nombre = roles_df['Nombre'].iloc[0]
        calle =roles_df['Calle'].iloc[0]
        factura =roles_df['Facturar_a'].iloc[0]
        noint = roles_df['No_int'].iloc[0]
        colonia = roles_df['Colonia'].iloc[0]
        ciuadad = roles_df['Ciudad'].iloc[0]
        estado = roles_df['Estado'].iloc[0]
        tel = roles_df['Tel'].iloc[0]
        cel = roles_df['Cel'].iloc[0]
        email = roles_df['Email'].iloc[0]
        rfc = roles_df['RFC'].iloc[0]
        autorizacion = roles_df['Autorizacion_ext'].iloc[0]
        marca = roles_df['Marca'].iloc[0]
        tipo = roles_df['Tipo'].iloc[0] 
        modelo = roles_df['Modelo'].iloc[0]
        motor = roles_df['Motor'].iloc[0]
        color = roles_df['Color'].iloc[0]
        kms = roles_df['kms'].iloc[0]
        noserie = roles_df['No_Serie'].iloc[0]
        placa = roles_df['Placa'].iloc[0]
        espejoretrovisor = roles_df['Espejo_retrovisor'].iloc[0]
        espejoizq = roles_df['Espejo_izquierdo'].iloc[0]
        antena = roles_df['Antena'].iloc[0]
        taponesruedas = roles_df['Tapones_ruedas'].iloc[0]
        radio = roles_df['Radio'].iloc[0]
        encendedor = roles_df['Encendedor'].iloc[0]
        gato = roles_df['Gato'].iloc[0]
        herramienta = roles_df['Herramienta'].iloc[0]
        llanarefaccion = roles_df['Llanta_refaccion'].iloc[0]
        limpiadores = roles_df['Limpiadores'].iloc[0]
        pintura = roles_df['Pintura_rayada'].iloc[0]
        cristales = roles_df['Cristales_rotos'].iloc[0]
        golpes = roles_df['Golpes'].iloc[0]
        tapetes = roles_df['Tapetes'].iloc[0]
        extintor = roles_df['Extintor'].iloc[0]
        tapones_gasolina = roles_df['Tapones_gasolina'].iloc[0]
        calaveras = roles_df['Calaveras_rotas'].iloc[0]
        molduras = roles_df['Molduras_completas'].iloc[0] 


 
        htmlstring = r"""<!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <div class="container">
        
        <div class="center-text">
        <strong> <p>ORDEN DE SERVICIO<br/>
        Refaccionaría y Taller Aautomotriz <br/>
        Trotamundos <br/>
        Horario <br/>
        Lunes a Viernes <br/>
        8 am - 6pm <br/>
        Sábados<br/>
        8 am - 3 pm<br/>        
        29 Guerrero y Bravo #422.
        Col. Héroes de Nacozari. C.P. 87030 <br/>
        Tel:(834) 2285 2869 y (834) 285 2872 R.F.C. CALN810623UF3</p>
        </strong>
        </div>
        
        </div>
  
		<!-- <img style="width:30%;" align:left; src="C:\Users\arael\Downloads\trot.jpg"/>
		<img style="width:30%;" align:right; src="C:\Users\arael\Downloads\todo.jpg"/> -->
		<!-- <h2 style="text-align:center;font-size:25px;">ORDEN DE SERVICIO</h2> 
		<h3 style="text-align:center;">Refaccionaría y Taller Aautomotriz</h3>
		<div style="text-align: right;">Horario <br/></h3>
		Lunes a Viernes <br/>
		8 am - 6pm <br/>
		Sábados<br/>
		8 am - 3 pm<br/>
		<h3 style="text-align:center;">Trotamundos</h3>
		<h3 style="text-align:center;">29 Guerrero y Bravo #422.</h3>
		<h3 style="text-align:center;">Col. Héroes de Nacozari. C.P. 87030</h3>
		<h3 style="text-align:center;">Tel:(834) 2285 2869 y (834) 285 2872 R.F.C. CALN810623UF3</h3> -->
		<div style="position: relative;">
		<div style="width: 20%; position: relative;">"""
        htmlstring +=f"""
		<table> 
		<th>
		  ORDEN
		</th>
		<tr>
		<td>
        {roles_df['idOrden'].iloc[0]}
		</td>
		</tr>
		<tr>
		<td>
        Fecha de Recepción:
	    </td>
		</tr>
		<tr>
		<td>
        Fecha de Entrega:
		</td>
		</tr>
		</table>
		</div>
		<div style="width: 100%; position: absolute; left: 30%; top: 0; height: 100%;">
		<table> 
		<tr>
        <td>Hora de compromiso</td>
        <td>Motivo de Visita:  (Previsto)  (Correctivo)</td>
		</tr>
		<tr>
        <td>Hora de entrega</td>
        <td>Medio:  Periódico  Radio  TV  Volante   Recomendación  Otros</td>
		</tr>
		</table>
		</div>
		</div>
		</head>
		<meta charset="UTF-8">"""
        htmlstring +="""
		<style>
		.left-image, .right-image {
        max-width: 20%; 
        height: 35%;
        border-radius:50%;
        }
		.container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        }
        .left-image, .right-image {
        max-width: 20%; /* Puedes ajustar el tamaño de las imágenes según tus necesidades */
        height: auto;
        }
        .center-text {
        flex: 1;
        text-align: center;
        font-size: 20px;
        padding: 0 20px; /* Espaciado alrededor del texto */
        font-weight: 50%;
        }
		table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #000;
		}
		td, th {
        border-collapse: collapse; border: 1px solid #dddddd;
        text-align: left;
        border: 1px solid #000;
        vertical-align: top;
        padding: 8px;
		}
		th {
        background-color: #dddddd;
		}
		.linea {
		border-top: 1px solid black;
		height: 2px;
		max-width: 200px;
		padding: 0;
		margin: 20px auto 0 auto;
		}
		td.empty-cell {
        min-width: 50px; /* Establece el tamaño mínimo para celdas vacías */
        min-height: 20px; /* Establece la altura mínima para celdas vacías */
		}
		</style>"""
        htmlstring += f"""
		<body>
		<div style="position: relative;">
        <div style="width: 40%; position: relative; height: 100%;">
        <table>
        <th>Cliente</th>  
        <tr>
        <td>Facturar a:{factura}</td>            
        </tr>
        <tr>
        <td>Nombre:{nombre}</td> 
        </tr>
        <tr>
        <td>Calle:{calle} </td>
        <td>No. int:{noint}</td>
        </tr>
        <tr>
        <td>Colonia:{colonia}</td>
        <td>Ciudad:{ciuadad}</td>
        </tr>
        <tr>
        <td>Cumpleaños:</td>
        <td>Estado:{estado}</td>  
        </tr>
        <tr>
        <td>Tel:{tel}</td>
        <td>Cel. /Nex:{cel} </td>
        </tr>
        <tr>
        <td>EMAIL:{email}</td>
        </tr>
        <tr>
        <td>RFC:{rfc}</td> 
        </tr>
        <tr>
        <td>Autorización Externa:{autorizacion}</td>
        </tr>
        <tr>
        <th>Servicio</th>
        </tr>

        <tr>
        
        <td>
        <h3 style="text-align:center;">FILTROS</h3>
        </td>
        </tr>
        
        <tr>
          <td>Filtro de Aire:</td>
         
          
        </tr>
        <tr>
          <td>Filtro de Aceite:</td>
         
        </tr>
        
        <tr>
          <td>Filtro de Cabina</td>
         
        </tr>
        <tr>
          <td>Filtro de Gasolina:</td>
         
          
        </tr>
        <tr>
        </tr>
         <tr>
        
        <td>
        <h3 style="text-align:center;">LUBRICACIÓN</h3>
        </td>
        </tr>
        <tr>
          <td>Tapón de Carter:</td>
        
        </tr>
        <tr>
          <td>Aceite de Motor:</td> 
          <td>W  /SAE</td>
        
        
        </tr>
        <tr>
          <td>Aceite de Transmisión Automática:</td>
    
        </tr>
          <tr>
          <td>Aceite de Transmisión Estándar:</td>
          <td>W  /SAE</td>
        </tr>
          <tr>
          <td>Aceite de Diferencial:</td>
          <td>W  /SAE</td>
        </tr>
          <tr>
          <td>Dirección Hidráulica:</td>
        
        </tr>
          <tr>
          <td>Líquido de Frenos:</td>
          <td>W  /SAE</td>
       
        </tr>
          <tr>
          <td>Líquido Limpiaparabrisas:</td>
          <td>W  /SAE</td>
        
        </tr>
          <tr>
          <td>Aditivo:</td>
        
        </tr>
           <tr>
        
        <td>
        <h3 style="text-align:center;">BANDAS</h3>
        </td>
        </tr>
          <tr>
          <td>Poly-V:</td>
        
        </tr>
          <tr>
          <td>Alternador:</td>
         
        </tr>
          <tr>
          <td>Aire Acondicionado:</td>
        
        </tr>
            <tr>
          <td>Dirección Hidráulica:</td>
         
        </tr>
            <tr>
          <td>Banda de Tiempo:</td>
        
        </tr>

        <tr>        
        <td>
        <h3 style="text-align:center;">ENFRIAMIENTO</h3>
        </td>
        </tr>
         <tr>
          <td>Manguera Superior Radiador:</td>
         
        </tr>
           <tr>
          <td>Refrigerante/ Anticongelante:</td>
        
        </tr>
        
           <tr>
          <td>Bomba de Agua:</td>
         
        </tr>                  
           <tr>
          <td>Manguera Inferior Radiador:</td>
          
        </tr>
        <tr>
          <td>Tapón de Radiador:</td>
          
        </tr>

        <tr>
          
          <td>
          <h3 style="text-align:center;">AMORTIGUADORES/BASES</h3>
          </td>
         
          </tr>
          
        <tr>
            <td>Delanteros:</td>
          
          </tr>
          <tr>
            <td>Traseros:</td>
            
          </tr>
        <tr>
        
        <td>
        <h3 style="text-align:center;">MOTOR</h3>
        </td>
        
        
        </tr>
        
        <tr>
          <td>Diagnóstico (Costo o revisión):</td>
        
        </tr>
        
        <tr>
          <td>Afinación:</td>
          <td>Menor 	Mayor 	Premium</td>
        </tr>
        
        
        <tr>
          <td>Tapa de Distribuidor:</td>
         
        </tr>
        
        
        <tr>
          <td>Rotor de Distribuidor:</td>
        </tr>              
        <tr>
          <td>Cables de Bujias:</td>
        
        </tr>
        
        <tr>
          <td>Bujias:</td>
          
        </tr>                
        <tr>
          <td>Sensor:</td>
         
        </tr>
             
        </table>
        </div>
        <div style="width: 50%; position: absolute; left: 50%; top: 0; height: 100%;">
        <table>
        <th>Vehículo</th>
        <tr>                
        <td>Marca:{marca}</td> 
        <td>Tipo:{tipo}</td>  
        </tr>
        <tr>
        <td>Modelo:{modelo}</td>
        <td>Motor:{motor}</td>
        </tr>
        <tr>          
        <td>Color:{color}</td>
        <td>Kms:{kms}</td>
        </tr>
        <tr>
        
        <td>N. Serie:{noserie}</td>
          
        </tr>
        <tr>
          <td>Placa:{placa}</td>
        </tr>
        <tr>
          <th>Inventario de Vehículo</th>
        </tr>


        <tr>
        
        
        <td>Espejo Retrovisor:</td>
        <td>{espejoretrovisor}</td>
        
        
        </tr>
        <tr>
        
        <td>Espejo Izquierdo:</td>
        <td>{espejoizq}</td>
        </tr>
          
        <tr>
            
        <td>Espejo Derecho:</td>
        <td></td>
        </tr>
        <tr>
           
        <td>Antena:</td>
        <td>{antena}</td>
                  
        </tr>
        <tr>
                  
        <td>Tapones de Ruedas:</td>
        <td>{taponesruedas}</td>
        </tr>
        <tr>
         
        
        <tr>
                  
        <td>Radio:</td>
        <td>{radio}</td>
        </tr>
        <tr>
                   
        <td>Encendedor:</td>
        <td>{encendedor}</td>
        </tr>
        <tr>
                   
        <td>Gato:</td>
        <td>{gato}</td>
        </tr>
        <tr>
                   
        <td>Herramienta:</td>
        <td>{herramienta}</td>
        </tr>
        <tr>
                    
        <td>Llanta de Refacción:</td>
        <td>{llanarefaccion}</td>
        </tr>
        <tr>
        
        <td>Limpiadores:</td>
        <td>{limpiadores}</td>
        </tr>
        <tr>
                   
        <td>Pintura Rayada:</td>
        <td>{pintura}</td>
        </tr>
        <tr>
                    
        <td>Cristales Rotos:</td>
        <td>{cristales}</td>
        </tr>
        <tr>
                    
        <td>Golpes:</td>
        <td>{golpes}</td>
        </tr>

        <tr>
                    
        <td>Tapetes:</td>
        <td>{tapetes}</td>
        </tr>

        <tr>
          
        <td>Extintor:</td>
        <td>{extintor}</td>
        </tr>

        <tr>
          
        <td>Tapón de Gasolina:</td>
        <td>{tapones_gasolina}</td>
        </tr>

        <tr>
          
        <td>Calaveras Rotas:</td>
        <td>{calaveras}</td>
        </tr>

        <tr>
          
        <td>Molduras Completas:</td>
        <td>{molduras}</td>
        </tr>

        <tr>
        <th>
        Servicio
        </th>
        </tr>
        <tr> 
        <td>
        <h3 style="text-align:center;">LLANTAS</h3>
        </td>
        </tr>

        <tr>
        <td>Medida:</td>
        </tr>
        <tr>
        <td>Alineación:</td>
        </tr>
        <tr>
        <td>Balanceo:</td>
        </tr>
        <tr>
        <td>Rotación:</td>
        </tr>
        <tr>
        <td>Montaje:</td>
        </tr>
        <tr>
        <td>Válvulas:</td>
        </tr>
        <tr> 
        <td>
        <h3 style="text-align:center;">FRENOS</h3>
        </td>
        </tr>
        <tr>
        <td>Generales:</td>
        </tr>
        <tr>
        <td>Delanteros:</td>
        </tr>
        <tr>
        <td>Traseros:</td>
        </tr>
        <tr>
        <td>Discos (2) (4):</td>
        </tr>
        <tr>
        <td>Tambores:</td>
        </tr>
        <tr>
        <td>Cilindros:</td>
        </tr>
        <tr>
        <td>Limpieza y Ajuste:</td>
        </tr>
        <tr>
        <td>Rectificado Disc/Tam:</td>
        </tr>
        <tr> 
        <td>
        <h3 style="text-align:center;">OTROS</h3>
        </td>
        </tr>
        <tr>
        <td>Limpiaparabrisas:</td>
        </tr>
        <tr>
        <td>Engrasado:</td>
        </tr>
        <tr>
        <td>Químicos:</td>
        </tr>



        </table>
        </div>
		</div>

		<table>
		<th>
		Observaciones
		</th>
		<tr>
        <td>

        </td>
	    </tr>
		</table>
      

		<div></div>
      
		<table> 
         
      
		<tr>
		<td>
		Firma del Proveedor
      
		</td>

		<td>
		Firma de Aceptación del Cliente
		
		</td>
		
		</tr>
		
		</table>
		
		<div></div>

		<table>
		<th>
		Servicio Solicitado
		</th>
		<th>
		Recibió
		</th>
		<th>
		Técnico
		</th>
		<th>
		Orden
		</th>


		<tr>
		  <td></td>
		</tr>

		</table>
		</body>
		</html>"""
         # Resto del código para convertir a PDF...
        img = "\\img1.jpg"
        pdf_path = "example.pdf"
          # Rutas y configuraciones para Linux
        path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_string(htmlstring, 'reporte.pdf', configuration=config)
        return JSONResponse(content={"message": "PDF creado exitosamente"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get(
        path="/api/empleados",
        name='Obtener empleados',
        tags=['Seguridad'],
        description='Método para obtener la informacion de todos los empleados',
        response_model=List[Empleado]
)
def getempleados():
    query = f"[Seguridad].[usuariosinsupdel] @Accion = 2"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)

@app.get(
        path="/api/empleado",
        name='Obtener empleado',
        tags=['Seguridad'],
        description='Método para obtener la informacion de todos los empleados',
        response_model=Empleado
)
def getempleados(IdUsuario: str):
    query = f"[Seguridad].[usuariosinsupdel] @Accion = 3, @Idusuario = {IdUsuario}"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    return JSONResponse(status_code=200,content=resultado)

@app.post(
        path="/api/checklist",
        name='Insertar checklist',
        tags=['Checklist'],
        description='Método para insertar el checklist',
        response_model=Checklist
)
def savechecklist(payload: Checklist):
    query = f"""
    EXEC InsertChecklist
        @lectura_codigos = {payload.Lectura_codigos}, \
        @lectura_codigos_observacion = N'{payload.Lectura_codigos_observacion}' , \
        @lectura_codigos_foto = N'{payload.Lectura_codigos_foto}' , \
        @servofreno = {payload.Servofreno}, \
        @servofreno_observacion = N'{payload.Servofreno_observacion}' , \
        @servofreno_foto = N'{payload.Servofreno_foto}' , \
        @pedal_freno = {payload.Pedal_freno}, \
        @pedal_freno_observacion = N'{payload.Pedal_freno_observacion}' , \
        @pedal_freno_foto = N'{payload.Pedal_freno_foto}' , \
        @pedal_estacionamiento = {payload.Pedal_estacionamiento}, \
        @pedal_estacionamiento_observacion = N'{payload.Pedal_estacionamiento_observacion}' , \
        @pedal_estacionamiento_foto = N'{payload.Pedal_estacionamiento_foto}' , \
        @cinturon_seguridad = {payload.Cinturon_seguridad}, \
        @cinturon_seguridad_observacion = N'{payload.Cinturon_seguridad_observacion}' , \
        @cinturon_seguridad_foto = N'{payload.Cinturon_seguridad_foto}' , \
        @cuadro_instrumentos = {payload.Cuadro_instrumentos}, \
        @cuadro_instrumentos_observacion = N'{payload.Cuadro_instrumentos_observacion}' ,\
        @cuadro_instrumentos_foto = N'{payload.Cuadro_instrumentos_foto}' ,\
        @aire_acondicionado = {payload.Aire_acondicionado},\
        @aire_acondicionado_observacion = N'{payload.Aire_acondicionado_observacion}' ,\
        @aire_acondicionado_foto = N'{payload.Aire_acondicionado_foto}' ,\
        @bocina_claxon = {payload.Bocina_claxon},\
        @bocina_claxon_observacion = N'{payload.Bocina_claxon_observacion}' ,\
        @bocina_claxon_foto = N'{payload.Bocina_claxon_foto}' ,\
        @iluminacion_interior = {payload.Iluminacion_interior},\
        @iluminacion_interior_observacion = N'{payload.Iluminacion_interior_observacion}' ,\
        @iluminacion_interior_foto = N'{payload.Iluminacion_interior_foto}' ,\
        @iluminacion_externa = {payload.Iluminacion_externa},\
        @iluminacion_externa_observacion = N'{payload.Iluminacion_externa_observacion}' ,\
        @iluminacion_externa_foto = N'{payload.Iluminacion_externa_foto}' ,\
        @limpiaparabrisas = {payload.Limpiaparabrisas}, \
        @limpiaparabrisas_observacion = N'{payload.Limpiaparabrisas_observacion}' ,\
        @limpiaparabrisas_foto = N'{payload.Limpiaparabrisas_foto}' , \
        @limpia_medallon = {payload.Limpia_medallon}, \
        @limpia_medallon_observacion = N'{payload.Limpia_medallon_observacion}' , \
        @limpia_medallon_foto = N'{payload.Limpia_medallon_foto}' , \
        @neumaticos_friccion = {payload.Neumaticos_friccion}, \
        @neumaticos_friccion_observacion = N'{payload.Neumaticos_friccion_observacion}' ,  \
        @neumaticos_friccion_foto = N'{payload.Neumaticos_friccion_foto}' , \
        @otros_vehiculo_en_piso = {payload.Otros_vehiculo_en_piso}, \
        @otros_vehiculo_en_piso_observacion = N'{payload.Otros_vehiculo_en_piso_observacion}' , \
        @otros_vehiculo_en_piso_foto = N'{payload.Otros_vehiculo_en_piso_foto}' , \
        @estado_fugas_aceite = {payload.Estado_fugas_aceite}, \
        @estado_fugas_aceite_observacion = N'{payload.Estado_fugas_aceite_observacion}' , \
        @estado_fugas_aceite_foto = N'{payload.Estado_fugas_aceite_foto}' , \
        @estado_nivel_calidad_lubricante_transmision = {payload.Estado_nivel_calidad_lubricante_transmision}, \
        @estado_nivel_calidad_lubricante_transmision_observacion = N'{payload.Estado_nivel_calidad_lubricante_transmision_observacion}' , \
        @estado_nivel_calidad_lubricante_transmision_foto = N'{payload.Estado_nivel_calidad_lubricante_transmision_foto}' , \
        @estado_nivel_calidad_lubricante_diferencial = {payload.Estado_nivel_calidad_lubricante_diferencial}, \
        @estado_nivel_calidad_lubricante_diferencial_observacion = N'{payload.Estado_nivel_calidad_lubricante_diferencial_observacion}' , \
        @estado_nivel_calidad_lubricante_diferencial_foto = N'{payload.Estado_nivel_calidad_lubricante_diferencial_foto}' , \
        @cubrepolvos_flechas = {payload.Cubrepolvos_flechas}, \
        @cubrepolvos_flechas_observacion = N'{payload.Cubrepolvos_flechas_observacion}' , \
        @cubrepolvos_flechas_foto = N'{payload.Cubrepolvos_flechas_foto}' , \
        @componentes_direccion = {payload.Componentes_direccion}, \
        @componentes_direccion_observacion = N'{payload.Componentes_direccion_observacion}' , \
        @componentes_direccion_foto = N'{payload.Componentes_direccion_foto}' , \
        @componentes_suspesion = {payload.Componentes_suspesion}, \
        @componentes_suspesion_observacion = N'{payload.Componentes_suspesion_observacion}' , \
        @componentes_suspesion_foto = N'{payload.Componentes_suspesion_foto}' , \
        @sistema_escape_completo = {payload.Sistema_escape_completo}, \
        @sistema_escape_completo_observacion = N'{payload.Sistema_escape_completo_observacion}' , \
        @sistema_escape_completo_foto = N'{payload.Sistema_escape_completo_foto}' , \
        @sistema_alimentacion_combustible = {payload.Sistema_alimentacion_combustible}, \
        @sistema_alimentacion_combustible_observacion = N'{payload.Sistema_alimentacion_combustible_observacion}' , \
        @sistema_alimentacion_combustible_foto = N'{payload.Sistema_alimentacion_combustible_foto}' , \
        @filtro_combustible = {payload.Filtro_combustible}, \
        @filtro_combustible_observacion = N'{payload.Filtro_combustible_observacion}' , \
        @filtro_combustible_foto = N'{payload.Filtro_combustible_foto}' , \
        @control_fugas_direccion_hidraulica = {payload.Control_fugas_direccion_hidraulica}, \
        @control_fugas_direccion_hidraulica_observacion = N'{payload.Control_fugas_direccion_hidraulica_observacion}' , \
        @control_fugas_direccion_hidraulica_foto = N'{payload.Control_fugas_direccion_hidraulica_foto}' , \
        @otros_altura_total = {payload.Otros_altura_total}, \
        @otros_altura_total_observacion = N'{payload.Otros_altura_total_observacion}' , \
        @otros_altura_total_foto = N'{payload.Otros_altura_total_foto}' , \
        @rodamiento_mazas_rueda = {payload.Rodamiento_mazas_rueda}, \
        @rodamiento_mazas_rueda_observacion = N'{payload.Rodamiento_mazas_rueda_observacion}' , \
        @rodamiento_mazas_rueda_foto = N'{payload.Rodamiento_mazas_rueda_foto}' , \
        @holgura_partes_suspension_rueda = {payload.Holgura_partes_suspension_rueda}, \
        @holgura_partes_suspension_rueda_observacion = N'{payload.Holgura_partes_suspension_rueda_observacion}' , \
        @holgura_partes_suspension_rueda_foto = N'{payload.Holgura_partes_suspension_rueda_foto}' , \
        @control_neumaticos_desgaste_presion = {payload.Control_neumaticos_desgaste_presion}, \
        @control_neumaticos_desgaste_presion_observacion = N'{payload.Control_neumaticos_desgaste_presion_observacion}' , \
        @control_neumaticos_desgaste_presion_foto = N'{payload.Control_neumaticos_desgaste_presion_foto}' , \
        @profundidad = {payload.Profundidad}, \
        @profundidad_observacion = N'{payload.Profundidad_observacion}' , \
        @profundidad_foto = N'{payload.Profundidad_foto}' , \
        @presion = {payload.Presion}, \
        @presion_observacion = N'{payload.Presion_observacion}' , \
        @presion_foto = N'{payload.Presion_foto}' , \
        @otros_altura_media = {payload.Otros_altura_media}, \
        @otros_altura_media_observacion = N'{payload.Otros_altura_media_observacion}' , \
        @otros_altura_media_foto = N'{payload.Otros_altura_media_foto}' , \
        @nivel_calidad_aceite_motor = {payload.Nivel_calidad_aceite_motor}, \
        @nivel_calidad_aceite_motor_observacion = N'{payload.Nivel_calidad_aceite_motor_observacion}' , \
        @nivel_calidad_aceite_motor_foto = N'{payload.Nivel_calidad_aceite_motor_foto}' , \
        @filtro_aire = {payload.Filtro_aire}, \
        @filtro_aire_observacion = N'{payload.Filtro_aire_observacion}' , \
        @filtro_aire_foto = N'{payload.Filtro_aire_foto}' , \
        @filtro_polen = {payload.Filtro_polen}, \
        @filtro_polen_observacion = N'{payload.Filtro_polen_observacion}' , \
        @filtro_polen_foto = N'{payload.Filtro_polen_foto}' , \
        @filtro_pcv = {payload.Filtro_pcv}, \
        @filtro_pcv_observacion = N'{payload.Filtro_pcv_observacion}' , \
        @filtro_pcv_foto = N'{payload.Filtro_pcv_foto}' , \
        @valvula_pcv = {payload.Valvula_pcv}, \
        @valvula_pcv_observacion = N'{payload.Valvula_pcv_observacion}' , \
        @valvula_pcv_foto = N'{payload.Valvula_pcv_foto}' , \
        @bujias_encendido = {payload.Bujias_encendido}, \
        @bujias_encendido_observacion = N'{payload.Bujias_encendido_observacion}' , \
        @bujias_encendido_foto = N'{payload.Bujias_encendido_foto}' , \
        @cables_bujias_bobinas_ignicion = {payload.Cables_bujias_bobinas_ignicion}, \
        @cables_bujias_bobinas_ignicion_observacion = N'{payload.Cables_bujias_bobinas_ignicion_observacion}' , \
        @cables_bujias_bobinas_ignicion_foto = N'{payload.Cables_bujias_bobinas_ignicion_foto}' , \
        @nivel_anticongenlante = {payload.Nivel_anticongenlante}, \
        @nivel_anticongenlante_observacion = N'{payload.Nivel_anticongenlante_observacion}' , \
        @nivel_anticongenlante_foto = N'{payload.Nivel_anticongenlante_foto}' , \
        @tapon_radiador = {payload.Tapon_radiador}, \
        @tapon_radiador_observacion = N'{payload.Tapon_radiador_observacion}' , \
        @tapon_radiador_foto = N'{payload.Tapon_radiador_foto}' , \
        @mangueras_sistema = {payload.Mangueras_sistema}, \
        @mangueras_sistema_observacion = N'{payload.Mangueras_sistema_observacion}' , \
        @mangueras_sistema_foto = N'{payload.Mangueras_sistema_foto}' , \
        @desempeño_ventilador = {payload.Desempeno_ventilador}, \
        @desempeño_ventilador_observacion = N'{payload.Desempeno_ventilador_observacion}' , \
        @desempeño_ventilador_foto = N'{payload.Desempeno_ventilador_foto}' , \
        @calidad_liquido_limpiaparabrisas = {payload.Calidad_liquido_limpiaparabrisas}, \
        @calidad_liquido_limpiaparabrisas_observacion = N'{payload.Calidad_liquido_limpiaparabrisas_observacion}' , \
        @calidad_liquido_limpiaparabrisas_foto = N'{payload.Calidad_liquido_limpiaparabrisas_foto}' , \
        @calidad_aceite_direccion_hidraulica = {payload.Calidad_aceite_direccion_hidraulica}, \
        @calidad_aceite_direccion_hidraulica_observacion = N'{payload.Calidad_aceite_direccion_hidraulica_observacion}' , \
        @calidad_aceite_direccion_hidraulica_foto = N'{payload.Calidad_aceite_direccion_hidraulica_foto}' , \
        @calidad_aceite_transmision_bayoneta = {payload.Calidad_aceite_transmision_bayoneta}, \
        @calidad_aceite_transmision_bayoneta_observacion = N'{payload.Calidad_aceite_transmision_bayoneta_observacion}' , \
        @calidad_aceite_transmision_bayoneta_foto = N'{payload.Calidad_aceite_transmision_bayoneta_foto}' , \
        @liquido_bateria_condiciones = {payload.Liquido_bateria_condiciones}, \
        @liquido_bateria_condiciones_observacion = N'{payload.Liquido_bateria_condiciones_observacion}' , \
        @liquido_bateria_condiciones_foto = N'{payload.Liquido_bateria_condiciones_foto}' ,    \
        @bandas_poly_v = {payload.Bandas_poly_v}, \
        @bandas_poly_v_observacion = N'{payload.Bandas_poly_v_observacion}' , \
        @bandas_poly_v_foto = N'{payload.Bandas_poly_v_foto}' , \
        @poleas_banda = {payload.Poleas_banda}, \
        @poleas_banda_observacion = N'{payload.Poleas_banda_observacion}' , \
        @poleas_banda_foto = N'{payload.Poleas_banda_foto}' , \
        @banda_tiempo = {payload.Banda_tiempo}, \
        @banda_tiempo_observacion = N'{payload.Banda_tiempo_observacion}' , \
        @banda_tiempo_foto = N'{payload.Banda_tiempo_foto}' , \
        @otros_habitaculo_motor = {payload.Otros_habitaculo_motor}, \
        @otros_habitaculo_motor_observacion = N'{payload.Otros_habitaculo_motor_observacion}' , \
        @otros_habitaculo_motor_foto = N'{payload.Otros_habitaculo_motor_foto}' , \
        @reset_intervalo_servicio = {payload.Reset_intervalo_servicio}, \
        @reset_intervalo_servicio_observacion = N'{payload.Reset_intervalo_servicio_observacion}' , \
        @reset_intervalo_servicio_foto = N'{payload.Reset_intervalo_servicio_foto}' , \
        @ajuste_tornillos_neumaticos_torquimetro = {payload.Ajuste_tornillos_neumaticos_torquimetro}, \
        @ajuste_tornillos_neumaticos_torquimetro_observacion = N'{payload.Ajuste_tornillos_neumaticos_torquimetro_observacion}' , \
        @ajuste_tornillos_neumaticos_torquimetro_foto = N'{payload.Ajuste_tornillos_neumaticos_torquimetro_foto}' , \
        @limpiar_libricar_puertas_cerraduras = {payload.Limpiar_libricar_puertas_cerraduras}, \
        @limpiar_libricar_puertas_cerraduras_observacion = N'{payload.Limpiar_libricar_puertas_cerraduras_observacion}' , \
        @limpiar_libricar_puertas_cerraduras_foto = N'{payload.Limpiar_libricar_puertas_cerraduras_foto}' , \
        @completar_plan_mantenimiento = {payload.Completar_plan_mantenimiento}, \
        @completar_plan_mantenimiento_observacion = N'{payload.Completar_plan_mantenimiento_observacion}' , \
        @completar_plan_mantenimiento_foto = N'{payload.Completar_plan_mantenimiento_foto}' , \
        @fecha = N'{payload.Fecha}' , \
        @Id_empleado = {payload.Id_empleado} , \
        @Id_vehiculo = {payload.Id_vehiculo} , \
        @id_ordendeservicio = {payload.Id_ordendeservicio} , \
        @NumeroSerie = '{payload.NumeroSerie}' """
    print (query)
    with engine.begin() as conn:
          conn.execution_options(autocommit = True)
          roles_df = pd.read_sql(query, conn)
    dumpp = ResponseModel(id_resultado=1,respuesta="El checklis se guardó de manera correcta")
    dict = dumpp.model_dump()
    return JSONResponse(status_code=200, content=dict)

@app.get(
        path="/api/obtenerchecklist",
        name='Obtener checklist',
        tags=['Checklist'],
        description='Método para obtener la informacion de 1 checklist',
        response_model=Checklist
)
def getempleados(Idchecklist: int):
    query = f"exec [dbo].[sp_get_all_checklist] @IdCheckList = {Idchecklist}"
    roles_df = pd.read_sql(query, engine)
    resultado = roles_df.to_dict(orient="records")
    print(resultado)
    return JSONResponse(status_code=200,content=resultado[0])

    
if __name__ == '__main__':
    app.run()
    