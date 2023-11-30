from sqlalchemy import text
from database import engine
import pandas as pd  # Importa Pandas
from modelos import DatosLogin
from utils import utilsclass
from loguru import logger

class Datos():
    async def inicio_sesion(self, payload: DatosLogin):
        # conn = engine.connect()
        # query = f"select * from usuario where nombre = '{payload.usuario}'"
        # try:
        #     result = conn.execute(query).fetchall()
        #     if(len(result) == 0):
        #         return False
        #     hashed_password = result[0]['contraseña']
        #     if not await utilsclass.verify_password(payload.contrasena, hashed_password):
        #         return False
        #     return True
        # except Exception as error:
        #     logger.error(error)
        # finally:
        #     conn.close()
        pass