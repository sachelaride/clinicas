# Guia de Instalação do Sistema de Clínicas

Este guia descreve os passos para uma instalação limpa do Sistema de Clínicas, que consiste em um backend FastAPI (Python) e um frontend React (JavaScript).

## Pré-requisitos

- Python 3.10 ou superior
- Node.js e npm (ou yarn)
- PostgreSQL
- Git

## Passos da Instalação

### 1. Configuração do Backend (FastAPI)

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd sistema
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências do backend:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o banco de dados PostgreSQL:**
    - Crie um banco de dados PostgreSQL (ex: `clinicas_db`).
    - Atualize a string de conexão do banco de dados no arquivo `app/core/database.py`:
      ```python
      SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/clinicas_db"
      ```
      Substitua `user`, `password` e `host` pelas suas credenciais.

5.  **Configure e execute as migrações do banco de dados com Alembic:**
    Este projeto utiliza [Alembic](https://alembic.sqlalchemy.org/en/latest/) para gerenciar as migrações do banco de dados.

    a.  **Inicialize o Alembic (apenas na primeira vez):**
        ```bash
        alembic init app/alembic
        ```
        Isso criará o diretório `app/alembic` e o arquivo `alembic.ini` na raiz do projeto.

    b.  **Configure o `alembic.ini`:**
        Abra o arquivo `alembic.ini` (na raiz do projeto) e atualize a linha `sqlalchemy.url` com a URL do seu banco de dados PostgreSQL. Exemplo:
        ```ini
        sqlalchemy.url = postgresql://user:password@host/clinicas_db
        ```
        **Importante:** Se sua URL contiver caracteres especiais como `%`, eles devem ser escapados (ex: `%3D` deve ser `%%3D`).

    c.  **Configure o `app/alembic/env.py`:**
        Abra o arquivo `app/alembic/env.py` e importe a `Base` dos seus modelos, e atribua-a a `target_metadata`. Localize as linhas:
        ```python
        # from myapp import mymodel
        # target_metadata = mymodel.Base.metadata
        target_metadata = None
        ```
        E altere para:
        ```python
        from app.models import Base
        target_metadata = Base.metadata
        ```

    d.  **Gere a primeira migração (após configurar `env.py` e `alembic.ini`):**
        ```bash
        alembic revision --autogenerate -m "Initial migration"
        ```
        Isso criará um novo arquivo de migração em `app/alembic/versions/`.

    e.  **Aplique as migrações ao banco de dados:**
        ```bash
        alembic upgrade head
        ```
        Isso criará as tabelas no seu banco de dados.

6.  **Popule o banco de dados (opcional, para desenvolvimento/testes):**
    Você pode usar os scripts de população localizados no diretório `auxiliary`:
    ```bash
    python auxiliary/create_db_tables.py
    python auxiliary/populate_permissions.py
    python auxiliary/populate_clinica.py
    python auxiliary/populate_clinics_and_services.py
    python auxiliary/populate_users_and_patients.py
    python auxiliary/populate_db.py
    python auxiliary/create_default_user.py
    ```

7.  **Inicie o servidor backend:**
    ```bash
    uvicorn app.main:app --reload
    ```
    O servidor backend estará acessível em `http://127.0.0.1:8000`.

### 2. Configuração do Frontend (React)

1.  **Navegue até o diretório do frontend:**
    ```bash
    cd frontend
    ```

2.  **Instale as dependências do frontend:**
    ```bash
    npm install
    # ou
    yarn install
    ```

3.  **Inicie o aplicativo React:**
    ```bash
    npm start
    # ou
    yarn start
    ```
    O aplicativo frontend será aberto no seu navegador, geralmente em `http://localhost:3000`.

### 3. Acesso ao Sistema

- Certifique-se de que tanto o servidor backend (FastAPI) quanto o aplicativo frontend (React) estejam em execução.
- Acesse o frontend no seu navegador (geralmente `http://localhost:3000`).
- Use as credenciais de usuário criadas (ou o usuário padrão, se populado) para fazer login.