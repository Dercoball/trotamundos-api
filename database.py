from sqlalchemy import create_engine


# Configura la conexión a la base de datos con SQLAlchemy
DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=ODBC+Driver+16+for+SQL+Server"
engine = create_engine(DATABASE_URL, echo=True)
