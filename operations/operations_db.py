from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from data.models import User
from typing import List, Optional
from pydantic import BaseModel
import datetime


# Modelos de Pydantic para la API
class UserBase(BaseModel):
    name: str
    email: str
    is_active: bool = True
    is_premium: bool = False


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


# Operaciones de base de datos para usuarios
def create_user(db: Session, user: UserCreate) -> User:
    """Crear un nuevo usuario en la base de datos"""
    db_user = User(
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        is_premium=user.is_premium
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session) -> List[User]:
    """Obtener todos los usuarios de la base de datos"""
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Obtener un usuario específico por ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


def update_user(db: Session, user_id: int, user: UserCreate) -> User:
    """Actualizar un usuario existente"""
    db_user = get_user_by_id(db, user_id)
    db_user.name = user.name
    db_user.email = user.email
    db_user.is_active = user.is_active
    db_user.is_premium = user.is_premium
    db.commit()
    db.refresh(db_user)
    return db_user


def make_user_premium(db: Session, user_id: int) -> User:
    """Hacer un usuario premium"""
    db_user = get_user_by_id(db, user_id)
    db_user.is_premium = True
    db.commit()
    db.refresh(db_user)
    return db_user


def get_inactive_users(db: Session) -> List[User]:
    """Obtener usuarios inactivos"""
    return db.query(User).filter(User.is_active == False).all()


def get_premium_users(db: Session) -> List[User]:
    """Obtener usuarios premium"""
    return db.query(User).filter(User.is_premium == True).all()


def filter_users(db: Session, is_premium: Optional[bool] = None, is_active: Optional[bool] = None) -> List[User]:
    """Filtrar usuarios por estado (premium y/o activo)"""
    query = db.query(User)

    if is_premium is not None:
        query = query.filter(User.is_premium == is_premium)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.all()