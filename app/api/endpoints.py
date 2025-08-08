"""
API endpoints for the application.

This file defines the API routes for all resources in the application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas
from ..core.database import get_db
from ..core.security import get_password_hash, verify_password, create_access_token
from ..core.auth import get_current_user, get_current_active_user, get_current_admin_user, get_current_profissional_user, get_current_paciente_user, has_permission

router = APIRouter()

# Endpoint de Login para obter o token JWT
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Helper para obter o clinic_id do usuário logado
def get_clinic_id_from_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user.clinica_id

# Endpoints para Clinica
@router.post("/clinicas/", response_model=schemas.ClinicaInDBBase, status_code=status.HTTP_201_CREATED)
def create_clinica(clinica: schemas.ClinicaCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_clinicas"))):
    db_clinica = models.Clinica(**clinica.dict())
    db.add(db_clinica)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

@router.get("/clinicas/", response_model=List[schemas.ClinicaInDBBase])
def read_clinicas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_clinicas"))):
    clinicas = db.query(models.Clinica).offset(skip).limit(limit).all()
    return clinicas

@router.get("/clinicas/{clinica_id}", response_model=schemas.ClinicaInDBBase)
def read_clinica(clinica_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_clinicas"))):
    clinica = db.query(models.Clinica).filter(models.Clinica.id == clinica_id).first()
    if clinica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinica not found")
    return clinica

@router.put("/clinicas/{clinica_id}", response_model=schemas.ClinicaInDBBase)
def update_clinica(clinica_id: int, clinica: schemas.ClinicaUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_clinicas"))):
    db_clinica = db.query(models.Clinica).filter(models.Clinica.id == clinica_id).first()
    if db_clinica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinica not found")
    for key, value in clinica.dict(exclude_unset=True).items():
        setattr(db_clinica, key, value)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

@router.delete("/clinicas/{clinica_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinica(clinica_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_clinicas"))):
    db_clinica = db.query(models.Clinica).filter(models.Clinica.id == clinica_id).first()
    if db_clinica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinica not found")
    db.delete(db_clinica)
    db.commit()
    return {"message": "Clinica deleted successfully"}

# Endpoint público para listar clínicas
@router.get("/clinicas-public/", response_model=List[schemas.ClinicaInDBBase])
def read_clinicas_public(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clinicas = db.query(models.Clinica).offset(skip).limit(limit).all()
    return clinicas


# Endpoints para Perfil
@router.post("/perfis/", response_model=schemas.PerfilInDBBase, status_code=status.HTTP_201_CREATED)
def create_perfil(perfil: schemas.PerfilCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_perfis"))):
    db_perfil = models.Perfil(nome=perfil.nome)
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

@router.get("/perfis/", response_model=List[schemas.PerfilInDBBase])
def read_perfis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_perfis"))):
    perfis = db.query(models.Perfil).offset(skip).limit(limit).all()
    return perfis

@router.get("/perfis/{perfil_id}", response_model=schemas.PerfilInDBBase)
def read_perfil(perfil_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_perfis"))):
    perfil = db.query(models.Perfil).filter(models.Perfil.id == perfil_id).first()
    if perfil is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    return perfil

@router.put("/perfis/{perfil_id}", response_model=schemas.PerfilInDBBase)
def update_perfil(perfil_id: int, perfil_update: schemas.PerfilUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_perfis"))):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.id == perfil_id).first()
    if db_perfil is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    
    # Atualiza o nome do perfil se fornecido
    if perfil_update.nome is not None:
        db_perfil.nome = perfil_update.nome

    # Atualiza as permissões do perfil se fornecidas
    if perfil_update.permissoes is not None:
        db_perfil.permissoes.clear() # Remove todas as permissões existentes
        for perm_id in perfil_update.permissoes:
            permissao = db.query(models.Permissao).filter(models.Permissao.id == perm_id).first()
            if permissao:
                db_perfil.permissoes.append(permissao)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permissão com ID {perm_id} não encontrada.")

    db.commit()
    db.refresh(db_perfil)
    return db_perfil

@router.delete("/perfis/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_perfil(perfil_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_perfis"))):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.id == perfil_id).first()
    if db_perfil is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    db.delete(db_perfil)
    db.commit()
    return {"message": "Perfil deleted successfully"}

# Endpoints para Permissao
@router.post("/permissoes/", response_model=schemas.PermissaoInDBBase, status_code=status.HTTP_201_CREATED)
def create_permissao(permissao: schemas.PermissaoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_permissoes"))):
    db_permissao = models.Permissao(**permissao.dict())
    db.add(db_permissao)
    db.commit()
    db.refresh(db_permissao)
    return db_permissao

@router.get("/permissoes/", response_model=List[schemas.PermissaoInDBBase])
def read_permissoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_permissoes"))):
    permissoes = db.query(models.Permissao).offset(skip).limit(limit).all()
    return permissoes

@router.get("/permissoes/{permissao_id}", response_model=schemas.PermissaoInDBBase)
def read_permissao(permissao_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_permissoes"))):
    permissao = db.query(models.Permissao).filter(models.Permissao.id == permissao_id).first()
    if permissao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissao not found")
    return permissao

@router.put("/permissoes/{permissao_id}", response_model=schemas.PermissaoInDBBase)
def update_permissao(permissao_id: int, permissao: schemas.PermissaoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_permissoes"))):
    db_permissao = db.query(models.Permissao).filter(models.Permissao.id == permissao_id).first()
    if db_permissao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissao not found")
    for key, value in permissao.dict(exclude_unset=True).items():
        setattr(db_permissao, key, value)
    db.commit()
    db.refresh(db_permissao)
    return db_permissao

@router.delete("/permissoes/{permissao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permissao(permissao_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_permissoes"))):
    db_permissao = db.query(models.Permissao).filter(models.Permissao.id == permissao_id).first()
    if db_permissao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissao not found")
    db.delete(db_permissao)
    db.commit()
    return {"message": "Permissao deleted successfully"}

# Endpoints para User
@router.post("/users/", response_model=schemas.UserInDBBase, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_usuarios"))):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, perfil_id=user.perfil_id, clinica_id=user.clinica_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=schemas.UserInDBBase)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/", response_model=List[schemas.UserInDBBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_usuarios"))):
    users = db.query(models.User).options(joinedload(models.User.perfil)).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=schemas.UserInDBBase)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_usuarios"))):
    user = db.query(models.User).options(joinedload(models.User.perfil)).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserInDBBase)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_usuarios"))):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_data = user.dict(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        db_user.hashed_password = get_password_hash(user_data["password"])
        user_data.pop("password") # Remove password from user_data to avoid direct setattr

    if "perfil_id" in user_data:
        perfil = db.query(models.Perfil).filter(models.Perfil.id == user_data["perfil_id"]).first()
        if perfil is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
        db_user.perfil = perfil
        user_data.pop("perfil_id") # Remove perfil_id from user_data to avoid direct setattr

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_usuarios"))):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Endpoints para Paciente
@router.post("/pacientes/", response_model=schemas.PacienteInDBBase, status_code=status.HTTP_201_CREATED)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_pacientes"))):
    # Lógica para associar paciente à clínica do usuário logado, se aplicável
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar paciente para esta clínica")
    if paciente.clinica_id is None:
        paciente.clinica_id = current_user.clinica_id
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.get("/pacientes/", response_model=List[schemas.PacienteInDBBase])
def read_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_pacientes"))):
    if current_user.is_superuser:
        pacientes = db.query(models.Paciente).offset(skip).limit(limit).all()
    else:
        pacientes = db.query(models.Paciente).filter(models.Paciente.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return pacientes

@router.get("/pacientes/{paciente_id}", response_model=schemas.PacienteInDBBase)
def read_paciente(paciente_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_pacientes"))):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if paciente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente not found")
    # Verifica se o paciente pertence à clínica do usuário logado, a menos que seja admin
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este paciente")
    return paciente

@router.put("/pacientes/{paciente_id}", response_model=schemas.PacienteInDBBase)
def update_paciente(paciente_id: int, paciente: schemas.PacienteUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_pacientes"))):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if db_paciente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente not found")
    # Verifica permissão de atualização
    if not current_user.is_superuser and db_paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este paciente")
    for key, value in paciente.dict(exclude_unset=True).items():
        setattr(db_paciente, key, value)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.delete("/pacientes/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paciente(paciente_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_pacientes"))):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if db_paciente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente not found")
    # Verifica permissão de exclusão
    if not current_user.is_superuser and db_paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este paciente")
    db.delete(db_paciente)
    db.commit()
    return {"message": "Paciente deleted successfully"}

# Endpoints para LancamentoFinanceiro
@router.post("/lancamentos-financeiros/", response_model=schemas.LancamentoFinanceiroInDBBase, status_code=status.HTTP_201_CREATED)
def create_lancamento_financeiro(lancamento: schemas.LancamentoFinanceiroCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_lancamentos_financeiros"))):
    # If an attendance is linked, ensure it belongs to the user's clinic
    if lancamento.atendimento_id:
        atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == lancamento.atendimento_id).first()
        if not atendimento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento not found")
        agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
        paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
        if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar lançamento financeiro para este atendimento")

    db_lancamento = models.LancamentoFinanceiro(**lancamento.dict())
    db.add(db_lancamento)
    db.commit()
    db.refresh(db_lancamento)
    return db_lancamento

@router.get("/lancamentos-financeiros/", response_model=List[schemas.LancamentoFinanceiroInDBBase])
def read_lancamentos_financeiros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_lancamentos_financeiros"))):
    if current_user.is_superuser:
        lancamentos = db.query(models.LancamentoFinanceiro).offset(skip).limit(limit).all()
    else:
        # Filter by attendance's patient's clinic, which is linked to the user's clinic
        lancamentos = db.query(models.LancamentoFinanceiro).join(models.Atendimento).join(models.Agendamento).join(models.Paciente).filter(models.Paciente.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return lancamentos

@router.get("/lancamentos-financeiros/{lancamento_id}", response_model=schemas.LancamentoFinanceiroInDBBase)
def read_lancamento_financeiro(lancamento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_lancamentos_financeiros"))):
    lancamento = db.query(models.LancamentoFinanceiro).filter(models.LancamentoFinanceiro.id == lancamento_id).first()
    if lancamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LancamentoFinanceiro not found")
    
    # Check if the financial entry's attendance's patient belongs to the current user's clinic (unless admin)
    if lancamento.atendimento_id:
        atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == lancamento.atendimento_id).first()
        agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
        paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
        if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este lançamento financeiro")

    return lancamento

@router.put("/lancamentos-financeiros/{lancamento_id}", response_model=schemas.LancamentoFinanceiroInDBBase)
def update_lancamento_financeiro(lancamento_id: int, lancamento: schemas.LancamentoFinanceiroUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_lancamentos_financeiros"))):
    db_lancamento = db.query(models.LancamentoFinanceiro).filter(models.LancamentoFinanceiro.id == lancamento_id).first()
    if db_lancamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LancamentoFinanceiro not found")
    
    # Check if the financial entry's attendance's patient belongs to the current user's clinic (unless admin)
    if db_lancamento.atendimento_id:
        atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == db_lancamento.atendimento_id).first()
        agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
        paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
        if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este lançamento financeiro")

    for key, value in lancamento.dict(exclude_unset=True).items():
        setattr(db_lancamento, key, value)
    db.commit()
    db.refresh(db_lancamento)
    return db_lancamento

@router.delete("/lancamentos-financeiros/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lancamento_financeiro(lancamento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_lancamentos_financeiros"))):
    db_lancamento = db.query(models.LancamentoFinanceiro).filter(models.LancamentoFinanceiro.id == lancamento_id).first()
    if db_lancamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LancamentoFinanceiro not found")
    
    # Check if the financial entry's attendance's patient belongs to the current user's clinic (unless admin)
    if db_lancamento.atendimento_id:
        atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == db_lancamento.atendimento_id).first()
        agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
        paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
        if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este lançamento financeiro")

    db.delete(db_lancamento)
    db.commit()
    return {"message": "LancamentoFinanceiro deleted successfully"}

# Endpoints para Lead
@router.post("/leads/", response_model=schemas.LeadInDBBase, status_code=status.HTTP_201_CREATED)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_leads"))):
    if not current_user.is_superuser and lead.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar lead para esta clínica")
    if lead.clinica_id is None:
        lead.clinica_id = current_user.clinica_id
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/leads/", response_model=List[schemas.LeadInDBBase])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_leads"))):
    if current_user.is_superuser:
        leads = db.query(models.Lead).offset(skip).limit(limit).all()
    else:
        leads = db.query(models.Lead).filter(models.Lead.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return leads

@router.get("/leads/{lead_id}", response_model=schemas.LeadInDBBase)
def read_lead(lead_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_leads"))):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    if not current_user.is_superuser and lead.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este lead")
    return lead

@router.put("/leads/{lead_id}", response_model=schemas.LeadInDBBase)
def update_lead(lead_id: int, lead: schemas.LeadUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_leads"))):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    if not current_user.is_superuser and db_lead.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este lead")
    for key, value in lead.dict(exclude_unset=True).items():
        setattr(db_lead, key, value)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(lead_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_leads"))):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    if not current_user.is_superuser and db_lead.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este lead")
    db.delete(db_lead)
    db.commit()
    return {"message": "Lead deleted successfully"}

# Endpoints para Profissional
@router.post("/profissionais/", response_model=schemas.ProfissionalInDBBase, status_code=status.HTTP_201_CREATED)
def create_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_profissionais"))):
    # Ensure the user associated with the professional belongs to the current user's clinic (unless admin)
    user_obj = db.query(models.User).filter(models.User.id == profissional.user_id).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if not current_user.is_superuser and user_obj.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar profissional para a clínica deste usuário")

    db_profissional = models.Profissional(**profissional.dict())
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

@router.get("/profissionais/", response_model=List[schemas.ProfissionalInDBBase])
def read_profissionais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_profissionais"))):
    if current_user.is_superuser:
        profissionais = db.query(models.Profissional).offset(skip).limit(limit).all()
    else:
        # Filter by user's clinic, which is linked to the user's clinic
        profissionais = db.query(models.Profissional).join(models.User).filter(models.User.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return profissionais

@router.get("/profissionais/{profissional_id}", response_model=schemas.ProfissionalInDBBase)
def read_profissional(profissional_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_profissionais"))):
    profissional = db.query(models.Profissional).filter(models.Profissional.id == profissional_id).first()
    if profissional is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional not found")
    
    # Check if the professional's user belongs to the current user's clinic (unless admin)
    user_obj = db.query(models.User).filter(models.User.id == profissional.user_id).first()
    if not current_user.is_superuser and user_obj.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este profissional")

    return profissional

@router.put("/profissionais/{profissional_id}", response_model=schemas.ProfissionalInDBBase)
def update_profissional(profissional_id: int, profissional: schemas.ProfissionalUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_profissionais"))):
    db_profissional = db.query(models.Profissional).filter(models.Profissional.id == profissional_id).first()
    if db_profissional is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional não encontrado")
    
    # Check if the professional's user belongs to the current user's clinic (unless admin)
    user_obj = db.query(models.User).filter(models.User.id == db_profissional.user_id).first()
    if not current_user.is_superuser and user_obj.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este profissional")

    for key, value in profissional.dict(exclude_unset=True).items():
        setattr(db_profissional, key, value)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

@router.delete("/profissionais/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profissional(profissional_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_profissionais"))):
    db_profissional = db.query(models.Profissional).filter(models.Profissional.id == profissional_id).first()
    if db_profissional is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional não encontrado")
    
    # Check if the professional's user belongs to the current user's clinic (unless admin)
    user_obj = db.query(models.User).filter(models.User.id == db_profissional.user_id).first()
    if not current_user.is_superuser and user_obj.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este profissional")

    db.delete(db_profissional)
    db.commit()
    return {"message": "Profissional deleted successfully"}

# Endpoints para TipoTratamento
@router.post("/tipos-tratamento/", response_model=schemas.TipoTratamentoInDBBase, status_code=status.HTTP_201_CREATED)
def create_tipo_tratamento(tipo_tratamento: schemas.TipoTratamentoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_tipos_tratamento"))):
    if not current_user.is_superuser and tipo_tratamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar tipo de tratamento para esta clínica")
    if tipo_tratamento.clinica_id is None:
        tipo_tratamento.clinica_id = current_user.clinica_id
    db_tipo_tratamento = models.TipoTratamento(**tipo_tratamento.dict())
    db.add(db_tipo_tratamento)
    db.commit()
    db.refresh(db_tipo_tratamento)
    return db_tipo_tratamento

@router.get("/tipos-tratamento/", response_model=List[schemas.TipoTratamentoInDBBase])
def read_tipos_tratamento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_tipos_tratamento"))):
    if current_user.is_superuser:
        tipos_tratamento = db.query(models.TipoTratamento).offset(skip).limit(limit).all()
    else:
        tipos_tratamento = db.query(models.TipoTratamento).filter(models.TipoTratamento.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return tipos_tratamento

@router.get("/tipos-tratamento/{tipo_tratamento_id}", response_model=schemas.TipoTratamentoInDBBase)
def read_tipo_tratamento(tipo_tratamento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_tipos_tratamento"))):
    tipo_tratamento = db.query(models.TipoTratamento).filter(models.TipoTratamento.id == tipo_tratamento_id).first()
    if tipo_tratamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TipoTratamento not found")
    if not current_user.is_superuser and tipo_tratamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este tipo de tratamento")
    return tipo_tratamento

@router.put("/tipos-tratamento/{tipo_tratamento_id}", response_model=schemas.TipoTratamentoInDBBase)
def update_tipo_tratamento(tipo_tratamento_id: int, tipo_tratamento: schemas.TipoTratamentoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_tipos_tratamento"))):
    db_tipo_tratamento = db.query(models.TipoTratamento).filter(models.TipoTratamento.id == tipo_tratamento_id).first()
    if db_tipo_tratamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TipoTratamento not found")
    if not current_user.is_superuser and db_tipo_tratamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este tipo de tratamento")
    for key, value in tipo_tratamento.dict(exclude_unset=True).items():
        setattr(db_tipo_tratamento, key, value)
    db.commit()
    db.refresh(db_tipo_tratamento)
    return db_tipo_tratamento

@router.delete("/tipos-tratamento/{tipo_tratamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_tratamento(tipo_tratamento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_tipos_tratamento"))):
    db_tipo_tratamento = db.query(models.TipoTratamento).filter(models.TipoTratamento.id == tipo_tratamento_id).first()
    if db_tipo_tratamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TipoTratamento not found")
    if not current_user.is_superuser and db_tipo_tratamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este tipo de tratamento")
    db.delete(db_tipo_tratamento)
    db.commit()
    return {"message": "TipoTratamento deleted successfully"}

# Endpoints para Agendamento
@router.post("/agendamentos/", response_model=schemas.AgendamentoInDBBase, status_code=status.HTTP_201_CREATED)
def create_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_agendamentos"))):
    # Ensure the patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar agendamento para este paciente")

    # Ensure the professional belongs to the current user's clinic (unless admin)
    if agendamento.profissional_id:
        profissional = db.query(models.Profissional).filter(models.Profissional.id == agendamento.profissional_id).first()
        if not profissional:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional not found")
        profissional_user = db.query(models.User).filter(models.User.id == profissional.user_id).first()
        if not current_user.is_superuser and profissional_user.clinica_id != current_user.clinica_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar agendamento com este profissional")

    db_agendamento = models.Agendamento(**agendamento.dict())
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

@router.get("/agendamentos/", response_model=List[schemas.AgendamentoInDBBase])
def read_agendamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_agendamentos"))):
    if current_user.is_superuser:
        agendamentos = db.query(models.Agendamento).offset(skip).limit(limit).all()
    else:
        # Filter by patient's clinic, which is linked to the user's clinic
        agendamentos = db.query(models.Agendamento).join(models.Paciente).filter(models.Paciente.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return agendamentos

@router.get("/agendamentos/{agendamento_id}", response_model=schemas.AgendamentoInDBBase)
def read_agendamento(agendamento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_agendamentos"))):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if agendamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento not found")
    
    # Check if the appointment's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este agendamento")
    
    return agendamento

@router.put("/agendamentos/{agendamento_id}", response_model=schemas.AgendamentoInDBBase)
def update_agendamento(agendamento_id: int, agendamento: schemas.AgendamentoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_agendamentos"))):
    db_agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if db_agendamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento not found")
    
    # Check if the appointment's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este agendamento")

    for key, value in agendamento.dict(exclude_unset=True).items():
        setattr(db_agendamento, key, value)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

@router.delete("/agendamentos/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agendamento(agendamento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_agendamentos"))):
    db_agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if db_agendamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento not found")
    
    # Check if the appointment's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este agendamento")

    db.delete(db_agendamento)
    db.commit()
    return {"message": "Agendamento deleted successfully"}

# Endpoints para Atendimento
@router.post("/atendimentos/", response_model=schemas.AtendimentoInDBBase, status_code=status.HTTP_201_CREATED)
def create_atendimento(atendimento: schemas.AtendimentoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_atendimentos"))):
    # Ensure the associated agendamento belongs to the current user's clinic (unless admin)
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento not found")
    
    paciente_agendamento = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente_agendamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar atendimento para este agendamento")

    db_atendimento = models.Atendimento(**atendimento.dict())
    db.add(db_atendimento)
    db.commit()
    db.refresh(db_atendimento)
    return db_atendimento

@router.get("/atendimentos/", response_model=List[schemas.AtendimentoInDBBase])
def read_atendimentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_atendimentos"))):
    if current_user.is_superuser:
        atendimentos = db.query(models.Atendimento).offset(skip).limit(limit).all()
    else:
        # Filter by agendamento's patient's clinic, which is linked to the user's clinic
        atendimentos = db.query(models.Atendimento).join(models.Agendamento).join(models.Paciente).filter(models.Paciente.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return atendimentos

@router.get("/atendimentos/{atendimento_id}", response_model=schemas.AtendimentoInDBBase)
def read_atendimento(atendimento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_atendimentos"))):
    atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == atendimento_id).first()
    if atendimento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento not found")
    
    # Check if the attendance's appointment's patient belongs to the current user's clinic (unless admin)
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
    paciente_agendamento = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente_agendamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este atendimento")

    return atendimento

@router.put("/atendimentos/{atendimento_id}", response_model=schemas.AtendimentoInDBBase)
def update_atendimento(atendimento_id: int, atendimento: schemas.AtendimentoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_atendimentos"))):
    db_atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == atendimento_id).first()
    if db_atendimento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento not found")
    
    # Check if the attendance's appointment's patient belongs to the current user's clinic (unless admin)
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == db_atendimento.agendamento_id).first()
    paciente_agendamento = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente_agendamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este atendimento")

    for key, value in atendimento.dict(exclude_unset=True).items():
        setattr(db_atendimento, key, value)
    db.commit()
    db.refresh(db_atendimento)
    return db_atendimento

@router.delete("/atendimentos/{atendimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_atendimento(atendimento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_atendimentos"))):
    db_atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == atendimento_id).first()
    if db_atendimento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento not found")
    
    # Check if the attendance's appointment's patient belongs to the current user's clinic (unless admin)
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == db_atendimento.agendamento_id).first()
    paciente_agendamento = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente_agendamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este atendimento")

    db.delete(db_atendimento)
    db.commit()
    return {"message": "Atendimento deleted successfully"}

# Endpoints para Prontuario
@router.post("/prontuarios/", response_model=schemas.ProntuarioInDBBase, status_code=status.HTTP_201_CREATED)
def create_prontuario(prontuario: schemas.ProntuarioCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_prontuarios"))):
    # Ensure the patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == prontuario.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar prontuário para este paciente")

    db_prontuario = models.Prontuario(**prontuario.dict())
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)
    return db_prontuario

@router.get("/prontuarios/", response_model=List[schemas.ProntuarioInDBBase])
def read_prontuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_prontuarios"))):
    if current_user.is_superuser:
        prontuarios = db.query(models.Prontuario).offset(skip).limit(limit).all()
    else:
        # Filter by patient's clinic, which is linked to the user's clinic
        prontuarios = db.query(models.Prontuario).join(models.Paciente).filter(models.Paciente.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return prontuarios

@router.get("/prontuarios/{prontuario_id}", response_model=schemas.ProntuarioInDBBase)
def read_prontuario(prontuario_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_prontuarios"))):
    prontuario = db.query(models.Prontuario).filter(models.Prontuario.id == prontuario_id).first()
    if prontuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prontuario not found")
    
    # Check if the medical record's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == prontuario.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este prontuário")

    return prontuario

@router.put("/prontuarios/{prontuario_id}", response_model=schemas.ProntuarioInDBBase)
def update_prontuario(prontuario_id: int, prontuario: schemas.ProntuarioUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_prontuarios"))):
    db_prontuario = db.query(models.Prontuario).filter(models.Prontuario.id == prontuario_id).first()
    if db_prontuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prontuario not found")
    
    # Check if the medical record's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_prontuario.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este prontuário")

    for key, value in prontuario.dict(exclude_unset=True).items():
        setattr(db_prontuario, key, value)
    db.commit()
    db.refresh(db_prontuario)
    return db_prontuario

@router.delete("/prontuarios/{prontuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prontuario(prontuario_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_prontuarios"))):
    db_prontuario = db.query(models.Prontuario).filter(models.Prontuario.id == prontuario_id).first()
    if db_prontuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prontuario not found")
    
    # Check if the medical record's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_prontuario.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este prontuário")

    db.delete(db_prontuario)
    db.commit()
    return {"message": "Prontuario deleted successfully"}

# Endpoints para DocumentoArquivo
@router.post("/documentos/", response_model=schemas.DocumentoArquivoInDBBase, status_code=status.HTTP_201_CREATED)
def create_documento_arquivo(documento: schemas.DocumentoArquivoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_documentos"))):
    # Ensure the associated pasta belongs to the current user's clinic (unless admin)
    pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == documento.pasta_id).first()
    if not pasta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PastaDocumento not found")
    if not current_user.is_superuser and pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar documento para esta pasta")

    # Ensure the associated paciente belongs to the current user's clinic (unless admin)
    if documento.paciente_id:
        paciente = db.query(models.Paciente).filter(models.Paciente.id == documento.paciente_id).first()
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente not found")
        if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar documento para este paciente")

    db_documento = models.DocumentoArquivo(**documento.dict())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

@router.get("/documentos/", response_model=List[schemas.DocumentoArquivoInDBBase])
def read_documentos_arquivo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_documentos"))):
    if current_user.is_superuser:
        documentos = db.query(models.DocumentoArquivo).offset(skip).limit(limit).all()
    else:
        # Filter by pasta's clinic, which is linked to the user's clinic
        documentos = db.query(models.DocumentoArquivo).join(models.PastaDocumento).filter(models.PastaDocumento.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return documentos

@router.get("/documentos/{documento_id}", response_model=schemas.DocumentoArquivoInDBBase)
def read_documento_arquivo(documento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_documentos"))):
    documento = db.query(models.DocumentoArquivo).filter(models.DocumentoArquivo.id == documento_id).first()
    if documento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DocumentoArquivo not found")
    
    # Check if the document's pasta belongs to the current user's clinic (unless admin)
    pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == documento.pasta_id).first()
    if not current_user.is_superuser and pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este documento")

    return documento

@router.put("/documentos/{documento_id}", response_model=schemas.DocumentoArquivoInDBBase)
def update_documento_arquivo(documento_id: int, documento: schemas.DocumentoArquivoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_documento = db.query(models.DocumentoArquivo).filter(models.DocumentoArquivo.id == documento_id).first()
    if db_documento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DocumentoArquivo not found")
    
    # Check if the document's pasta belongs to the current user's clinic (unless admin)
    pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == db_documento.pasta_id).first()
    if not current_user.is_superuser and pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este documento")

    for key, value in documento.dict(exclude_unset=True).items():
        setattr(db_documento, key, value)
    db.commit()
    db.refresh(db_documento)
    return db_documento

@router.delete("/documentos/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_documento_arquivo(documento_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_documento = db.query(models.DocumentoArquivo).filter(models.DocumentoArquivo.id == documento_id).first()
    if db_documento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DocumentoArquivo not found")
    
    # Check if the document's pasta belongs to the current user's clinic (unless admin)
    pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == db_documento.pasta_id).first()
    if not current_user.is_superuser and pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este documento")

    db.delete(db_documento)
    db.commit()
    return {"message": "DocumentoArquivo deleted successfully"}

# Endpoints para PastaDocumento
@router.post("/pastas-documento/", response_model=schemas.PastaDocumentoInDBBase, status_code=status.HTTP_201_CREATED)
def create_pasta_documento(pasta: schemas.PastaDocumentoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_pastas_documento"))):
    if not current_user.is_superuser and pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar pasta de documento para esta clínica")
    if pasta.clinica_id is None:
        pasta.clinica_id = current_user.clinica_id
    db_pasta = models.PastaDocumento(**pasta.dict())
    db.add(db_pasta)
    db.commit()
    db.refresh(db_pasta)
    return db_pasta

@router.get("/pastas-documento/", response_model=List[schemas.PastaDocumentoInDBBase])
def read_pastas_documento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_pastas_documento"))):
    if current_user.is_superuser:
        pastas = db.query(models.PastaDocumento).offset(skip).limit(limit).all()
    else:
        pastas = db.query(models.PastaDocumento).filter(models.PastaDocumento.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return pastas

@router.get("/pastas-documento/{pasta_id}", response_model=schemas.PastaDocumentoInDBBase)
def read_pasta_documento(pasta_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_pastas_documento"))):
    pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == pasta_id).first()
    if pasta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PastaDocumento not found")
    if not current_user.is_superuser and pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar esta pasta de documento")
    return pasta

@router.put("/pastas-documento/{pasta_id}", response_model=schemas.PastaDocumentoInDBBase)
def update_pasta_documento(pasta_id: int, pasta: schemas.PastaDocumentoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_pastas_documento"))):
    db_pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == pasta_id).first()
    if db_pasta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PastaDocumento not found")
    if not current_user.is_superuser and db_pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar esta pasta de documento")
    for key, value in pasta.dict(exclude_unset=True).items():
        setattr(db_pasta, key, value)
    db.commit()
    db.refresh(db_pasta)
    return db_pasta

@router.delete("/pastas-documento/{pasta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pasta_documento(pasta_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_pastas_documento"))):
    db_pasta = db.query(models.PastaDocumento).filter(models.PastaDocumento.id == pasta_id).first()
    if db_pasta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PastaDocumento not found")
    if not current_user.is_superuser and db_pasta.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir esta pasta de documento")
    db.delete(db_pasta)
    db.commit()
    return {"message": "PastaDocumento deleted successfully"}

# Endpoints para CampanhaMarketing
@router.post("/campanhas-marketing/", response_model=schemas.CampanhaMarketingInDBBase, status_code=status.HTTP_201_CREATED)
def create_campanha_marketing(campanha: schemas.CampanhaMarketingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_campanhas_marketing"))):
    if not current_user.is_superuser and campanha.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar campanha de marketing para esta clínica")
    if campanha.clinica_id is None:
        campanha.clinica_id = current_user.clinica_id
    db_campanha = models.CampanhaMarketing(**campanha.dict())
    db.add(db_campanha)
    db.commit()
    db.refresh(db_campanha)
    return db_campanha

@router.get("/campanhas-marketing/", response_model=List[schemas.CampanhaMarketingInDBBase])
def read_campanhas_marketing(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_campanhas_marketing"))):
    if current_user.is_superuser:
        campanhas = db.query(models.CampanhaMarketing).offset(skip).limit(limit).all()
    else:
        campanhas = db.query(models.CampanhaMarketing).filter(models.CampanhaMarketing.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return campanhas

@router.get("/campanhas-marketing/{campanha_id}", response_model=schemas.CampanhaMarketingInDBBase)
def read_campanha_marketing(campanha_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_campanhas_marketing"))):
    campanha = db.query(models.CampanhaMarketing).filter(models.CampanhaMarketing.id == campanha_id).first()
    if campanha is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CampanhaMarketing not found")
    if not current_user.is_superuser and campanha.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar esta campanha de marketing")
    return campanha

@router.put("/campanhas-marketing/{campanha_id}", response_model=schemas.CampanhaMarketingInDBBase)
def update_campanha_marketing(campanha_id: int, campanha: schemas.CampanhaMarketingUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_campanhas_marketing"))):
    db_campanha = db.query(models.CampanhaMarketing).filter(models.CampanhaMarketing.id == campanha_id).first()
    if db_campanha is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CampanhaMarketing not found")
    if not current_user.is_superuser and db_campanha.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar esta campanha de marketing")
    for key, value in campanha.dict(exclude_unset=True).items():
        setattr(db_campanha, key, value)
    db.commit()
    db.refresh(db_campanha)
    return db_campanha

@router.delete("/campanhas-marketing/{campanha_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campanha_marketing(campanha_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_campanhas_marketing"))):
    db_campanha = db.query(models.CampanhaMarketing).filter(models.CampanhaMarketing.id == campanha_id).first()
    if db_campanha is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CampanhaMarketing not found")
    if not current_user.is_superuser and db_campanha.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir esta campanha de marketing")
    db.delete(db_campanha)
    db.commit()
    return {"message": "CampanhaMarketing deleted successfully"}

# Endpoints para Comissao
@router.post("/comissoes/", response_model=schemas.ComissaoInDBBase, status_code=status.HTTP_201_CREATED)
def create_comissao(comissao: schemas.ComissaoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_comissoes"))):
    # Ensure the associated professional belongs to the current user's clinic (unless admin)
    profissional = db.query(models.Profissional).filter(models.Profissional.id == comissao.profissional_id).first()
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional not found")
    profissional_user = db.query(models.User).filter(models.User.id == profissional.user_id).first()
    if not current_user.is_superuser and profissional_user.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar comissão para este profissional")

    # Ensure the associated attendance belongs to the current user's clinic (unless admin)
    atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == comissao.atendimento_id).first()
    if not atendimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento not found")
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == atendimento.agendamento_id).first()
    paciente = db.query(models.Paciente).filter(models.Paciente.id == agendamento.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar comissão para este atendimento")

    db_comissao = models.Comissao(**comissao.dict())
    db.add(db_comissao)
    db.commit()
    db.refresh(db_comissao)
    return db_comissao

@router.get("/comissoes/", response_model=List[schemas.ComissaoInDBBase])
def read_comissoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_comissoes"))):
    if current_user.is_superuser:
        comissoes = db.query(models.Comissao).offset(skip).limit(limit).all()
    else:
        # Filter by professional's clinic, which is linked to the user's clinic
        comissoes = db.query(models.Comissao).join(models.Profissional).join(models.User).filter(models.User.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return comissoes

@router.get("/comissoes/{comissao_id}", response_model=schemas.ComissaoInDBBase)
def read_comissao(comissao_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_comissoes"))):
    comissao = db.query(models.Comissao).filter(models.Comissao.id == comissao_id).first()
    if comissao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comissao not found")
    
    # Check if the commission's professional belongs to the current user's clinic (unless admin)
    profissional = db.query(models.Profissional).filter(models.Profissional.id == comissao.profissional_id).first()
    profissional_user = db.query(models.User).filter(models.User.id == profissional.user_id).first()
    if not current_user.is_superuser and profissional_user.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar esta comissão")

    return comissao

@router.put("/comissoes/{comissao_id}", response_model=schemas.ComissaoInDBBase)
def update_comissao(comissao_id: int, comissao: schemas.ComissaoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_comissoes"))):
    db_comissao = db.query(models.Comissao).filter(models.Comissao.id == comissao_id).first()
    if db_comissao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comissao not found")
    
    # Check if the commission's professional belongs to the current user's clinic (unless admin)
    profissional = db.query(models.Profissional).filter(models.Profissional.id == db_comissao.profissional_id).first()
    profissional_user = db.query(models.User).filter(models.User.id == profissional.user_id).first()
    if not current_user.is_superuser and profissional_user.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar esta comissão")

    for key, value in comissao.dict(exclude_unset=True).items():
        setattr(db_comissao, key, value)
    db.commit()
    db.refresh(db_comissao)
    return db_comissao

@router.delete("/comissoes/{comissao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comissao(comissao_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_comissoes"))):
    db_comissao = db.query(models.Comissao).filter(models.Comissao.id == comissao_id).first()
    if db_comissao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comissao not found")
    
    # Check if the commission's professional belongs to the current user's clinic (unless admin)
    profissional = db.query(models.Profissional).filter(models.Profissional.id == db_comissao.profissional_id).first()
    profissional_user = db.query(models.User).filter(models.User.id == profissional.user_id).first()
    if not current_user.is_superuser and profissional_user.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir esta comissão")

    db.delete(db_comissao)
    db.commit()
    return {"message": "Comissao deleted successfully"}

# Endpoints para Fatura
@router.post("/faturas/", response_model=schemas.FaturaInDBBase, status_code=status.HTTP_201_CREATED)
def create_fatura(fatura: schemas.FaturaCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_faturas"))):
    # Ensure the associated convenio belongs to the current user's clinic (unless admin)
    convenio = db.query(models.Convenio).filter(models.Convenio.id == fatura.convenio_id).first()
    if not convenio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Convenio not found")
    if not current_user.is_superuser and convenio.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar fatura para este convênio")

    db_fatura = models.Fatura(**fatura.dict())
    db.add(db_fatura)
    db.commit()
    db.refresh(db_fatura)
    return db_fatura

@router.get("/faturas/", response_model=List[schemas.FaturaInDBBase])
def read_faturas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_faturas"))):
    if current_user.is_superuser:
        faturas = db.query(models.Fatura).offset(skip).limit(limit).all()
    else:
        # Filter by convenio's clinic, which is linked to the user's clinic
        faturas = db.query(models.Fatura).join(models.Convenio).filter(models.Convenio.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return faturas

@router.get("/faturas/{fatura_id}", response_model=schemas.FaturaInDBBase)
def read_fatura(fatura_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_faturas"))):
    fatura = db.query(models.Fatura).filter(models.Fatura.id == fatura_id).first()
    if fatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fatura not found")
    
    # Check if the invoice's convenio belongs to the current user's clinic (unless admin)
    convenio = db.query(models.Convenio).filter(models.Convenio.id == fatura.convenio_id).first()
    if not current_user.is_superuser and convenio.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar esta fatura")

    return fatura

@router.put("/faturas/{fatura_id}", response_model=schemas.FaturaInDBBase)
def update_fatura(fatura_id: int, fatura: schemas.FaturaUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_faturas"))):
    db_fatura = db.query(models.Fatura).filter(models.Fatura.id == fatura_id).first()
    if db_fatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fatura not found")
    
    # Check if the invoice's convenio belongs to the current user's clinic (unless admin)
    convenio = db.query(models.Convenio).filter(models.Convenio.id == db_fatura.convenio_id).first()
    if not current_user.is_superuser and convenio.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar esta fatura")

    for key, value in fatura.dict(exclude_unset=True).items():
        setattr(db_fatura, key, value)
    db.commit()
    db.refresh(db_fatura)
    return db_fatura

@router.delete("/faturas/{fatura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fatura(fatura_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_faturas"))):
    db_fatura = db.query(models.Fatura).filter(models.Fatura.id == fatura_id).first()
    if db_fatura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fatura not found")
    
    # Check if the invoice's convenio belongs to the current user's clinic (unless admin)
    convenio = db.query(models.Convenio).filter(models.Convenio.id == db_fatura.convenio_id).first()
    if not current_user.is_superuser and convenio.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir esta fatura")

    db.delete(db_fatura)
    db.commit()
    return {"message": "Fatura deleted successfully"}

# Endpoints para PesquisaSatisfacao
@router.post("/pesquisas-satisfacao/", response_model=schemas.PesquisaSatisfacaoInDBBase, status_code=status.HTTP_201_CREATED)
def create_pesquisa_satisfacao(pesquisa: schemas.PesquisaSatisfacaoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_pesquisas_satisfacao"))):
    # Ensure the associated patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == pesquisa.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar pesquisa de satisfação para este paciente")

    if pesquisa.clinica_id is None:
        pesquisa.clinica_id = paciente.clinica_id # Associate with patient's clinic

    db_pesquisa = models.PesquisaSatisfacao(**pesquisa.dict())
    db.add(db_pesquisa)
    db.commit()
    db.refresh(db_pesquisa)
    return db_pesquisa

@router.get("/pesquisas-satisfacao/", response_model=List[schemas.PesquisaSatisfacaoInDBBase])
def read_pesquisas_satisfacao(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_pesquisas_satisfacao"))):
    if current_user.is_superuser:
        pesquisas = db.query(models.PesquisaSatisfacao).offset(skip).limit(limit).all()
    else:
        # Filter by patient's clinic, which is linked to the user's clinic
        pesquisas = db.query(models.PesquisaSatisfacao).join(models.Paciente).filter(models.Paciente.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return pesquisas

@router.get("/pesquisas-satisfacao/{pesquisa_id}", response_model=schemas.PesquisaSatisfacaoInDBBase)
def read_pesquisa_satisfacao(pesquisa_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_pesquisas_satisfacao"))):
    pesquisa = db.query(models.PesquisaSatisfacao).filter(models.PesquisaSatisfacao.id == pesquisa_id).first()
    if pesquisa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PesquisaSatisfacao not found")
    
    # Check if the survey's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == pesquisa.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar esta pesquisa de satisfação")

    return pesquisa

@router.put("/pesquisas-satisfacao/{pesquisa_id}", response_model=schemas.PesquisaSatisfacaoInDBBase)
def update_pesquisa_satisfacao(pesquisa_id: int, pesquisa: schemas.PesquisaSatisfacaoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_pesquisas_satisfacao"))):
    db_pesquisa = db.query(models.PesquisaSatisfacao).filter(models.PesquisaSatisfacao.id == pesquisa_id).first()
    if db_pesquisa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PesquisaSatisfacao not found")
    
    # Check if the survey's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_pesquisa.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar esta pesquisa de satisfação")

    for key, value in pesquisa.dict(exclude_unset=True).items():
        setattr(db_pesquisa, key, value)
    db.commit()
    db.refresh(db_pesquisa)
    return db_pesquisa

@router.delete("/pesquisas-satisfacao/{pesquisa_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_pesquisa_satisfacao(pesquisa_id: int, pesquisa: schemas.PesquisaSatisfacaoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_pesquisas_satisfacao"))):
    db_pesquisa = db.query(models.PesquisaSatisfacao).filter(models.PesquisaSatisfacao.id == pesquisa_id).first()
    if db_pesquisa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PesquisaSatisfacao not found")
    
    # Check if the survey's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_pesquisa.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar esta pesquisa de satisfação")

    for key, value in pesquisa.dict(exclude_unset=True).items():
        setattr(db_pesquisa, key, value)
    db.commit()
    db.refresh(db_pesquisa)
    return db_pesquisa

@router.delete("/pesquisas-satisfacao/{pesquisa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pesquisa_satisfacao(pesquisa_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_pesquisas_satisfacao"))):
    db_pesquisa = db.query(models.PesquisaSatisfacao).filter(models.PesquisaSatisfacao.id == pesquisa_id).first()
    if db_pesquisa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PesquisaSatisfacao not found")
    
    # Check if the survey's patient belongs to the current user's clinic (unless admin)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == db_pesquisa.paciente_id).first()
    if not current_user.is_superuser and paciente.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir esta pesquisa de satisfação")

    db.delete(db_pesquisa)
    db.commit()
    return {"message": "PesquisaSatisfacao deleted successfully"}

# Endpoints para CupomDesconto
@router.post("/cupons-desconto/", response_model=schemas.CupomDescontoInDBBase, status_code=status.HTTP_201_CREATED)
def create_cupom_desconto(cupom: schemas.CupomDescontoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("criar_cupons_desconto"))):
    if not current_user.is_superuser and cupom.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar cupom de desconto para esta clínica")
    if cupom.clinica_id is None:
        cupom.clinica_id = current_user.clinica_id
    db_cupom = models.CupomDesconto(**cupom.dict())
    db.add(db_cupom)
    db.commit()
    db.refresh(db_cupom)
    return db_cupom

@router.get("/cupons-desconto/", response_model=List[schemas.CupomDescontoInDBBase])
def read_cupons_desconto(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_cupons_desconto"))):
    if current_user.is_superuser:
        cupons = db.query(models.CupomDesconto).offset(skip).limit(limit).all()
    else:
        cupons = db.query(models.CupomDesconto).filter(models.CupomDesconto.clinica_id == current_user.clinica_id).offset(skip).limit(limit).all()
    return cupons

@router.get("/cupons-desconto/{cupom_id}", response_model=schemas.CupomDescontoInDBBase)
def read_cupom_desconto(cupom_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("ler_cupons_desconto"))):
    cupom = db.query(models.CupomDesconto).filter(models.CupomDesconto.id == cupom_id).first()
    if cupom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CupomDesconto not found")
    if not current_user.is_superuser and cupom.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a acessar este cupom de desconto")
    return cupom

@router.put("/cupons-desconto/{cupom_id}", response_model=schemas.CupomDescontoInDBBase)
def update_cupom_desconto(cupom_id: int, cupom: schemas.CupomDescontoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("atualizar_cupons_desconto"))):
    db_cupom = db.query(models.CupomDesconto).filter(models.CupomDesconto.id == cupom_id).first()
    if db_cupom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CupomDesconto not found")
    if not current_user.is_superuser and db_cupom.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este cupom de desconto")
    for key, value in cupom.dict(exclude_unset=True).items():
        setattr(db_cupom, key, value)
    db.commit()
    db.refresh(db_cupom)
    return db_cupom

@router.delete("/cupons-desconto/{cupom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cupom_desconto(cupom_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("excluir_cupons_desconto"))):
    db_cupom = db.query(models.CupomDesconto).filter(models.CupomDesconto.id == cupom_id).first()
    if db_cupom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CupomDesconto not found")
    if not current_user.is_superuser and db_cupom.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este cupom de desconto")
    db.delete(db_cupom)
    db.commit()
    return {"message": "CupomDesconto deleted successfully"}