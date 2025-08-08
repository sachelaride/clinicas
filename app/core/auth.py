"""
Authentication and authorization utilities.

This file contains functions for getting the current user, checking for active users, and checking for permissions.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

from .. import models
from ..core.database import get_db
from ..core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(models.User).options(joinedload(models.User.perfil).joinedload(models.Perfil.permissoes)).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def has_permission(permission_name: str):
    async def permission_checker(current_user: models.User = Depends(get_current_active_user)):
        # Se o usuário for superuser ou tiver acesso de admin, ele tem todas as permissões
        if current_user.is_superuser or (current_user.perfil and any(p.nome == "admin_acesso" for p in current_user.perfil.permissoes)):
            return current_user

        if not current_user.perfil:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não possui perfil atribuído")
        
        # Verifica se o perfil do usuário possui a permissão necessária
        for permission in current_user.perfil.permissoes:
            if permission.nome == permission_name:
                return current_user
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Usuário não possui permissão: {permission_name}")
    return permission_checker

async def get_current_admin_user(current_user: models.User = Depends(has_permission("admin_acesso"))):
    return current_user

async def get_current_profissional_user(current_user: models.User = Depends(has_permission("profissional_acesso"))):
    return current_user

async def get_current_paciente_user(current_user: models.User = Depends(has_permission("paciente_acesso"))):
    return current_user
