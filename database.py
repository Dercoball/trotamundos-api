from sqlalchemy import create_engine


# Configura la conexión a la base de datos con SQLAlchemy
DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.5.1"
engine = create_engine(DATABASE_URL, echo=True)
