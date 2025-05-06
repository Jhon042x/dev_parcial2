from fastapi import FastAPI, Depends, status
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

# Importamos estas funciones directamente
from utils.connection_db import engine, SessionLocal, init_db
from data.models import Base


# Para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from operations.operations_db import (
    UserBase, UserCreate, UserResponse,
    create_user, get_all_users, get_user_by_id, update_user,
    make_user_premium, get_inactive_users, get_premium_users, filter_users
)

# Inicializar la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Usuarios", description="API para gestión de usuarios")


# Ruta personalizada para la documentación Swagger
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Documentación Swagger",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    )


# Método POST para añadir usuarios
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# Método GET para obtener todos los usuarios
@app.get("/users/", response_model=List[UserResponse])
def api_read_users(db: Session = Depends(get_db)):
    return get_all_users(db)


# Método GET para obtener un usuario específico por ID
@app.get("/users/{user_id}", response_model=UserResponse)
def api_read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


# Método PUT para actualizar el estado de un usuario
@app.put("/users/{user_id}", response_model=UserResponse)
def api_update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)


# Método PATCH para hacer un usuario Premium
@app.patch("/users/{user_id}/premium", response_model=UserResponse)
def api_make_user_premium(user_id: int, db: Session = Depends(get_db)):
    return make_user_premium(db, user_id)


# Método GET para consultar usuarios inactivos
@app.get("/users/status/inactive", response_model=List[UserResponse])
def api_read_inactive_users(db: Session = Depends(get_db)):
    return get_inactive_users(db)


# Método GET para consultar usuarios Premium
@app.get("/users/status/premium", response_model=List[UserResponse])
def api_read_premium_users(db: Session = Depends(get_db)):
    return get_premium_users(db)


# Método GET para filtrar usuarios por estado (premium y/o inactivo)
@app.get("/users/filter/", response_model=List[UserResponse])
def api_filter_users(is_premium: Optional[bool] = None, is_active: Optional[bool] = None,
                     db: Session = Depends(get_db)):
    return filter_users(db, is_premium, is_active)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)