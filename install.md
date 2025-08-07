# Guia de Instalação do Sistema de Clínicas

Este guia descreve os passos para uma instalação limpa do Sistema de Clínicas.

## Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL
- Git

## Passos da Instalação

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd sistema_clinicas
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   - Crie um banco de dados no PostgreSQL.
   - Atualize as credenciais no arquivo `sistema_clinicas/settings.py` com os detalhes do seu banco de dados.

5. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Limpe e configure o banco de dados para um novo ambiente:**
   ```bash
   python manage.py clean_and_setup
   ```

8. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

Acesse a aplicação em `http://127.0.0.1:8000`.
