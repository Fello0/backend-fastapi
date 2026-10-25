from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserLogin
from fastapi import HTTPException
import jwt
import os
from datetime import datetime, timedelta

class AuthController:
    def __init__(self, db: Session):
        self.db = db
        self.secret_key = os.getenv("SECRET_KEY", "secret")

    def login(self, user_data: UserLogin):
        # Buscar usuario en la base de datos
        user = self.db.query(User).filter(User.username == user_data.username).first()
        
        # Validar credenciales (US01)
        if not user or user.password != user_data.password:
            raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")
            
        # Detecta automáticamente si en TiDB se llama 'role' o 'rol'
        role_value = getattr(user, 'role', getattr(user, 'rol', 'cliente1'))

        # Generar Token JWT
        payload = {
            "sub": user.username,
            "id": user.id,
            "role": role_value,
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        return {
            "access_token": token, 
            "user_id": user.id, 
            "role": role_value
        }