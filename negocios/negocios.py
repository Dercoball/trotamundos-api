from datos import Datos


class Negocios:
    async def getusuario(self, payload):
        _datos = Datos()
        user = await _datos.inicio_sesion(payload)        
        return user