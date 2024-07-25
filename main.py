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

    
if __name__ == '__main__':
    app.run()
    