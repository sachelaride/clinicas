import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app import models
from app.core.security import create_access_token, get_password_hash
from datetime import date, datetime

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

@pytest.fixture(name="client")
def client_fixture(session: TestingSessionLocal):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(name="admin_user_token")
def admin_user_token_fixture(session: TestingSessionLocal):
    # Create admin profile and permissions
    permissao_admin_acesso = models.Permissao(nome="admin_acesso", descricao="Acesso total de administrador")
    permissao_criar_clinicas = models.Permissao(nome="criar_clinicas", descricao="Permissão para criar clínicas")
    permissao_ler_clinicas = models.Permissao(nome="ler_clinicas", descricao="Permissão para ler clínicas")
    permissao_atualizar_clinicas = models.Permissao(nome="atualizar_clinicas", descricao="Permissão para atualizar clínicas")
    permissao_excluir_clinicas = models.Permissao(nome="excluir_clinicas", descricao="Permissão para excluir clínicas")
    permissao_criar_perfis = models.Permissao(nome="criar_perfis", descricao="Permissão para criar perfis")
    permissao_ler_perfis = models.Permissao(nome="ler_perfis", descricao="Permissão para ler perfis")
    permissao_atualizar_perfis = models.Permissao(nome="atualizar_perfis", descricao="Permissão para atualizar perfis")
    permissao_excluir_perfis = models.Permissao(nome="excluir_perfis", descricao="Permissão para excluir perfis")
    permissao_criar_permissoes = models.Permissao(nome="criar_permissoes", descricao="Permissão para criar permissões")
    permissao_ler_permissoes = models.Permissao(nome="ler_permissoes", descricao="Permissão para ler permissões")
    permissao_atualizar_permissoes = models.Permissao(nome="atualizar_permissoes", descricao="Permissão para atualizar permissões")
    permissao_excluir_permissoes = models.Permissao(nome="excluir_permissoes", descricao="Permissão para excluir permissões")
    permissao_criar_usuarios = models.Permissao(nome="criar_usuarios", descricao="Permissão para criar usuários")
    permissao_ler_usuarios = models.Permissao(nome="ler_usuarios", descricao="Permissão para ler usuários")
    permissao_atualizar_usuarios = models.Permissao(nome="atualizar_usuarios", descricao="Permissão para atualizar usuários")
    permissao_excluir_usuarios = models.Permissao(nome="excluir_usuarios", descricao="Permissão para excluir usuários")
    permissao_criar_pacientes = models.Permissao(nome="criar_pacientes", descricao="Permissão para criar pacientes")
    permissao_ler_pacientes = models.Permissao(nome="ler_pacientes", descricao="Permissão para ler pacientes")
    permissao_atualizar_pacientes = models.Permissao(nome="atualizar_pacientes", descricao="Permissão para atualizar pacientes")
    permissao_excluir_pacientes = models.Permissao(nome="excluir_pacientes", descricao="Permissão para excluir pacientes")
    permissao_criar_lancamentos_financeiros = models.Permissao(nome="criar_lancamentos_financeiros", descricao="Permissão para criar lançamentos financeiros")
    permissao_ler_lancamentos_financeiros = models.Permissao(nome="ler_lancamentos_financeiros", descricao="Permissão para ler lançamentos financeiros")
    permissao_atualizar_lancamentos_financeiros = models.Permissao(nome="atualizar_lancamentos_financeiros", descricao="Permissão para atualizar lançamentos financeiros")
    permissao_excluir_lancamentos_financeiros = models.Permissao(nome="excluir_lancamentos_financeiros", descricao="Permissão para excluir lançamentos financeiros")
    permissao_criar_leads = models.Permissao(nome="criar_leads", descricao="Permissão para criar leads")
    permissao_ler_leads = models.Permissao(nome="ler_leads", descricao="Permissão para ler leads")
    permissao_atualizar_leads = models.Permissao(nome="atualizar_leads", descricao="Permissão para atualizar leads")
    permissao_excluir_leads = models.Permissao(nome="excluir_leads", descricao="Permissão para excluir leads")
    permissao_criar_profissionais = models.Permissao(nome="criar_profissionais", descricao="Permissão para criar profissionais")
    permissao_ler_profissionais = models.Permissao(nome="ler_profissionais", descricao="Permissão para ler profissionais")
    permissao_atualizar_profissionais = models.Permissao(nome="atualizar_profissionais", descricao="Permissão para atualizar profissionais")
    permissao_excluir_profissionais = models.Permissao(nome="excluir_profissionais", descricao="Permissão para excluir profissionais")
    permissao_criar_tipos_tratamento = models.Permissao(nome="criar_tipos_tratamento", descricao="Permissão para criar tipos de tratamento")
    permissao_ler_tipos_tratamento = models.Permissao(nome="ler_tipos_tratamento", descricao="Permissão para ler tipos de tratamento")
    permissao_atualizar_tipos_tratamento = models.Permissao(nome="atualizar_tipos_tratamento", descricao="Permissão para atualizar tipos de tratamento")
    permissao_excluir_tipos_tratamento = models.Permissao(nome="excluir_tipos_tratamento", descricao="Permissão para excluir tipos de tratamento")
    permissao_criar_agendamentos = models.Permissao(nome="criar_agendamentos", descricao="Permissão para criar agendamentos")
    permissao_ler_agendamentos = models.Permissao(nome="ler_agendamentos", descricao="Permissão para ler agendamentos")
    permissao_atualizar_agendamentos = models.Permissao(nome="atualizar_agendamentos", descricao="Permissão para atualizar agendamentos")
    permissao_excluir_agendamentos = models.Permissao(nome="excluir_agendamentos", descricao="Permissão para excluir agendamentos")

    session.add_all([
        permissao_admin_acesso,
        permissao_criar_clinicas,
        permissao_ler_clinicas,
        permissao_atualizar_clinicas,
        permissao_excluir_clinicas,
        permissao_criar_perfis,
        permissao_ler_perfis,
        permissao_atualizar_perfis,
        permissao_excluir_perfis,
        permissao_criar_permissoes,
        permissao_ler_permissoes,
        permissao_atualizar_permissoes,
        permissao_excluir_permissoes,
        permissao_criar_usuarios,
        permissao_ler_usuarios,
        permissao_atualizar_usuarios,
        permissao_excluir_usuarios,
        permissao_criar_pacientes,
        permissao_ler_pacientes,
        permissao_atualizar_pacientes,
        permissao_excluir_pacientes,
        permissao_criar_lancamentos_financeiros,
        permissao_ler_lancamentos_financeiros,
        permissao_atualizar_lancamentos_financeiros,
        permissao_excluir_lancamentos_financeiros,
        permissao_criar_leads,
        permissao_ler_leads,
        permissao_atualizar_leads,
        permissao_excluir_leads,
        permissao_criar_profissionais,
        permissao_ler_profissionais,
        permissao_atualizar_profissionais,
        permissao_excluir_profissionais,
        permissao_criar_tipos_tratamento,
        permissao_ler_tipos_tratamento,
        permissao_atualizar_tipos_tratamento,
        permissao_excluir_tipos_tratamento,
        permissao_criar_agendamentos,
        permissao_ler_agendamentos,
        permissao_atualizar_agendamentos,
        permissao_excluir_agendamentos
    ])
    session.commit()

    perfil_admin = models.Perfil(nome="ADMIN")
    perfil_admin.permissoes.append(permissao_admin_acesso)
    perfil_admin.permissoes.append(permissao_criar_clinicas)
    perfil_admin.permissoes.append(permissao_ler_clinicas)
    perfil_admin.permissoes.append(permissao_atualizar_clinicas)
    perfil_admin.permissoes.append(permissao_excluir_clinicas)
    perfil_admin.permissoes.append(permissao_criar_perfis)
    perfil_admin.permissoes.append(permissao_ler_perfis)
    perfil_admin.permissoes.append(permissao_atualizar_perfis)
    perfil_admin.permissoes.append(permissao_excluir_perfis)
    perfil_admin.permissoes.append(permissao_criar_permissoes)
    perfil_admin.permissoes.append(permissao_ler_permissoes)
    perfil_admin.permissoes.append(permissao_atualizar_permissoes)
    perfil_admin.permissoes.append(permissao_excluir_permissoes)
    perfil_admin.permissoes.append(permissao_criar_usuarios)
    perfil_admin.permissoes.append(permissao_ler_usuarios)
    perfil_admin.permissoes.append(permissao_atualizar_usuarios)
    perfil_admin.permissoes.append(permissao_excluir_usuarios)
    perfil_admin.permissoes.append(permissao_criar_pacientes)
    perfil_admin.permissoes.append(permissao_ler_pacientes)
    perfil_admin.permissoes.append(permissao_atualizar_pacientes)
    perfil_admin.permissoes.append(permissao_excluir_pacientes)
    perfil_admin.permissoes.append(permissao_criar_lancamentos_financeiros)
    perfil_admin.permissoes.append(permissao_ler_lancamentos_financeiros)
    perfil_admin.permissoes.append(permissao_atualizar_lancamentos_financeiros)
    perfil_admin.permissoes.append(permissao_excluir_lancamentos_financeiros)
    perfil_admin.permissoes.append(permissao_criar_leads)
    perfil_admin.permissoes.append(permissao_ler_leads)
    perfil_admin.permissoes.append(permissao_atualizar_leads)
    perfil_admin.permissoes.append(permissao_excluir_leads)
    perfil_admin.permissoes.append(permissao_criar_profissionais)
    perfil_admin.permissoes.append(permissao_ler_profissionais)
    perfil_admin.permissoes.append(permissao_atualizar_profissionais)
    perfil_admin.permissoes.append(permissao_excluir_profissionais)
    perfil_admin.permissoes.append(permissao_criar_tipos_tratamento)
    perfil_admin.permissoes.append(permissao_ler_tipos_tratamento)
    perfil_admin.permissoes.append(permissao_atualizar_tipos_tratamento)
    perfil_admin.permissoes.append(permissao_excluir_tipos_tratamento)
    perfil_admin.permissoes.append(permissao_criar_agendamentos)
    perfil_admin.permissoes.append(permissao_ler_agendamentos)
    perfil_admin.permissoes.append(permissao_atualizar_agendamentos)
    perfil_admin.permissoes.append(permissao_excluir_agendamentos)
    session.add(perfil_admin)
    session.commit()
    session.refresh(perfil_admin)

    # Create admin user
    admin_user = models.User(
        username="admin",
        email="admin@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_admin.id,
        is_active=True,
        is_superuser=True
    )
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)

    return create_access_token(data={"sub": admin_user.username})

