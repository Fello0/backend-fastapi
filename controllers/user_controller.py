from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from schemas.user import UserCreate
from config.security import ALLOWED_ROLES, resolve_role


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self):
        """Lista usuarios SIN exponer la contraseña (nunca se retorna el campo)."""
        users = self.db.query(User).order_by(User.id.asc()).all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "role": resolve_role(user),
            }
            for user in users
        ]

    def create_user(self, payload: UserCreate):
        username = (payload.username or "").strip()
        role = (payload.role or "cliente1").strip().lower()

        if not username:
            raise HTTPException(status_code=400, detail="El nombre de usuario es obligatorio.")

        if len(username) < 3:
            raise HTTPException(status_code=400, detail="El usuario debe tener al menos 3 caracteres.")

        if role not in ALLOWED_ROLES:
            raise HTTPException(
                status_code=400,
                detail="Rol inválido. Los roles permitidos son: admin1, auditor1, cliente1.",
            )

        if len(payload.password) < 4:
            raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 4 caracteres.")

        exists = self.db.query(User).filter(User.username == username).first()
        if exists:
            raise HTTPException(status_code=409, detail="Ese nombre de usuario ya existe.")

        user = User(username=username, password=payload.password, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {
            "id": user.id,
            "username": user.username,
            "role": role,
            "message": "Usuario creado correctamente",
        }
