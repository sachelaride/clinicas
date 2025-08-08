# Roadmap do Sistema de Clínicas

Este documento descreve o estado atual do sistema e um possível caminho de evolução, com sugestões de melhorias e novas funcionalidades a curto, médio e longo prazo.

## Estado Atual do Sistema (As-Is) - Concluído

- [x] **Arquitetura e Tecnologia:**
    - [x] Linguagem de Backend: Python 3
    - [x] Framework Backend: FastAPI
    - [x] Banco de Dados: PostgreSQL
    - [x] Frontend: React (SPA - Single Page Application)
    - [x] Dependências Principais Backend: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `pydantic`, `passlib`, `python-jose`
    - [x] Dependências Principais Frontend: `react`, `react-dom`, `react-router-dom`, `axios`, `bootstrap`, `react-bootstrap`, `react-big-calendar`, `moment`

- [x] **Funcionalidades Implementadas:**
    - [x] **Gestão Central e Cadastros:**
        - [x] Administração de múltiplas clínicas.
        - [x] Controle de acesso baseado em perfis (Administrador, Coordenador, Atendente, Profissional, Paciente).
        - [x] Cadastros completos de Pacientes, Profissionais, Convênios e Planos de Saúde.
        - [x] Definição de Tipos de Tratamento e seus respectivos preços (tabela de preços).
    - [x] **Operações Clínicas:**
        - [x] Agenda de consultas interativa.
        - [x] Prontuário Eletrônico do Paciente (PEP) detalhado e com histórico.
        - [x] Registro do fluxo de atendimento, da chegada à finalização.
        - [x] Sistema de gestão de documentos com upload de arquivos.
    - [x] **Módulo Financeiro:**
        - [x] Lançamentos de contas a pagar e a receber.
        - [x] Geração de faturas para convênios.
        - [x] Cálculo e controle de comissões para profissionais.
    - [x] **CRM e Marketing:**
        - [x] Gestão de Leads com funil de conversão.
        - [x] Criação e acompanhamento de campanhas de marketing.
        - [x] Geração de cupons de desconto.
        - [x] Realização de pesquisas de satisfação (NPS).
    - [x] **Portais de Acesso:**
        - [x] Portal do Paciente para visualização de dados.
        - [x] Portal do Profissional para gestão de sua agenda e prontuários.

---

## Roadmap de Melhorias (To-Be)

A seguir, são apresentadas sugestões de evolução para o sistema.

### Curto Prazo (Próximos 3 meses)

- [x] **Refatoração e Unificação do Frontend:** Finalizar a migração do frontend para **React**, unificando a experiência do usuário em uma SPA (Single Page Application) moderna. Isso melhorará a performance, a interatividade e a manutenibilidade da interface.
- [x] **Testes Automatizados:** Aumentar a cobertura de testes unitários e de integração, especialmente para as funcionalidades críticas de agendamento, faturamento e prontuário eletrônico, garantindo maior estabilidade.
    - [x] Backend: unit/integration (pytest + httpx), contrato de API (pydantic schemas).
    - [x] Frontend: e2e (Playwright).
    - [x] Frontend: Testes de componentes críticos (React Testing Library).
    - [ ] Cobertura mínima: 70% para módulos críticos (agendamento, PEP, financeiro).
    - [ ] Executar testes em CI para cada PR.
- [x] **Migrações Alembic:**
    - [x] **Configurar Alembic:** Instalado e configurado o Alembic no projeto backend.
    - [x] **Gerar Primeira Migração:** Gerada a migração inicial do banco de dados a partir do modelo atual.
    - [x] **Testar Migração Localmente:** Testada a aplicação com as migrações do Alembic em um ambiente de desenvolvimento local.
    - [x] **Documentar Processo de Migração:** Adicionadas instruções sobre como executar as migrações no README.md.
    - [x] **Integrar Migração no Deploy:** Criado `docs/DEPLOYMENT.md` e referenciado no README.md.

### Médio Prazo (3 a 6 meses)

