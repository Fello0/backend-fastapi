from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from config.security import verify_admin_role
from models.user import User
from schemas.user import UserCreate, UserResponse, UserCreatedResponse
from controllers.user_controller import UserController

router = APIRouter(prefix="/users", tags=["Usuarios (Admin)"])

@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(verify_admin_role),
):
    """Lista todos los usuarios. Solo admin1. Nunca devuelve contraseñas."""
    controller = UserController(db)
    return controller.list_users()

@router.post("/", response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(verify_admin_role),
):
    """Crea un usuario con rol. Solo admin1."""
    controller = UserController(db)
    return controller.create_user(payload)
