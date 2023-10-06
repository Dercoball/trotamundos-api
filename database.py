from sqlalchemy import create_engine


# Configura la conexión a la base de datos con SQLAlchemy
DATABASE_URL = "mssql+pyodbc://sa:Trotamundosserver@trotamundos.ccrmmk5pk9na.us-east-1.rds.amazonaws.com/prueba?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL, echo=True)