- **API para Integrações:**
    - **Plataformas de Telemedicina:**
        - [ ] **Definir Requisitos:** Identificar plataformas e dados necessários.
        - [ ] **Projetar Endpoints:** Criar o design dos endpoints da API.
        - [ ] **Implementar Autenticação/Autorização:** Garantir a segurança dos endpoints.
        - [ ] **Desenvolver Lógica de Negócio:** Implementar a interação com plataformas externas.
        - [ ] **Criar Testes Automatizados:** Escrever testes para os novos endpoints.
        - [ ] **Documentar API:** Adicionar documentação detalhada.
    - **Gateways de Pagamento:** Integrar com APIs de pagamento (ex: Stripe, PagSeguro) para cobrança online de faturas e serviços.
    - **Sistemas de Laboratórios:** Criar endpoints para recebimento automático de resultados de exames.
- [ ] **Notificações em Tempo Real:**
    - [ ] **Análise e Design:**
        - [ ] Definir provedores de serviço de SMS/WhatsApp/E-mail.
        - [ ] Projetar a arquitetura de WebSockets para notificações em tempo real.
        - [ ] Modelar as tabelas de banco de dados para notificações e status de envio.
    - [ ] **Desenvolvimento Backend:**
        - [ ] Implementar serviço de agendamento de tarefas (APScheduler/Celery Beat) para lembretes.
        - [ ] Desenvolver lógica de envio de mensagens para diferentes canais (SMS, WhatsApp, E-mail).
        - [ ] Criar endpoints para confirmação/cancelamento de agendamentos via link.
        - [ ] Implementar rastreamento de métricas de envio e interação com notificações.
        - [ ] Configurar WebSockets no backend para envio de notificações em tempo real.
    - [ ] **Desenvolvimento Frontend:**
        - [ ] Desenvolver UI para exibir status de lembretes e notificações.
        - [ ] Implementar funcionalidade de envio manual de lembretes.
        - [ ] Adicionar filtros por status de notificação nas listas de agendamento.
        - [ ] Integrar WebSockets para atualizações em tempo real na UI.
    - [ ] **Testes:**
        - [ ] Escrever testes unitários para a lógica de envio e agendamento.
        - [ ] Escrever testes de integração para os endpoints de notificação.
        - [ ] Testar a funcionalidade de WebSockets.
    - [ ] **Documentação:**
        - [ ] Documentar a API de notificações.
        - [ ] Documentar o processo de configuração dos provedores de serviço.
- [ ] **Observabilidade e Alertas:**
    - [ ] Logs estruturados (JSON) com correlação de requisições.
    - [ ] Métricas chave: tempo de resposta, taxa de erro, jobs de lembrete.
    - [ ] Alertas para falha de disparo de lembretes.
- [ ] **Hardening de Segurança:**
    - [ ] Senhas com hash (passlib), política de rotação de tokens JWT.
    - [ ] CORS restrito por ambiente, rate limit.
    - [ ] Scan de dependências na pipeline.
    - [ ] Conformidade com LGPD: mínimo necessário de dados, logs sem dados sensíveis.

### Longo Prazo (6 a 12 meses)

- [ ] **Containerização (Docker):** Implementar Docker Compose para facilitar o ambiente de desenvolvimento e implantação.
    - **Sugestão de Implementação:**
        - Criar arquivos `Dockerfile` para o backend (FastAPI) e frontend (React).
        - Configurar `docker-compose.yml` para orquestrar os serviços (PostgreSQL, Backend, Frontend, pgAdmin).
        - Adicionar scripts para `docker-compose up` e `docker-compose down`.
- [ ] **Módulo de Business Intelligence (BI):** Criar um painel de BI com relatórios e gráficos interativos para que os gestores possam analisar métricas importantes, como faturamento, taxa de ocupação, eficácia de campanhas de marketing, etc.
    - [ ] Métricas: Taxa de envio/entrega/confirmação de lembretes, eficácia por canal e antecedência, no-show antes/depois.
