from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base

# Configuración para SQLite (local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Para configuración remota, descomentar y ajustar la siguiente línea
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()