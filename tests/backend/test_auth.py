import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.auth import get_current_user, get_current_active_user, has_permission
from app.core.security import create_access_token
from app.core.database import Base
from app import models
from app.main import app

# Setup a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="test_user")
def test_user_fixture(session: TestingSessionLocal):
    # Create a test user with admin_acesso permission
    permissao_admin = models.Permissao(nome="admin_acesso", descricao="Acesso total de administrador")
    permissao_ler_usuarios = models.Permissao(nome="ler_usuarios", descricao="Permissão para ler usuários")
    perfil_admin = models.Perfil(nome="ADMIN")
    perfil_admin.permissoes.append(permissao_admin)
    perfil_admin.permissoes.append(permissao_ler_usuarios)
    session.add(permissao_admin)
    session.add(permissao_ler_usuarios)
    session.add(perfil_admin)
    session.commit()
    session.refresh(perfil_admin)

    user = models.User(
        username="testuser",
        email="test@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_admin.id,
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="test_token")
def test_token_fixture(test_user: models.User):
    return create_access_token(data={"sub": test_user.username})

@pytest.mark.asyncio
async def test_get_current_user(session: TestingSessionLocal, test_token: str, test_user: models.User):
    # Mock the get_db dependency
    def override_get_db():
        yield session

    from fastapi import Depends
    from app.api.endpoints import get_db
    app.dependency_overrides[get_db] = override_get_db

    current_user = await get_current_user(test_token, session)
    assert current_user.username == test_user.username
    assert current_user.email == test_user.email

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_current_active_user(session: TestingSessionLocal, test_token: str, test_user: models.User):
    def override_get_db():
        yield session

    from fastapi import Depends
    from app.api.endpoints import get_db
    app.dependency_overrides[get_db] = override_get_db

    active_user = await get_current_active_user(test_user)
    assert active_user.username == test_user.username

    test_user.is_active = False
    session.add(test_user)
    session.commit()
    session.refresh(test_user)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_active_user(test_user)
    assert exc_info.value.status_code == 400

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_has_permission(session: TestingSessionLocal, test_user: models.User):
    def override_get_db():
        yield session

    from fastapi import Depends
    from app.api.endpoints import get_db
    app.dependency_overrides[get_db] = override_get_db

    # Test with admin_acesso permission
    permission_checker = has_permission("admin_acesso")
    user_with_permission = await permission_checker(test_user)
    assert user_with_permission.username == test_user.username

    # Test with specific permission
    permission_checker = has_permission("ler_usuarios")
    user_with_permission = await permission_checker(test_user)
    assert user_with_permission.username == test_user.username

    # Test without permission
    perfil_sem_permissao = models.Perfil(nome="USUARIO_COMUM")
    session.add(perfil_sem_permissao)
    session.commit()
    session.refresh(perfil_sem_permissao)

    user_sem_permissao = models.User(
        username="nopermissionuser",
        email="nopermission@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_sem_permissao.id,
        is_active=True
    )
    session.add(user_sem_permissao)
    session.commit()
    session.refresh(user_sem_permissao)

    permission_checker = has_permission("criar_clinicas")
    with pytest.raises(HTTPException) as exc_info:
        await permission_checker(user_sem_permissao)
    assert exc_info.value.status_code == 403

    app.dependency_overrides.clear()