import os
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User

# ---------------------------------------------------------------------------
# Configuración del token (debe coincidir con SECRET_KEY de Render / .env)
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
TOKEN_EXPIRATION_DAYS = 1

ADMIN_ROLE = "admin1"
ALLOWED_ROLES = ("admin1", "auditor1", "cliente1")

# auto_error=False para poder devolver nuestros propios mensajes en español
bearer_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="JWT",
    description="Pega el access_token devuelto por POST /auth/login",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def resolve_role(user) -> str:
    """Devuelve el rol normalizado (soporta columna 'role' o 'rol' en TiDB)."""
    raw = getattr(user, "role", None) or getattr(user, "rol", None) or "cliente1"
    return str(raw).strip().lower()


def create_access_token(user) -> str:
    payload = {
        "sub": user.username,
        "id": user.id,
        "role": resolve_role(user),
        "exp": datetime.utcnow() + timedelta(days=TOKEN_EXPIRATION_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


# ---------------------------------------------------------------------------
# Dependencias de FastAPI
# ---------------------------------------------------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Valida el JWT y devuelve el usuario real de la base de datos."""
    if credentials is None or not credentials.credentials:
        raise _unauthorized("Token no proporcionado. Inicia sesión para continuar.")

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise _unauthorized("La sesión expiró. Inicia sesión nuevamente.")
    except jwt.PyJWTError:
        raise _unauthorized("Token inválido o malformado.")

    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if user is None and payload.get("id") is not None:
        user = db.query(User).filter(User.id == payload.get("id")).first()
    if user is None:
        raise _unauthorized("El usuario del token ya no existe.")

    return user


def verify_admin_role(current_user: User = Depends(get_current_user)) -> User:
    """RBAC estricto: SOLO admin1 pasa. auditor1 y cliente1 reciben 403."""
    if resolve_role(current_user) != ADMIN_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Esta operación requiere el rol de Administrador (admin1).",
        )
    return current_user
