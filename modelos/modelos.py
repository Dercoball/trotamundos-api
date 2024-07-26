from typing import Optional, List
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
    Espejo_retrovisor_foto	: str
    Espejo_izquierdo_foto 	: str
    Antena_foto			    : str
    Tapones_ruedas_foto	    : str
    Radio_foto				: str
    Encendedor_foto		    : str
    Gato_foto				: str
    Herramienta_foto		: str
    Llanta_refaccion_foto	: str
    Limpiadores_foto		: str
    Pintura_rayada_foto	    : str
    Cristales_rotos_foto	: str
    Golpes_foto			    : str
    Tapetes_foto			: str
    Extintor_foto			: str
    Tapones_gasolina_foto	: str
    Calaveras_rotas_foto	: str
    Molduras_completas_foto : str

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

class ImageData(BaseModel):
    tags: List[str]
    description: List[str]
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

class Empleado(BaseModel):
    Idusuario: int
    Nombre: str
    Rol: int
    Estatus: int

class Checklist(BaseModel):
    Lectura_codigos: Optional[int] = None
    Lectura_codigos_observacion: Optional[str] = None
    Lectura_codigos_foto: Optional[str] = None

    Servofreno: Optional[int] = None
    Servofreno_observacion: Optional[str] = None
    Servofreno_foto: Optional[str] = None

    Pedal_freno: Optional[int] = None
    Pedal_freno_observacion: Optional[str] = None
    Pedal_freno_foto: Optional[str] = None

    Pedal_estacionamiento: Optional[int] = None
    Pedal_estacionamiento_observacion: Optional[str] = None
    Pedal_estacionamiento_foto: Optional[str] = None

    Cinturon_seguridad: Optional[int] = None
    Cinturon_seguridad_observacion: Optional[str] = None
    Cinturon_seguridad_foto: Optional[str] = None

    Cuadro_instrumentos: Optional[int] = None
    Cuadro_instrumentos_observacion: Optional[str] = None
    Cuadro_instrumentos_foto: Optional[str] = None

    Aire_acondicionado: Optional[int] = None
    Aire_acondicionado_observacion: Optional[str] = None
    Aire_acondicionado_foto: Optional[str] = None

    Bocina_claxon: Optional[int] = None
    Bocina_claxon_observacion: Optional[str] = None
    Bocina_claxon_foto: Optional[str] = None

    Iluminacion_interior: Optional[int] = None
    Iluminacion_interior_observacion: Optional[str] = None
    Iluminacion_interior_foto: Optional[str] = None

    Iluminacion_externa: Optional[int] = None
    Iluminacion_externa_observacion: Optional[str] = None
    Iluminacion_externa_foto: Optional[str] = None

    Limpiaparabrisas: Optional[int] = None
    Limpiaparabrisas_observacion: Optional[str] = None
    Limpiaparabrisas_foto: Optional[str] = None

    Limpia_medallon: Optional[int] = None
    Limpia_medallon_observacion: Optional[str] = None
    Limpia_medallon_foto: Optional[str] = None

    Neumaticos_friccion: Optional[int] = None
    Neumaticos_friccion_observacion: Optional[str] = None
    Neumaticos_friccion_foto: Optional[str] = None

    Otros_vehiculo_en_piso: Optional[int] = None
    Otros_vehiculo_en_piso_observacion: Optional[str] = None
    Otros_vehiculo_en_piso_foto: Optional[str] = None

    Estado_fugas_aceite: Optional[int] = None
    Estado_fugas_aceite_observacion: Optional[str] = None
    Estado_fugas_aceite_foto: Optional[str] = None

    Estado_nivel_calidad_lubricante_transmision: Optional[int] = None
    Estado_nivel_calidad_lubricante_transmision_observacion: Optional[str] = None
    Estado_nivel_calidad_lubricante_transmision_foto: Optional[str] = None

    Estado_nivel_calidad_lubricante_diferencial: Optional[int] = None
    Estado_nivel_calidad_lubricante_diferencial_observacion: Optional[str] = None
    Estado_nivel_calidad_lubricante_diferencial_foto: Optional[str] = None

    Cubrepolvos_flechas: Optional[int] = None
    Cubrepolvos_flechas_observacion: Optional[str] = None
    Cubrepolvos_flechas_foto: Optional[str] = None

    Componentes_direccion: Optional[int] = None
    Componentes_direccion_observacion: Optional[str] = None
    Componentes_direccion_foto: Optional[str] = None

    Componentes_suspesion: Optional[int] = None
    Componentes_suspesion_observacion: Optional[str] = None
    Componentes_suspesion_foto: Optional[str] = None

    Sistema_escape_completo: Optional[int] = None
    Sistema_escape_completo_observacion: Optional[str] = None
    Sistema_escape_completo_foto: Optional[str] = None

    Sistema_alimentacion_combustible: Optional[int] = None
    Sistema_alimentacion_combustible_observacion: Optional[str] = None
    Sistema_alimentacion_combustible_foto: Optional[str] = None

    Filtro_combustible: Optional[int] = None
    Filtro_combustible_observacion: Optional[str] = None
    Filtro_combustible_foto: Optional[str] = None

    Control_fugas_direccion_hidraulica: Optional[int] = None
    Control_fugas_direccion_hidraulica_observacion: Optional[str] = None
    Control_fugas_direccion_hidraulica_foto: Optional[str] = None

    Otros_altura_total: Optional[int] = None
    Otros_altura_total_observacion: Optional[str] = None
    Otros_altura_total_foto: Optional[str] = None

    Rodamiento_mazas_rueda: Optional[int] = None
    Rodamiento_mazas_rueda_observacion: Optional[str] = None
    Rodamiento_mazas_rueda_foto: Optional[str] = None

    Holgura_partes_suspension_rueda: Optional[int] = None
    Holgura_partes_suspension_rueda_observacion: Optional[str] = None
    Holgura_partes_suspension_rueda_foto: Optional[str] = None

    Control_neumaticos_desgaste_presion: Optional[int] = None
    Control_neumaticos_desgaste_presion_observacion: Optional[str] = None
    Control_neumaticos_desgaste_presion_foto: Optional[str] = None

    Profundidad: Optional[int] = None
    Profundidad_observacion: Optional[str] = None
    Profundidad_foto: Optional[str] = None

    Presion: Optional[int] = None
    Presion_observacion: Optional[str] = None
    Presion_foto: Optional[str] = None

    Otros_altura_media: Optional[int] = None
    Otros_altura_media_observacion: Optional[str] = None
    Otros_altura_media_foto: Optional[str] = None

    Nivel_calidad_aceite_motor: Optional[int] = None
    Nivel_calidad_aceite_motor_observacion: Optional[str] = None
    Nivel_calidad_aceite_motor_foto: Optional[str] = None

    Filtro_aire: Optional[int] = None
    Filtro_aire_observacion: Optional[str] = None
    Filtro_aire_foto: Optional[str] = None

    Filtro_polen: Optional[int] = None
    Filtro_polen_observacion: Optional[str] = None
    Filtro_polen_foto: Optional[str] = None

    Filtro_pcv: Optional[int] = None
    Filtro_pcv_observacion: Optional[str] = None
    Filtro_pcv_foto: Optional[str] = None

    Valvula_pcv: Optional[int] = None
    Valvula_pcv_observacion: Optional[str] = None
    Valvula_pcv_foto: Optional[str] = None

    Bujias_encendido: Optional[int] = None
    Bujias_encendido_observacion: Optional[str] = None
    Bujias_encendido_foto: Optional[str] = None

    Cables_bujias_bobinas_ignicion: Optional[int] = None
    Cables_bujias_bobinas_ignicion_observacion: Optional[str] = None
    Cables_bujias_bobinas_ignicion_foto: Optional[str] = None

    Nivel_anticongenlante: Optional[int] = None
    Nivel_anticongenlante_observacion: Optional[str] = None
    Nivel_anticongenlante_foto: Optional[str] = None

    Tapon_radiador: Optional[int] = None
    Tapon_radiador_observacion: Optional[str] = None
    Tapon_radiador_foto: Optional[str] = None

    Mangueras_sistema: Optional[int] = None
    Mangueras_sistema_observacion: Optional[str] = None
    Mangueras_sistema_foto: Optional[str] = None

    Desempeno_ventilador: Optional[int] = None
    Desempeno_ventilador_observacion: Optional[str] = None
    Desempeno_ventilador_foto: Optional[str] = None

    Calidad_liquido_limpiaparabrisas: Optional[int] = None
    Calidad_liquido_limpiaparabrisas_observacion: Optional[str] = None
    Calidad_liquido_limpiaparabrisas_foto: Optional[str] = None

    Calidad_aceite_direccion_hidraulica: Optional[int] = None
    Calidad_aceite_direccion_hidraulica_observacion: Optional[str] = None
    Calidad_aceite_direccion_hidraulica_foto: Optional[str] = None

    Calidad_aceite_transmision_bayoneta: Optional[int] = None
    Calidad_aceite_transmision_bayoneta_observacion: Optional[str] = None
    Calidad_aceite_transmision_bayoneta_foto: Optional[str] = None

    Liquido_bateria_condiciones: Optional[int] = None
    Liquido_bateria_condiciones_observacion: Optional[str] = None
    Liquido_bateria_condiciones_foto: Optional[str] = None

    Bandas_poly_v: Optional[int] = None
    Bandas_poly_v_observacion: Optional[str] = None
    Bandas_poly_v_foto: Optional[str] = None

    Poleas_banda: Optional[int] = None
    Poleas_banda_observacion: Optional[str] = None
    Poleas_banda_foto: Optional[str] = None

    Banda_tiempo: Optional[int] = None
    Banda_tiempo_observacion: Optional[str] = None
    Banda_tiempo_foto: Optional[str] = None

    Otros_habitaculo_motor: Optional[int] = None
    Otros_habitaculo_motor_observacion: Optional[str] = None
    Otros_habitaculo_motor_foto: Optional[str] = None

    Reset_intervalo_servicio: Optional[int] = None
    Reset_intervalo_servicio_observacion: Optional[str] = None
    Reset_intervalo_servicio_foto: Optional[str] = None

    Ajuste_tornillos_neumaticos_torquimetro: Optional[int] = None
    Ajuste_tornillos_neumaticos_torquimetro_observacion: Optional[str] = None
    Ajuste_tornillos_neumaticos_torquimetro_foto: Optional[str] = None

    Limpiar_libricar_puertas_cerraduras: Optional[int] = None
    Limpiar_libricar_puertas_cerraduras_observacion: Optional[str] = None
    Limpiar_libricar_puertas_cerraduras_foto: Optional[str] = None

    Completar_plan_mantenimiento: Optional[int] = None
    Completar_plan_mantenimiento_observacion: Optional[str] = None
    Completar_plan_mantenimiento_foto: Optional[str] = None

    Fecha: str
    Id_empleado: Optional[int] = None
    Id_vehiculo: Optional[int] = None
    Id_ordendeservicio: Optional[int] = None