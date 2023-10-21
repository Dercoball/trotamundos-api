from fastapi import FastAPI
from sqlalchemy import text
from database import engine
import pandas as pd  # Importa Pandas

app = FastAPI()

# Crea la instancia de la aplicación FastAPI
app = FastAPI()

# Ruta para obtener los resultados de la consulta SQL en formato JSON (GET)
@app.get("/query/")
def get_query_result():
    query = text("SELECT * FROM tabla1")

    # Ejecutar la consulta utilizando el motor de conexión
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = result.fetchall()

    # Convierte los resultados en un DataFrame de Pandas
    df = pd.DataFrame(rows, columns=result.keys())

    # Convierte el DataFrame en una lista de diccionarios
    result_list = df.to_dict(orient="records")

    return result_list[0]

if __name__ == '__main__':
    app.run()