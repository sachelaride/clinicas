# Sistema de Gestão de Clínicas

Um sistema web completo para a gestão de clínicas médicas, odontológicas e de outras especialidades, desenvolvido com FastAPI (Python) para o backend e React (JavaScript) para o frontend. O projeto visa centralizar e otimizar todas as operações da clínica, desde o agendamento de pacientes até a gestão financeira e de marketing.

## ✨ Funcionalidades Principais

O sistema é dividido em módulos que cobrem as principais áreas de uma clínica moderna:

### 🏥 Gestão da Clínica e Cadastros
- **Gestão de Múltiplas Clínicas:** Permite administrar diversas unidades ou filiais a partir de um único sistema.
- **Gestão de Usuários com Perfis:** Controle de acesso robusto com perfis pré-definidos:
    - **Administrador:** Acesso total ao sistema.
    - **Coordenador:** Gerencia equipes e operações.
    - **Atendente:** Focado em agendamentos, recepção e atendimento ao paciente.
    - **Profissional da Saúde:** Acesso à sua agenda e aos prontuários dos pacientes.
    - **Paciente:** Acesso ao seu portal exclusivo.
- **Cadastro de Pacientes:** Registro completo de informações pessoais, de contato e do responsável legal.
- **Cadastro de Profissionais:** Gerenciamento de dados dos profissionais, incluindo especialidade, conselho profissional e carga horária.
- **Gestão de Convênios e Planos:** Cadastro de convênios médicos e seus respectivos planos.
- **Tipos de Tratamento:** Definição dos tratamentos e procedimentos oferecidos pela clínica.

### 🗓️ Operações e Atendimento
- **Agendamento de Consultas:** Um calendário interativo para marcar, visualizar, concluir e cancelar agendamentos.
- **Prontuário Eletrônico do Paciente (PEP):** Um prontuário completo e seguro, com seções para:
    - Queixa principal e histórico da doença.
    - Antecedentes pessoais e familiares.
    - Hábitos de vida, medicamentos em uso e alergias.
    - Sinais vitais e exames físicos.
    - Hipóteses diagnósticas (com suporte a CID-10).
    - Solicitação de exames complementares.
    - Prescrições, encaminhamentos e orientações.
    - Evolução clínica.
    - Anexo de documentos (termos de consentimento, exames, etc.).
- **Registro de Atendimentos:** Controle do fluxo de atendimento, desde a chegada do paciente até a finalização da consulta.
- **Gestão de Documentos:** Sistema para upload e organização de documentos de pacientes em pastas personalizadas, com controle de integridade via hash.

### 💰 Gestão Financeira
- **Tabela de Preços:** Definição de preços para cada tratamento, com distinção entre particular e diferentes planos de convênio.
- **Controle de Lançamentos:** Módulo de contas a pagar e a receber para um controle financeiro detalhado.
- **Faturamento de Convênios:** Geração de faturas para convênios, agrupando os atendimentos realizados em um período.
- **Cálculo de Comissões:** Cálculo automático e gestão de comissões para os profissionais com base nos atendimentos realizados.

### 📈 CRM e Marketing
- **Gestão de Leads:** Funil de vendas para capturar e gerenciar potenciais pacientes, desde o primeiro contato até a conversão.
- **Campanhas de Marketing:** Planejamento e registro de campanhas de marketing via SMS, WhatsApp, E-mail, etc.
- **Cupons de Desconto:** Criação e gerenciamento de cupons de desconto, que podem ser associados a campanhas.
- **Pesquisas de Satisfação (NPS):** Envio de pesquisas e coleta de feedback dos pacientes para medir a qualidade do serviço.

### 💻 Portais de Acesso
- **Portal do Paciente:** Uma área exclusiva para o paciente consultar seus agendamentos, prontuários, documentos e histórico financeiro.
- **Portal do Profissional:** Uma área dedicada ao profissional da saúde para visualizar sua agenda, acessar os prontuários dos seus pacientes e registrar atendimentos.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python 3, FastAPI
- **Banco de Dados:** PostgreSQL
- **Frontend:** React, JavaScript, HTML, CSS

## 📂 Estrutura do Projeto

O projeto está organizado nos seguintes diretórios principais:

-   `app/`: Contém o código-fonte do backend FastAPI, incluindo modelos, esquemas, endpoints da API e lógica de negócio.
-   `frontend/`: Contém o código-fonte do aplicativo React, incluindo componentes, estilos e lógica do frontend.
-   `auxiliary/`: Contém scripts auxiliares para criação e população do banco de dados, bem como outras ferramentas de suporte.
-   `tests/`: Contém os testes automatizados para o backend e o frontend.
-   `alembic.ini`: Arquivo de configuração principal do Alembic para migrações de banco de dados.
-   `requirements.txt`: Lista as dependências Python do projeto.
-   `install.md`: Guia detalhado de instalação e configuração do ambiente.
-   `roadmap.md`: O roadmap do projeto, detalhando o estado atual e as futuras melhorias.

## 🚀 Instalação
Para instruções detalhadas de como instalar e configurar o ambiente de desenvolvimento, consulte o arquivo [install.md](install.md).

## 🔄 Migrações de Banco de Dados (Alembic)

Este projeto utiliza [Alembic](https://alembic.sqlalchemy.org/en/latest/) para gerenciar as migrações do banco de dados.

### Como Gerar uma Nova Migração

Após fazer alterações nos modelos SQLAlchemy (`app/models.py`), você pode gerar uma nova migração automaticamente:

```bash
alembic revision --autogenerate -m "Sua mensagem descritiva aqui"
```

Substitua `"Sua mensagem descritiva aqui"` por uma descrição clara das mudanças no esquema.

### Como Aplicar Migrações

Para aplicar todas as migrações pendentes ao seu banco de dados (levando-o ao estado mais recente), execute:

```bash
alembic upgrade head
```

### Como Reverter Migrações

Para reverter a última migração aplicada:

```bash
alembic downgrade -1
```

Para reverter para uma revisão específica (substitua `[REVISAO]` pelo ID da revisão):

```bash
alembic downgrade [REVISAO]
```



## 🗺️ Roadmap
Temos muitas ideias para o futuro! Confira nosso [roadmap.md](roadmap.md) para ver as próximas funcionalidades e melhorias planejadas para o sistema.