@pytest.fixture(name="common_user_token")
def common_user_token_fixture(session: TestingSessionLocal):
    # Create a common user profile without any specific permissions
    perfil_comum = models.Perfil(nome="COMUM")
    session.add(perfil_comum)
    session.commit()
    session.refresh(perfil_comum)

    common_user = models.User(
        username="commonuser",
        email="common@example.com",
        hashed_password=get_password_hash("commonpassword"),
        perfil_id=perfil_comum.id,
        is_active=True
    )
    session.add(common_user)
    session.commit()
    session.refresh(common_user)

    return create_access_token(data={"sub": common_user.username})

@pytest.fixture(name="test_clinica")
def test_clinica_fixture(session: TestingSessionLocal):
    clinica = models.Clinica(
        nome="Clinica Teste",
        endereco="Rua Teste, 123",
        telefone="11987654321",
        num_guiches=2,
        tempo_minimo_atendimento=30
    )
    session.add(clinica)
    session.commit()
    session.refresh(clinica)
    return clinica

# Tests for /clinicas endpoints
def test_create_clinica(client: TestClient, admin_user_token: str):
    response = client.post(
        "/api/clinicas/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Clinica Teste",
            "endereco": "Rua Teste, 123",
            "telefone": "11987654321",
            "num_guiches": 2,
            "tempo_minimo_atendimento": 30
        }
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Clinica Teste"

