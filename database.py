from sqlalchemy import create_engine

# SERVER = 'trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com'
# DATABASE = 'trotamundosdb'
# DRIVER = 'SQL Server Native Client 11.0'
# USERNAME = 'sa'
# PASSWORD = 'Trotamundosserver'
# DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

# engine = create_engine(DATABASE_CONNECTION)
# connection = engine.connect()
# # Configura la conexión a la base de datos con SQLAlchemy
# # engine = create_engine("mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?+Driver+17+for+SQL+Server")
# # DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.5.1'"
# # engine = create_engine(DATABASE_URL, echo=True)

DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL, echo=True)