- [ ] **Aplicativo Móvel (PWA ou Nativo):** Desenvolver um aplicativo móvel para pacientes, permitindo que eles agendem consultas, acessem seus prontuários, recebam notificações e realizem pagamentos de forma conveniente.
- [ ] **Melhoria do Fluxo de Caixa:** Implementar link de pagamento e conciliação simples.
- [ ] **Onboarding Guiado para Atendentes:** Diminuir tempo de treinamento do atendente em 30%.
    - [ ] Sugestão de Implementação:
        - Tutoriais Interativos: Guias passo a passo dentro do próprio sistema.
        - Checklists de Tarefas: Para garantir que todas as etapas do processo sejam seguidas.
        - Base de Conhecimento: Seção de FAQ e artigos de ajuda.
- [ ] **Remarcação Proativa de Cancelados:** Aumentar taxa de ocupação em 10%.

## Padrões de Qualidade e Desenvolvimento (Cross-cutting)

### Integração de Migrações Alembic no Deploy

É crucial integrar o processo de migração do Alembic no fluxo de deploy da aplicação para garantir que o esquema do banco de dados esteja sempre atualizado e em sincronia com a versão do código.

#### Estratégias de Integração

Existem várias abordagens para integrar as migrações no deploy, dependendo da sua infraestrutura e pipeline de CI/CD:

1.  **Execução Automática no Início da Aplicação (para ambientes menores/desenvolvimento):**
    *   Pode ser feito adicionando um comando `alembic upgrade head` ao script de inicialização da aplicação. **CUIDADO:** Esta abordagem não é recomendada para ambientes de produção de alta disponibilidade, pois pode causar tempo de inatividade ou problemas de concorrência.

2.  **Passo Dedicado na Pipeline de CI/CD:**
    *   A abordagem mais robusta e recomendada para produção.
    *   Adicione um passo na sua pipeline de CI/CD (e.g., Jenkins, GitLab CI, GitHub Actions) que execute `alembic upgrade head` *antes* de implantar a nova versão da aplicação.
    *   Isso garante que o banco de dados esteja pronto para a nova versão do código.

3.  **Execução Manual (para controle total):**
    *   Em alguns casos, especialmente em ambientes muito críticos, pode-se optar por executar as migrações manualmente após o deploy do código, mas antes de liberar o tráfego para a nova versão.

#### Considerações Importantes

*   **Backup:** Sempre faça backup do seu banco de dados antes de aplicar migrações em produção.
*   **Transações:** O Alembic executa migrações dentro de transações, o que ajuda a garantir a atomicidade das operações.
*   **Rollback:** Tenha um plano de rollback caso uma migração falhe ou cause problemas inesperados.
*   **Zero Downtime:** Para aplicações de alta disponibilidade, considere estratégias de deploy que minimizem o tempo de inatividade durante as migrações (e.g., blue/green deployment, canary releases).

#### Exemplo (Pseudocódigo para Pipeline de CI/CD)

```yaml
stages:
  - build
  - test
  - migrate
  - deploy

migrate_db:
  stage: migrate
  script:
    - pip install -r requirements.txt
    - alembic upgrade head
  only:
    - main # Executar apenas no branch principal
```

**Nota:** Este é um exemplo genérico. Adapte-o à sua ferramenta de CI/CD e ambiente de deploy específicos.

- [ ] **Estilo e Lint:**
    - [ ] Backend: flake8/black/isort.
    - [ ] Frontend: eslint + prettier.
    - [ ] Pre-commit hooks para padronização.
- [ ] **Revisão de Código:**
    - [ ] PR pequeno, objetivo e testável.
    - [ ] Checklist: testes passam? documentação atualizada? rollback claro? impacto em dados?
- [ ] **Documentação:**
    - [ ] Atualizar documentação (README, install, docs/feature.md) para novas funcionalidades.
- [ ] **Logs e Mensagens de Erro:**
    - [ ] Logs e mensagens de erro amigáveis.