def test_read_clinicas(client: TestClient, admin_user_token: str):
    # Create a clinic first
    client.post(
        "/api/clinicas/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Clinica Leitura",
            "endereco": "Rua Leitura, 456",
            "telefone": "11912345678",
            "num_guiches": 1,
            "tempo_minimo_atendimento": 20
        }
    )

    response = client.get(
        "/api/clinicas/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(c["nome"] == "Clinica Leitura" for c in response.json())

def test_read_clinica_by_id(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a clinic first
    new_clinica = models.Clinica(
        nome="Clinica ID",
        endereco="Rua ID, 789",
        telefone="11998765432",
        num_guiches=3,
        tempo_minimo_atendimento=40
    )
    session.add(new_clinica)
    session.commit()
    session.refresh(new_clinica)

    response = client.get(
        f"/api/clinicas/{new_clinica.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Clinica ID"

def test_update_clinica(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a clinic first
    clinica_to_update = models.Clinica(
        nome="Clinica Antiga",
        endereco="Rua Antiga, 1",
        telefone="11111111111",
        num_guiches=1,
        tempo_minimo_atendimento=15
    )
    session.add(clinica_to_update)
    session.commit()
    session.refresh(clinica_to_update)

    response = client.put(
        f"/api/clinicas/{clinica_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Clinica Atualizada",
            "telefone": "22222222222"
        }
  )
    assert response.status_code == 200
    assert response.json()["nome"] == "Clinica Atualizada"
    assert response.json()["telefone"] == "22222222222"

def test_delete_clinica(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a clinic first
    clinica_to_delete = models.Clinica(
        nome="Clinica para Deletar",
        endereco="Rua Deletar, 99",
        telefone="33333333333",
        num_guiches=1,
        tempo_minimo_atendimento=10
    )
    session.add(clinica_to_delete)
    session.commit()
    session.refresh(clinica_to_delete)

    response = client.delete(
        f"/api/clinicas/{clinica_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/clinicas/{clinica_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /clinicas endpoints
def test_create_clinica_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.post(
        "/api/clinicas/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Clinica Sem Permissao",
            "endereco": "Rua Sem Permissao, 1",
            "telefone": "11000000000",
            "num_guiches": 1,
            "tempo_minimo_atendimento": 10
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_clinicas"

def test_read_clinicas_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/clinicas/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_clinicas"

def test_update_clinica_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a clinic first
    clinica_to_update = models.Clinica(
        nome="Clinica Permissao Update",
        endereco="Rua Permissao Update, 1",
        telefone="11111111111",
        num_guiches=1,
        tempo_minimo_atendimento=15
    )
    session.add(clinica_to_update)
    session.commit()
    session.refresh(clinica_to_update)

    response = client.put(
        f"/api/clinicas/{clinica_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Clinica Atualizada Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_clinicas"

def test_delete_clinica_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a clinic first
    clinica_to_delete = models.Clinica(
        nome="Clinica Permissao Delete",
        endereco="Rua Permissao Delete, 99",
        telefone="33333333333",
        num_guiches=1,
        tempo_minimo_atendimento=10
    )
    session.add(clinica_to_delete)
    session.commit()
    session.refresh(clinica_to_delete)

    response = client.delete(
        f"/api/clinicas/{clinica_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_clinicas"

# Tests for /perfis endpoints
def test_create_perfil(client: TestClient, admin_user_token: str):
    response = client.post(
        "/api/perfis/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Perfil Teste"
        }
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Perfil Teste"

def test_read_perfis(client: TestClient, admin_user_token: str):
    # Create a perfil first
    client.post(
        "/api/perfis/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Perfil Leitura"
        }
    )

    response = client.get(
        "/api/perfis/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(p["nome"] == "Perfil Leitura" for p in response.json())

def test_read_perfil_by_id(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a perfil first
    new_perfil = models.Perfil(
        nome="Perfil ID"
    )
    session.add(new_perfil)
    session.commit()
    session.refresh(new_perfil)

    response = client.get(
        f"/api/perfis/{new_perfil.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Perfil ID"

def test_update_perfil(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a perfil first
    perfil_to_update = models.Perfil(
        nome="Perfil Antigo"
    )
    session.add(perfil_to_update)
    session.commit()
    session.refresh(perfil_to_update)

    # Create a permission to add to the profile
    permissao_teste = models.Permissao(nome="permissao_teste", descricao="Permissão de Teste")
    session.add(permissao_teste)
    session.commit()
    session.refresh(permissao_teste)

    response = client.put(
        f"/api/perfis/{perfil_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Perfil Atualizado",
            "permissoes": [permissao_teste.id]
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Perfil Atualizado"
    assert any(p["nome"] == "permissao_teste" for p in response.json()["permissoes"])

def test_delete_perfil(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a perfil first
    perfil_to_delete = models.Perfil(
        nome="Perfil para Deletar"
    )
    session.add(perfil_to_delete)
    session.commit()
    session.refresh(perfil_to_delete)

    response = client.delete(
        f"/api/perfis/{perfil_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/perfis/{perfil_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /perfis endpoints
def test_create_perfil_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.post(
        "/api/perfis/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Perfil Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_perfis"

def test_read_perfis_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/perfis/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_perfis"

def test_update_perfil_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a perfil first
    perfil_to_update = models.Perfil(
        nome="Perfil Permissao Update"
    )
    session.add(perfil_to_update)
    session.commit()
    session.refresh(perfil_to_update)

    response = client.put(
        f"/api/perfis/{perfil_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Perfil Atualizado Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_perfis"

def test_delete_perfil_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a perfil first
    perfil_to_delete = models.Perfil(
        nome="Perfil Permissao Delete"
    )
    session.add(perfil_to_delete)
    session.commit()
    session.refresh(perfil_to_delete)

    response = client.delete(
        f"/api/perfis/{perfil_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_perfis"

# Tests for /permissoes endpoints
def test_create_permissao(client: TestClient, admin_user_token: str):
    response = client.post(
        "/api/permissoes/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Permissao Teste",
            "descricao": "Descricao da Permissao Teste"
        }
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Permissao Teste"

def test_read_permissoes(client: TestClient, admin_user_token: str):
    # Create a permissao first
    client.post(
        "/api/permissoes/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Permissao Leitura",
            "descricao": "Descricao da Permissao Leitura"
        }
    )

    response = client.get(
        "/api/permissoes/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(p["nome"] == "Permissao Leitura" for p in response.json())

def test_read_permissao_by_id(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a permissao first
    new_permissao = models.Permissao(
        nome="Permissao ID",
        descricao="Descricao da Permissao ID"
    )
    session.add(new_permissao)
    session.commit()
    session.refresh(new_permissao)

    response = client.get(
        f"/api/permissoes/{new_permissao.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Permissao ID"

def test_update_permissao(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a permissao first
    permissao_to_update = models.Permissao(
        nome="Permissao Antiga",
        descricao="Descricao Antiga"
    )
    session.add(permissao_to_update)
    session.commit()
    session.refresh(permissao_to_update)

    response = client.put(
        f"/api/permissoes/{permissao_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Permissao Atualizada",
            "descricao": "Descricao Atualizada"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Permissao Atualizada"
    assert response.json()["descricao"] == "Descricao Atualizada"

def test_delete_permissao(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a permissao first
    permissao_to_delete = models.Permissao(
        nome="Permissao para Deletar",
        descricao="Descricao para Deletar"
    )
    session.add(permissao_to_delete)
    session.commit()
    session.refresh(permissao_to_delete)

    response = client.delete(
        f"/api/permissoes/{permissao_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/permissoes/{permissao_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /permissoes endpoints
def test_create_permissao_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.post(
        "/api/permissoes/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Permissao Sem Permissao",
            "descricao": "Descricao Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_permissoes"

def test_read_permissoes_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/permissoes/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_permissoes"

def test_update_permissao_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a permissao first
    permissao_to_update = models.Permissao(
        nome="Permissao Permissao Update",
        descricao="Descricao Permissao Update"
    )
    session.add(permissao_to_update)
    session.commit()
    session.refresh(permissao_to_update)

    response = client.put(
        f"/api/permissoes/{permissao_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Permissao Atualizada Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_permissoes"

def test_delete_permissao_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a permissao first
    permissao_to_delete = models.Permissao(
        nome="Permissao Permissao Delete",
        descricao="Descricao Permissao Delete"
    )
    session.add(permissao_to_delete)
    session.commit()
    session.refresh(permissao_to_delete)

    response = client.delete(
        f"/api/permissoes/{permissao_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_permissoes"

# Tests for /users endpoints
def test_create_user(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a profile for the new user
    perfil_novo_user = models.Perfil(nome="NOVO_USER_PERFIL")
    session.add(perfil_novo_user)
    session.commit()
    session.refresh(perfil_novo_user)

    response = client.post(
        "/api/users/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "perfil_id": perfil_novo_user.id,
            "is_active": True
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "newuser@example.com"

def test_read_users_me(client: TestClient, admin_user_token: str):
    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "admin"

def test_read_users(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a user first
    perfil_leitura_user = models.Perfil(nome="LEITURA_USER_PERFIL")
    session.add(perfil_leitura_user)
    session.commit()
    session.refresh(perfil_leitura_user)

    user_leitura = models.User(
        username="userleitura",
        email="userleitura@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_leitura_user.id,
        is_active=True
    )
    session.add(user_leitura)
    session.commit()
    session.refresh(user_leitura)

    response = client.get(
        "/api/users/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(u["username"] == "userleitura" for u in response.json())

def test_read_user_by_id(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a user first
    perfil_id_user = models.Perfil(nome="ID_USER_PERFIL")
    session.add(perfil_id_user)
    session.commit()
    session.refresh(perfil_id_user)

    user_id = models.User(
        username="userid",
        email="userid@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_id_user.id,
        is_active=True
    )
    session.add(user_id)
    session.commit()
    session.refresh(user_id)

    response = client.get(
        f"/api/users/{user_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "userid"

def test_update_user(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a user first
    perfil_update_user = models.Perfil(nome="UPDATE_USER_PERFIL")
    session.add(perfil_update_user)
    session.commit()
    session.refresh(perfil_update_user)

    user_to_update = models.User(
        username="userantigo",
        email="userantigo@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_update_user.id,
        is_active=True
    )
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    response = client.put(
        f"/api/users/{user_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "username": "useratualizado",
            "email": "useratualizado@example.com"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "useratualizado"
    assert response.json()["email"] == "useratualizado@example.com"

def test_delete_user(client: TestClient, admin_user_token: str, session: TestingSessionLocal):
    # Create a user first
    perfil_delete_user = models.Perfil(nome="DELETE_USER_PERFIL")
    session.add(perfil_delete_user)
    session.commit()
    session.refresh(perfil_delete_user)

    user_to_delete = models.User(
        username="userdeletar",
        email="userdeletar@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_delete_user.id,
        is_active=True
    )
    session.add(user_to_delete)
    session.commit()
    session.refresh(user_to_delete)

    response = client.delete(
        f"/api/users/{user_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/users/{user_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /users endpoints
def test_create_user_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    # Create a profile for the new user
    perfil_novo_user = models.Perfil(nome="NOVO_USER_PERFIL_DENIED")
    session.add(perfil_novo_user)
    session.commit()
    session.refresh(perfil_novo_user)

    response = client.post(
        "/api/users/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "username": "newuser_denied",
            "email": "newuser_denied@example.com",
            "password": "newpassword_denied",
            "perfil_id": perfil_novo_user.id,
            "is_active": True
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_usuarios"

def test_read_users_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/users/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_usuarios"

def test_update_user_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a user first
    perfil_update_user = models.Perfil(nome="UPDATE_USER_PERFIL_DENIED")
    session.add(perfil_update_user)
    session.commit()
    session.refresh(perfil_update_user)

    user_to_update = models.User(
        username="userantigo_denied",
        email="userantigo_denied@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_update_user.id,
        is_active=True
    )
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    response = client.put(
        f"/api/users/{user_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "username": "useratualizado_denied"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_usuarios"

def test_delete_user_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str):
    # Create a user first
    perfil_delete_user = models.Perfil(nome="DELETE_USER_PERFIL_DENIED")
    session.add(perfil_delete_user)
    session.commit()
    session.refresh(perfil_delete_user)

    user_to_delete = models.User(
        username="userdeletar_denied",
        email="userdeletar_denied@example.com",
        hashed_password="fakehashedpassword",
        perfil_id=perfil_delete_user.id,
        is_active=True
    )
    session.add(user_to_delete)
    session.commit()
    session.refresh(user_to_delete)

    response = client.delete(
        f"/api/users/{user_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_usuarios"

# Tests for /pacientes endpoints
def test_create_paciente(client: TestClient, admin_user_token: str, test_clinica: models.Clinica):
    response = client.post(
        "/api/pacientes/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Paciente Teste",
            "cpf": "123.456.789-00",
            "data_nascimento": "2000-01-01",
            "email": "paciente@example.com",
            "clinica_id": test_clinica.id
        }
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Paciente Teste"

def test_read_pacientes(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a patient first
    paciente_leitura = models.Paciente(
        nome="Paciente Leitura",
        cpf="987.654.321-00",
        data_nascimento=date(1990, 5, 10),
        email="leitura@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente_leitura)
    session.commit()
    session.refresh(paciente_leitura)

    response = client.get(
        "/api/pacientes/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(p["nome"] == "Paciente Leitura" for p in response.json())

def test_read_paciente_by_id(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a patient first
    paciente_id = models.Paciente(
        nome="Paciente ID",
        cpf="111.222.333-44",
        data_nascimento=date(1985, 11, 20),
        email="pacienteid@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente_id)
    session.commit()
    session.refresh(paciente_id)

    response = client.get(
        f"/api/pacientes/{paciente_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Paciente ID"

def test_update_paciente(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a patient first
    paciente_to_update = models.Paciente(
        nome="Paciente Antigo",
        cpf="555.666.777-88",
        data_nascimento=date(1970, 1, 1),
        email="pacienteantigo@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente_to_update)
    session.commit()
    session.refresh(paciente_to_update)

    response = client.put(
        f"/api/pacientes/{paciente_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Paciente Atualizado",
            "email": "pacienteatualizado@example.com"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Paciente Atualizado"
    assert response.json()["email"] == "pacienteatualizado@example.com"

def test_delete_paciente(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a patient first
    paciente_to_delete = models.Paciente(
        nome="Paciente para Deletar",
        cpf="999.888.777-66",
        data_nascimento=date(2005, 3, 15),
        email="pacientedeletar@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente_to_delete)
    session.commit()
    session.refresh(paciente_to_delete)

    response = client.delete(
        f"/api/pacientes/{paciente_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/pacientes/{paciente_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /pacientes endpoints
def test_create_paciente_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    response = client.post(
        "/api/pacientes/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Paciente Sem Permissao",
            "cpf": "123.123.123-12",
            "data_nascimento": "2001-01-01",
            "email": "sempermissao@example.com",
            "clinica_id": test_clinica.id
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_pacientes"

def test_read_pacientes_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/pacientes/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_pacientes"

def test_update_paciente_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a patient first
    paciente_to_update = models.Paciente(
        nome="Paciente Permissao Update",
        cpf="123.456.789-11",
        data_nascimento=date(1995, 7, 7),
        email="updateperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente_to_update)
    session.commit()
    session.refresh(paciente_to_update)

    response = client.put(
        f"/api/pacientes/{paciente_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Paciente Atualizado Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_pacientes"

def test_delete_paciente_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a patient first
    paciente_to_delete = models.Paciente(
        nome="Paciente Permissao Delete",
        cpf="123.456.789-22",
        data_nascimento=date(1980, 2, 2),
        email="deleteperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente_to_delete)
    session.commit()
    session.refresh(paciente_to_delete)

    response = client.delete(
        f"/api/pacientes/{paciente_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_pacientes"

# Tests for /lancamentos-financeiros endpoints
def test_create_lancamento_financeiro(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a patient and an appointment for the financial entry
    paciente = models.Paciente(
        nome="Paciente Lancamento",
        cpf="111.111.111-11",
        data_nascimento=date(1990, 1, 1),
        email="lancamento@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_CREATE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lanc",
        email="prof_lanc@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12345"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 10, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    response = client.post(
        "/api/lancamentos-financeiros/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "tipo": "RECEITA",
            "descricao": "Consulta",
            "valor": 150.00,
            "data_vencimento": "2024-08-10",
            "atendimento_id": atendimento.id
        }
    )
    assert response.status_code == 201
    assert response.json()["descricao"] == "Consulta"

def test_read_lancamentos_financeiros(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a financial entry first
    paciente = models.Paciente(
        nome="Paciente LF Leitura",
        cpf="222.222.222-22",
        data_nascimento=date(1991, 2, 2),
        email="lfleitura@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_READ")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_leitura",
        email="prof_lf_leitura@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12346"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 11, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento leitura",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    lancamento_leitura = models.LancamentoFinanceiro(
        tipo="DESPESA",
        descricao="Aluguel",
        valor=1000.00,
        data_vencimento=date(2024, 8, 1),
        atendimento_id=atendimento.id
    )
    session.add(lancamento_leitura)
    session.commit()
    session.refresh(lancamento_leitura)

    response = client.get(
        "/api/lancamentos-financeiros/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(l["descricao"] == "Aluguel" for l in response.json())

def test_read_lancamento_financeiro_by_id(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a financial entry first
    paciente = models.Paciente(
        nome="Paciente LF ID",
        cpf="333.333.333-33",
        data_nascimento=date(1992, 3, 3),
        email="lfid@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_ID")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_id",
        email="prof_lf_id@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12347"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 12, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento id",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    lancamento_id = models.LancamentoFinanceiro(
        tipo="RECEITA",
        descricao="Serviço Extra",
        valor=200.00,
        data_vencimento=date(2024, 8, 12),
        atendimento_id=atendimento.id
    )
    session.add(lancamento_id)
    session.commit()
    session.refresh(lancamento_id)

    response = client.get(
        f"/api/lancamentos-financeiros/{lancamento_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["descricao"] == "Serviço Extra"

def test_update_lancamento_financeiro(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a financial entry first
    paciente = models.Paciente(
        nome="Paciente LF Update",
        cpf="444.444.444-44",
        data_nascimento=date(1993, 4, 4),
        email="lfupdate@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_UPDATE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_update",
        email="prof_lf_update@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12348"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 13, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento update",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    lancamento_to_update = models.LancamentoFinanceiro(
        tipo="RECEITA",
        descricao="Serviço Antigo",
        valor=50.00,
        data_vencimento=date(2024, 8, 13),
        atendimento_id=atendimento.id
    )
    session.add(lancamento_to_update)
    session.commit()
    session.refresh(lancamento_to_update)

    response = client.put(
        f"/api/lancamentos-financeiros/{lancamento_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "descricao": "Serviço Novo",
            "valor": 75.00
        }
    )
    assert response.status_code == 200
    assert response.json()["descricao"] == "Serviço Novo"
    assert float(response.json()["valor"]) == 75.00

def test_delete_lancamento_financeiro(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a financial entry first
    paciente = models.Paciente(
        nome="Paciente LF Delete",
        cpf="555.555.555-55",
        data_nascimento=date(1994, 5, 5),
        email="lfdelete@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_DELETE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_delete",
        email="prof_lf_delete@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12349"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 14, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento delete",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    lancamento_to_delete = models.LancamentoFinanceiro(
        tipo="DESPESA",
        descricao="Material",
        valor=120.00,
        data_vencimento=date(2024, 8, 14),
        atendimento_id=atendimento.id
    )
    session.add(lancamento_to_delete)
    session.commit()
    session.refresh(lancamento_to_delete)

    response = client.delete(
        f"/api/lancamentos-financeiros/{lancamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/lancamentos-financeiros/{lancamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /lancamentos-financeiros endpoints
def test_create_lancamento_financeiro_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a patient and an appointment for the financial entry
    paciente = models.Paciente(
        nome="Paciente LF Sem Perm",
        cpf="666.666.666-66",
        data_nascimento=date(1990, 1, 1),
        email="lfsemperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_CREATE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_semperm",
        email="prof_lf_semperm@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=user_prof.id,
        data=datetime(2024, 8, 15, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento sem perm",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    response = client.post(
        "/api/lancamentos-financeiros/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "tipo": "RECEITA",
            "descricao": "Consulta Sem Permissao",
            "valor": 100.00,
            "data_vencimento": "2024-08-15",
            "atendimento_id": atendimento.id
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_lancamentos_financeiros"

def test_read_lancamentos_financeiros_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/lancamentos-financeiros/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_lancamentos_financeiros"

def test_update_lancamento_financeiro_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a financial entry first
    paciente = models.Paciente(
        nome="Paciente LF Update Sem Perm",
        cpf="777.777.777-77",
        data_nascimento=date(1990, 1, 1),
        email="lfupdatesemperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_UPDATE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_update_semperm",
        email="prof_lf_update_semperm@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12351"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 16, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento update sem perm",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    lancamento_to_update = models.LancamentoFinanceiro(
        tipo="RECEITA",
        descricao="Serviço Antigo Sem Permissao",
        valor=50.00,
        data_vencimento=date(2024, 8, 16),
        atendimento_id=atendimento.id
    )
    session.add(lancamento_to_update)
    session.commit()
    session.refresh(lancamento_to_update)

    response = client.put(
        f"/api/lancamentos-financeiros/{lancamento_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "descricao": "Serviço Novo Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_lancamentos_financeiros"

def test_delete_lancamento_financeiro_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a financial entry first
    paciente = models.Paciente(
        nome="Paciente LF Delete Sem Perm",
        cpf="888.888.888-88",
        data_nascimento=date(1990, 1, 1),
        email="lfdeletesemperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_LF_DELETE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_lf_delete",
        email="prof_lf_delete@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12352"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 8, 17, 10, 0, 0), # Convert to datetime object
        status="AGENDADO"
    )
    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)

    atendimento = models.Atendimento(
        agendamento_id=agendamento.id,
        observacoes="Atendimento para lancamento delete",
        status="FINALIZADO"
    )
    session.add(atendimento)
    session.commit()
    session.refresh(atendimento)

    lancamento_to_delete = models.LancamentoFinanceiro(
        tipo="DESPESA",
        descricao="Material Sem Permissao",
        valor=120.00,
        data_vencimento=date(2024, 8, 17),
        atendimento_id=atendimento.id
    )
    session.add(lancamento_to_delete)
    session.commit()
    session.refresh(lancamento_to_delete)

    response = client.delete(
        f"/api/lancamentos-financeiros/{lancamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_lancamentos_financeiros"

# Tests for /leads endpoints
def test_create_lead(client: TestClient, admin_user_token: str, test_clinica: models.Clinica):
    response = client.post(
        "/api/leads/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Lead Teste",
            "email": "lead@example.com",
            "telefone": "11987654321",
            "origem": "Website",
            "status": "NOVO",
            "clinica_id": test_clinica.id
        }
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Lead Teste"

def test_read_leads(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a lead first
    lead_leitura = models.Lead(
        nome="Lead Leitura",
        email="leadleitura@example.com",
        telefone="11912345678",
        origem="Telefone",
        status="CONTATO",
        clinica_id=test_clinica.id
    )
    session.add(lead_leitura)
    session.commit()
    session.refresh(lead_leitura)

    response = client.get(
        "/api/leads/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(l["nome"] == "Lead Leitura" for l in response.json())

def test_read_lead_by_id(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a lead first
    lead_id = models.Lead(
        nome="Lead ID",
        email="leadid@example.com",
        telefone="11998765432",
        origem="Email",
        status="QUALIFICADO",
        clinica_id=test_clinica.id
    )
    session.add(lead_id)
    session.commit()
    session.refresh(lead_id)

    response = client.get(
        f"/api/leads/{lead_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Lead ID"

def test_update_lead(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a lead first
    lead_to_update = models.Lead(
        nome="Lead Antigo",
        email="leadantigo@example.com",
        telefone="11111111111",
        origem="Evento",
        status="NOVO",
        clinica_id=test_clinica.id
    )
    session.add(lead_to_update)
    session.commit()
    session.refresh(lead_to_update)

    response = client.put(
        f"/api/leads/{lead_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Lead Atualizado",
            "status": "CONVERTIDO"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Lead Atualizado"
    assert response.json()["status"] == "CONVERTIDO"

def test_delete_lead(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a lead first
    lead_to_delete = models.Lead(
        nome="Lead para Deletar",
        email="leaddeletar@example.com",
        telefone="11222222222",
        origem="Indicação",
        status="PERDIDO",
        clinica_id=test_clinica.id
    )
    session.add(lead_to_delete)
    session.commit()
    session.refresh(lead_to_delete)

    response = client.delete(
        f"/api/leads/{lead_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/leads/{lead_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /leads endpoints
def test_create_lead_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    response = client.post(
        "/api/leads/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Lead Sem Permissao",
            "email": "leadsemperm@example.com",
            "telefone": "11333333333",
            "origem": "Outro",
            "status": "NOVO",
            "clinica_id": test_clinica.id
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_leads"

def test_read_leads_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/leads/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_leads"

def test_update_lead_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a lead first
    lead_to_update = models.Lead(
        nome="Lead Permissao Update",
        email="leadupdateperm@example.com",
        telefone="11444444444",
        origem="Website",
        status="NOVO",
        clinica_id=test_clinica.id
    )
    session.add(lead_to_update)
    session.commit()
    session.refresh(lead_to_update)

    response = client.put(
        f"/api/leads/{lead_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Lead Atualizado Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_leads"

def test_delete_lead_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a lead first
    lead_to_delete = models.Lead(
        nome="Lead Permissao Delete",
        email="leaddeleteperm@example.com",
        telefone="11555555555",
        origem="Indicação",
        status="NOVO",
        clinica_id=test_clinica.id
    )
    session.add(lead_to_delete)
    session.commit()
    session.refresh(lead_to_delete)

    response = client.delete(
        f"/api/leads/{lead_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_leads"

# Tests for /profissionais endpoints
def test_create_profissional(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_CREATE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_create",
        email="prof_create@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    response = client.post(
        "/api/profissionais/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "user_id": user_prof.id,
            "especialidade": "Cardiologia",
            "conselho_profissional": "CRM",
            "numero_conselho": "123456",
            "carga_horaria_semanal": 40,
            "comissao_percentual": 10.00
        }
    )
    assert response.status_code == 201
    assert response.json()["user_id"] == user_prof.id
    assert response.json()["especialidade"] == "Cardiologia"

def test_read_profissionais(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a professional first
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_READ")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_read",
        email="prof_read@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional_read = models.Profissional(
        user_id=user_prof.id,
        especialidade="Dermatologia",
        conselho_profissional="CRM",
        numero_conselho="654321"
    )
    session.add(profissional_read)
    session.commit()
    session.refresh(profissional_read)

    response = client.get(
        "/api/profissionais/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(p["especialidade"] == "Dermatologia" for p in response.json())

def test_read_profissional_by_id(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a professional first
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_ID")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_id",
        email="prof_id@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional_id = models.Profissional(
        user_id=user_prof.id,
        especialidade="Pediatria",
        conselho_profissional="CRM",
        numero_conselho="987654"
    )
    session.add(profissional_id)
    session.commit()
    session.refresh(profissional_id)

    response = client.get(
        f"/api/profissionais/{profissional_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["especialidade"] == "Pediatria"

def test_update_profissional(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a professional first
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_UPDATE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_update",
        email="prof_update@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional_to_update = models.Profissional(
        user_id=user_prof.id,
        especialidade="Oftalmologia",
        conselho_profissional="CRM",
        numero_conselho="112233"
    )
    session.add(profissional_to_update)
    session.commit()
    session.refresh(profissional_to_update)

    response = client.put(
        f"/api/profissionais/{profissional_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "especialidade": "Gastroenterologia",
            "carga_horaria_semanal": 30
        }
    )
    assert response.status_code == 200
    assert response.json()["especialidade"] == "Gastroenterologia"
    assert response.json()["carga_horaria_semanal"] == 30

def test_delete_profissional(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a professional first
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_DELETE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_delete",
        email="prof_delete@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional_to_delete = models.Profissional(
        user_id=user_prof.id,
        especialidade="Psicologia",
        conselho_profissional="CRP",
        numero_conselho="445566"
    )
    session.add(profissional_to_delete)
    session.commit()
    session.refresh(profissional_to_delete)

    response = client.delete(
        f"/api/profissionais/{profissional_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/profissionais/{profissional_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /profissionais endpoints
def test_create_profissional_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a Perfil for the professional
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_CREATE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    # Create a User for the professional
    user_prof = models.User(
        username="prof_create_denied",
        email="prof_create_denied@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    response = client.post(
        "/api/profissionais/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "user_id": user_prof.id,
            "especialidade": "Cardiologia",
            "conselho_profissional": "CRM",
            "numero_conselho": "123456",
            "carga_horaria_semanal": 40,
            "comissao_percentual": 10.00
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_profissionais"

def test_read_profissionais_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/profissionais/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_profissionais"

def test_update_profissional_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a professional first
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_UPDATE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_update_denied",
        email="prof_update_denied@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional_to_update = models.Profissional(
        user_id=user_prof.id,
        especialidade="Oftalmologia",
        conselho_profissional="CRM",
        numero_conselho="112233"
    )
    session.add(profissional_to_update)
    session.commit()
    session.refresh(profissional_to_update)

    response = client.put(
        f"/api/profissionais/{profissional_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "especialidade": "Gastroenterologia"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_profissionais"

def test_delete_profissional_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a professional first
    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_DELETE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_delete_denied",
        email="prof_delete_denied@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional_to_delete = models.Profissional(
        user_id=user_prof.id,
        especialidade="Psicologia",
        conselho_profissional="CRP",
        numero_conselho="445566"
    )
    session.add(profissional_to_delete)
    session.commit()
    session.refresh(profissional_to_delete)

    response = client.delete(
        f"/api/profissionais/{profissional_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_profissionais"

# Tests for /tipos-tratamento endpoints
def test_create_tipo_tratamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica):
    response = client.post(
        "/api/tipos-tratamento/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "clinica_id": test_clinica.id,
            "nome": "Tratamento Teste",
            "descricao": "Descricao do Tratamento Teste",
            "tempo_minimo_atendimento": 60
        }
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Tratamento Teste"

def test_read_tipos_tratamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a tipo_tratamento first
    tipo_tratamento_leitura = models.TipoTratamento(
        clinica_id=test_clinica.id,
        nome="Tratamento Leitura",
        descricao="Descricao do Tratamento Leitura",
        tempo_minimo_atendimento=45
    )
    session.add(tipo_tratamento_leitura)
    session.commit()
    session.refresh(tipo_tratamento_leitura)

    response = client.get(
        "/api/tipos-tratamento/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(t["nome"] == "Tratamento Leitura" for t in response.json())

def test_read_tipo_tratamento_by_id(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a tipo_tratamento first
    tipo_tratamento_id = models.TipoTratamento(
        clinica_id=test_clinica.id,
        nome="Tratamento ID",
        descricao="Descricao do Tratamento ID",
        tempo_minimo_atendimento=90
    )
    session.add(tipo_tratamento_id)
    session.commit()
    session.refresh(tipo_tratamento_id)

    response = client.get(
        f"/api/tipos-tratamento/{tipo_tratamento_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Tratamento ID"

def test_update_tipo_tratamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a tipo_tratamento first
    tipo_tratamento_to_update = models.TipoTratamento(
        clinica_id=test_clinica.id,
        nome="Tratamento Antigo",
        descricao="Descricao Antiga",
        tempo_minimo_atendimento=30
    )
    session.add(tipo_tratamento_to_update)
    session.commit()
    session.refresh(tipo_tratamento_to_update)

    response = client.put(
        f"/api/tipos-tratamento/{tipo_tratamento_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "nome": "Tratamento Atualizado",
            "tempo_minimo_atendimento": 75
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Tratamento Atualizado"
    assert response.json()["tempo_minimo_atendimento"] == 75

def test_delete_tipo_tratamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create a tipo_tratamento first
    tipo_tratamento_to_delete = models.TipoTratamento(
        clinica_id=test_clinica.id,
        nome="Tratamento para Deletar",
        descricao="Descricao para Deletar",
        tempo_minimo_atendimento=20
    )
    session.add(tipo_tratamento_to_delete)
    session.commit()
    session.refresh(tipo_tratamento_to_delete)

    response = client.delete(
        f"/api/tipos-tratamento/{tipo_tratamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/tipos-tratamento/{tipo_tratamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /tipos-tratamento endpoints
def test_create_tipo_tratamento_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    response = client.post(
        "/api/tipos-tratamento/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "clinica_id": test_clinica.id,
            "nome": "Tratamento Sem Permissao",
            "descricao": "Descricao Sem Permissao",
            "tempo_minimo_atendimento": 60
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_tipos_tratamento"

def test_read_tipos_tratamento_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/tipos-tratamento/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_tipos_tratamento"

def test_update_tipo_tratamento_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a tipo_tratamento first
    tipo_tratamento_to_update = models.TipoTratamento(
        clinica_id=test_clinica.id,
        nome="Tratamento Permissao Update",
        descricao="Descricao Permissao Update",
        tempo_minimo_atendimento=30
    )
    session.add(tipo_tratamento_to_update)
    session.commit()
    session.refresh(tipo_tratamento_to_update)

    response = client.put(
        f"/api/tipos-tratamento/{tipo_tratamento_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "nome": "Tratamento Atualizado Sem Permissao"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_tipos_tratamento"

def test_delete_tipo_tratamento_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create a tipo_tratamento first
    tipo_tratamento_to_delete = models.TipoTratamento(
        clinica_id=test_clinica.id,
        nome="Tratamento Permissao Delete",
        descricao="Descricao Permissao Delete",
        tempo_minimo_atendimento=20
    )
    session.add(tipo_tratamento_to_delete)
    session.commit()
    session.refresh(tipo_tratamento_to_delete)

    response = client.delete(
        f"/api/tipos-tratamento/{tipo_tratamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_tipos_tratamento"

# Tests for /agendamentos endpoints
def test_create_agendamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento",
        cpf="111.111.111-12",
        data_nascimento=date(1990, 1, 1),
        email="agendamento@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento",
        email="prof_agendamento@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12353"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    response = client.post(
        "/api/agendamentos/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "paciente_id": paciente.id,
            "profissional_id": profissional.id,
            "data": "2024-09-01T10:00:00",
            "status": "AGENDADO"
        }
    )
    assert response.status_code == 201
    assert response.json()["paciente_id"] == paciente.id

def test_read_agendamentos(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento Leitura",
        cpf="222.222.222-23",
        data_nascimento=date(1991, 2, 2),
        email="agendamentoleitura@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_READ")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_read",
        email="prof_agendamento_read@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12354"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento_leitura = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 9, 2, 10, 0, 0),
        status="AGENDADO"
    )
    session.add(agendamento_leitura)
    session.commit()
    session.refresh(agendamento_leitura)

    response = client.get(
        "/api/agendamentos/",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(a["paciente_id"] == paciente.id for a in response.json())

def test_read_agendamento_by_id(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento ID",
        cpf="333.333.333-34",
        data_nascimento=date(1992, 3, 3),
        email="agendamentoid@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_ID")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_id",
        email="prof_agendamento_id@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12355"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento_id = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 9, 3, 10, 0, 0),
        status="AGENDADO"
    )
    session.add(agendamento_id)
    session.commit()
    session.refresh(agendamento_id)

    response = client.get(
        f"/api/agendamentos/{agendamento_id.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["paciente_id"] == paciente.id

def test_update_agendamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento Update",
        cpf="444.444.444-45",
        data_nascimento=date(1993, 4, 4),
        email="agendamentoupdate@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_UPDATE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_update",
        email="prof_agendamento_update@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12356"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento_to_update = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 9, 4, 10, 0, 0),
        status="AGENDADO"
    )
    session.add(agendamento_to_update)
    session.commit()
    session.refresh(agendamento_to_update)

    response = client.put(
        f"/api/agendamentos/{agendamento_to_update.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        },
        json={
            "status": "CONCLUIDO"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "CONCLUIDO"

def test_delete_agendamento(client: TestClient, admin_user_token: str, test_clinica: models.Clinica, session: TestingSessionLocal):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento Delete",
        cpf="555.555.555-56",
        data_nascimento=date(1994, 5, 5),
        email="agendamentodelete@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_DELETE")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_delete",
        email="prof_agendamento_delete@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12357"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento_to_delete = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 9, 5, 10, 0, 0),
        status="AGENDADO"
    )
    session.add(agendamento_to_delete)
    session.commit()
    session.refresh(agendamento_to_delete)

    response = client.delete(
        f"/api/agendamentos/{agendamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(
        f"/api/agendamentos/{agendamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {admin_user_token}"
        }
    )
    assert get_response.status_code == 404

# Test permission denied for /agendamentos endpoints
def test_create_agendamento_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento Sem Perm",
        cpf="666.666.666-67",
        data_nascimento=date(1990, 1, 1),
        email="agendamentosemperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_CREATE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_create_denied",
        email="prof_agendamento_create_denied@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12358"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    response = client.post(
        "/api/agendamentos/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "paciente_id": paciente.id,
            "profissional_id": profissional.id,
            "data": "2024-09-06T10:00:00",
            "status": "AGENDADO"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: criar_agendamentos"

def test_read_agendamentos_permission_denied(client: TestClient, session: TestingSessionLocal, common_user_token: str):
    response = client.get(
        "/api/agendamentos/",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: ler_agendamentos"

def test_update_agendamento_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento Update Sem Perm",
        cpf="777.777.777-78",
        data_nascimento=date(1990, 1, 1),
        email="agendamentoupdatesemperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_UPDATE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_update_denied",
        email="prof_agendamento_update_denied@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12359"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento_to_update = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 9, 7, 10, 0, 0),
        status="AGENDADO"
    )
    session.add(agendamento_to_update)
    session.commit()
    session.refresh(agendamento_to_update)

    response = client.put(
        f"/api/agendamentos/{agendamento_to_update.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "status": "CONCLUIDO"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: atualizar_agendamentos"

def test_delete_agendamento_permission_denied(client: TestClient, admin_user_token: str, session: TestingSessionLocal, common_user_token: str, test_clinica: models.Clinica):
    # Create patient and professional
    paciente = models.Paciente(
        nome="Paciente Agendamento Delete Sem Perm",
        cpf="888.888.888-89",
        data_nascimento=date(1990, 1, 1),
        email="agendamentodeletesemperm@example.com",
        clinica_id=test_clinica.id
    )
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    perfil_prof = models.Perfil(nome="PROFISSIONAL_TESTE_AGENDAMENTO_DELETE_DENIED")
    session.add(perfil_prof)
    session.commit()
    session.refresh(perfil_prof)

    user_prof = models.User(
        username="prof_agendamento_delete_denied",
        email="prof_agendamento_delete_denied@example.com",
        hashed_password=get_password_hash("hashed"),
        perfil_id=perfil_prof.id,
        clinica_id=test_clinica.id
    )
    session.add(user_prof)
    session.commit()
    session.refresh(user_prof)

    profissional = models.Profissional(
        user_id=user_prof.id,
        especialidade="Geral",
        conselho_profissional="CRM",
        numero_conselho="12360"
    )
    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    agendamento_to_delete = models.Agendamento(
        paciente_id=paciente.id,
        profissional_id=profissional.id,
        data=datetime(2024, 9, 8, 10, 0, 0),
        status="AGENDADO"
    )
    session.add(agendamento_to_delete)
    session.commit()
    session.refresh(agendamento_to_delete)

    response = client.delete(
        f"/api/agendamentos/{agendamento_to_delete.id}",
        headers={
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão: excluir_agendamentos"