from sqlalchemy import create_engine


# Configura la conexión a la base de datos con SQLAlchemy
DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=/usr/local/lib/libmsodbcsql.17.dylib', echo=True"
engine = create_engine(DATABASE_URL, echo=True)
