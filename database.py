from sqlalchemy import create_engine


# Configura la conexión a la base de datos con SQLAlchemy
#DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=ODBC+Driver+17+for+SQL+Server"
#engine = create_engine(DATABASE_URL, echo=True)
engine = create_engine('mssql+pyodbc://sa:Trotamundosserver@trotamundosdb.cuvrbibw9zda.us-east-2.rds.amazonaws.com/trotamundosdb?driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.5.1', echo=True)
engine.execute('select 1')