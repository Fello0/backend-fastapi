from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserLogin
from fastapi import HTTPException
from config.security import create_access_token, resolve_role


class AuthController:
    def __init__(self, db: Session):
        self.db = db

    def login(self, user_data: UserLogin):
        # Buscar usuario en la base de datos
        user = self.db.query(User).filter(User.username == user_data.username).first()

        # Validar credenciales (US01)
        if not user or user.password != user_data.password:
            raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")

        # Rol normalizado (soporta columna 'role' o 'rol')
        role_value = resolve_role(user)

        # Token JWT firmado
        token = create_access_token(user)

        return {
            "access_token": token,
            "user_id": user.id,
            "role": role_value,
        }
