# Roadmap do Sistema de Clínicas

Este documento descreve o estado atual do sistema e um possível caminho de evolução, com sugestões de melhorias e novas funcionalidades a curto, médio e longo prazo.

##  Estado Atual do Sistema (As-Is)

Esta seção detalha a arquitetura, as tecnologias e as funcionalidades que já foram implementadas e estão operacionais no sistema.

### Arquitetura e Tecnologia

- **Linguagem de Backend:** Python 3
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **Frontend:** O sistema utiliza uma arquitetura de **Single Page Application (SPA)** com **React (JavaScript)**, onde toda a interface é renderizada no lado do cliente e se comunica com o backend via API RESTful.
- **Dependências Principais Backend:**
    - `fastapi`: O framework web para o backend.
    - `uvicorn`: Servidor ASGI para o FastAPI.
    - `sqlalchemy`: ORM para interação com o banco de dados.
    - `psycopg2-binary`: Driver PostgreSQL.
    - `pydantic`: Validação de dados e serialização.
    - `passlib[bcrypt]`: Hashing de senhas.
    - `python-jose[cryptography]`: Geração e verificação de tokens JWT.
- **Dependências Principais Frontend:**
    - `react`, `react-dom`: Bibliotecas principais do React.
    - `react-router-dom`: Roteamento no frontend.
    - `axios`: Cliente HTTP para requisições API.
    - `bootstrap`, `react-bootstrap`: Componentes UI.
    - `react-big-calendar`, `moment`: Componentes de calendário.

### Funcionalidades Implementadas

O sistema já conta com um conjunto robusto de funcionalidades que cobrem as principais necessidades de uma clínica:

- **Gestão Central e Cadastros:**
    - Administração de múltiplas clínicas.
    - Controle de acesso baseado em perfis (Administrador, Coordenador, Atendente, Profissional, Paciente).
    - Cadastros completos de Pacientes, Profissionais, Convênios e Planos de Saúde.
    - Definição de Tipos de Tratamento e seus respectivos preços (tabela de preços).

- **Operações Clínicas:**
    - Agenda de consultas interativa.
    - Prontuário Eletrônico do Paciente (PEP) detalhado e com histórico.
    - Registro do fluxo de atendimento, da chegada à finalização.
    - Sistema de gestão de documentos com upload de arquivos.

- **Módulo Financeiro:**
    - Lançamentos de contas a pagar e a receber.
    - Geração de faturas para convênios.
    - Cálculo e controle de comissões para profissionais.

- **CRM e Marketing:**
    - Gestão de Leads com funil de conversão.
    - Criação e acompanhamento de campanhas de marketing.
    - Geração de cupons de desconto.
    - Realização de pesquisas de satisfação (NPS).

- **Portais de Acesso:**
    - Portal do Paciente para visualização de dados.
    - Portal do Profissional para gestão de sua agenda e prontuários.

**Nota:** A última mensagem de commit (`a625152 Mensagem do commit aqui`) é genérica. Para um melhor acompanhamento do progresso, é crucial utilizar mensagens de commit mais descritivas e atômicas, que reflitam as mudanças realizadas.

---

## Roadmap de Melhorias (To-Be)

A seguir, são apresentadas sugestões de evolução para o sistema.

### Curto Prazo (Próximos 3 meses)

- [x] **Refatoração e Unificação do Frontend:** Finalizar a migração do frontend para **React**, unificando a experiência do usuário em uma SPA (Single Page Application) moderna. Isso melhorará a performance, a interatividade e a manutenibilidade da interface.
- [x] **Testes Automatizados:** Aumentar a cobertura de testes unitários e de integração, especialmente para as funcionalidades críticas de agendamento, faturamento e prontuário eletrônico, garantindo maior estabilidade.
    - **Sugestão de Implementação:**
        - **Backend:** Utilizar `pytest` com `httpx` para testes de unidade e integração. Implementar testes de contrato de API com base nos schemas Pydantic.
        - **Frontend E2E:** Adotar `Playwright` para testes end-to-end (e2e) de fluxos críticos (ex: login).
        - **Frontend Componentes:** Implementar testes de componentes críticos com `React Testing Library`.
        - **CI/CD:** Configurar pipelines para executar testes automaticamente em cada Pull Request.
- [ ] **Migrações Alembic:**
    - [ ] **Configurar Alembic:** Instalar e configurar o Alembic no projeto backend.
    - [ ] **Gerar Primeira Migração:** Gerar a migração inicial do banco de dados a partir do modelo atual.
    - [ ] **Testar Migração Localmente:** Testar a aplicação com as migrações do Alembic em um ambiente de desenvolvimento local.
    - [ ] **Documentar Processo de Migração:** Adicionar instruções sobre como executar as migrações no README ou em um arquivo de documentação.
    - [ ] **Integrar Migração no Deploy:** Incluir o processo de migração do Alembic no fluxo de deploy.

### Médio Prazo (3 a 6 meses)

- **API para Integrações:** Desenvolver uma API RESTful segura para permitir a integração do sistema com serviços externos.
    - **Sugestão de Implementação:**
        - **Plataformas de Telemedicina:** Definir endpoints para agendamento e sincronização de status de consultas online.
        - **Gateways de Pagamento:** Integrar com APIs de pagamento (ex: Stripe, PagSeguro) para cobrança online de faturas e serviços.
        - **Sistemas de Laboratórios:** Criar endpoints para recebimento automático de resultados de exames.
- **Notificações em Tempo Real e Confirmação Automática de Agendamentos (D-2):** Implementar um sistema robusto de notificações para eventos importantes e lembretes de agendamento com confirmação/cancelamento.
    - **Sugestão de Implementação:**
        - **Backend:**
            - **Job Agendado:** Utilizar `APScheduler` (para menor complexidade inicial) ou `Celery` + `Celery Beat` (para escalabilidade em produção) para agendar o envio de lembretes (D-2, D-1, no dia).
            - **Lógica de Envio:** Desenvolver serviço para enviar mensagens via WhatsApp, SMS e E-mail, utilizando as variáveis de ambiente configuradas em `.env`.
            - **Endpoints de Confirmação/Cancelamento:** Criar endpoints públicos (`GET /appointments/confirm?token=...`, `GET /appointments/cancel?token=...`) para que os pacientes possam interagir com os lembretes.
            - **Rastreamento de Métricas:** Implementar o registro de status de envio, entrega e confirmação/cancelamento das notificações.
        - **Frontend:**
            - **UI para Lembretes:** Adicionar um banner na tela de agendamento indicando o status do lembrete.
            - **Ações Manuais:** Botão "Enviar lembrete agora" para envio manual.
            - **Filtros:** Adicionar filtros por status (Confirmado/Pendente/Cancelar/Remarcar) nas listas de agendamento.
            - **Indicador em Tempo Real:** (Opcional, futuro) Utilizar WebSockets para atualizar o status do agendamento em tempo real na interface.
        - **Banco de Dados:**
            - **Tabela `appointments`:** Adicionar campos `preferred_channel` (enum: whatsapp, sms, email), `confirmation_token` (string), `status` (PENDENTE, CONFIRMADO, CANCELADO, REMARCAR).
            - **Nova Tabela `notifications`:** Para registrar o histórico de notificações (id, appointment_id, channel, status, attempts, sent_at, response_at, provider_message_id).
        - **Segurança e Privacidade:** Implementar tokens curtos e de uso único, evitar exposição de dados sensíveis em links, garantir logs sem PII e conformidade com a LGPD.
- **Observabilidade e Alertas:** Implementar um sistema de monitoramento para garantir a saúde e o desempenho do sistema.
    - **Sugestão de Implementação:**
        - **Logs:** Configurar logs estruturados (JSON) com IDs de correlação para rastrear requisições.
        - **Métricas:** Coletar métricas chave como tempo de resposta da API, taxa de erro, e status de execução de jobs (ex: jobs de lembrete).
        - **Alertas:** Configurar alertas para falhas críticas, como falha no disparo de lembretes D-2/D-1 ou erros na API.
- **Hardening de Segurança:** Fortalecer a segurança do sistema em diversas camadas.
    - **Sugestão de Implementação:**
        - **Autenticação/Autorização:** Revisar e aprimorar a política de senhas (força, expiração), rotação de tokens JWT.
        - **CORS:** Manter o CORS restrito por ambiente (desenvolvimento vs. produção).
        - **Rate Limiting:** Implementar rate limiting básico para proteger contra ataques de força bruta.
        - **Scan de Dependências:** Integrar ferramentas de scan de vulnerabilidades de dependências na pipeline de CI/CD.
        - **LGPD:** Garantir que o sistema colete apenas o mínimo de dados necessário, que logs não contenham PII e que haja processos para atender a solicitações de dados e exclusão.

### Longo Prazo (6 a 12 meses)

- **Containerização (Docker):** Implementar Docker Compose para facilitar o ambiente de desenvolvimento e implantação.
    - **Sugestão de Implementação:**
        - Criar arquivos `Dockerfile` para o backend (FastAPI) e frontend (React).
        - Configurar `docker-compose.yml` para orquestrar os serviços (PostgreSQL, Backend, Frontend, pgAdmin).
        - Adicionar scripts para `docker-compose up` e `docker-compose down`.
- **Módulo de Business Intelligence (BI):** Criar um painel de BI com relatórios e gráficos interativos para que os gestores possam analisar métricas importantes.
    - **Sugestão de Implementação:**
        - **Métricas Chave:** Desenvolver dashboards para visualizar faturamento, taxa de ocupação, eficácia de campanhas de marketing, taxa de envio/entrega/confirmação de lembretes, eficácia por canal e antecedência, e comparação de no-show antes/depois da implementação dos lembretes.
        - **Ferramentas:** Avaliar ferramentas de BI open-source (ex: Metabase, Superset) ou construir dashboards customizados no frontend.
- **Aplicativo Móvel (PWA ou Nativo):** Desenvolver um aplicativo móvel para pacientes.
    - **Sugestão de Implementação:**
        - **PWA (Progressive Web App):** Abordagem inicial mais rápida, utilizando tecnologias web para uma experiência de aplicativo.
        - **Nativo (React Native/Flutter):** Para uma experiência mais rica e acesso a recursos nativos do dispositivo, se necessário.
        - **Funcionalidades:** Agendamento de consultas, acesso a prontuários, recebimento de notificações push, pagamentos.
- **Melhoria do Fluxo de Caixa:** Implementar funcionalidades avançadas para otimizar o fluxo financeiro.
    - **Sugestão de Implementação:**
        - **Link de Pagamento:** Geração de links de pagamento para faturas.
        - **Conciliação:** Ferramentas para conciliação bancária e de pagamentos.
- **Onboarding Guiado para Atendentes:** Diminuir tempo de treinamento do atendente em 30%.
    - **Sugestão de Implementação:**
        - **Tutoriais Interativos:** Guias passo a passo dentro do próprio sistema.
        - **Checklists de Tarefas:** Para garantir que todas as etapas do processo sejam seguidas.
        - **Base de Conhecimento:** Seção de FAQ e artigos de ajuda.
- **Remarcação Proativa de Cancelados:** Aumentar taxa de ocupação em 10%.

## Padrões de Qualidade e Desenvolvimento (Cross-cutting)

- **Estilo e Lint:** Garantir a padronização do código.
    - **Sugestão de Implementação:**
        - **Backend:** Configurar `flake8`, `black` e `isort` para formatação e linting automáticos.
        - **Frontend:** Configurar `eslint` e `prettier` para formatação e linting automáticos.
        - **Hooks de Pre-commit:** Utilizar `pre-commit` para automatizar a execução de lints e formatadores antes de cada commit.
- **Revisão de Código:** Estabelecer um processo de revisão de código eficaz.
    - **Sugestão de Implementação:**
        - **PRs Pequenos:** Incentivar Pull Requests pequenos, focados em um único objetivo.
        - **Checklist de Revisão:** Criar um checklist para revisores, incluindo verificação de testes, documentação, rollback e impacto em dados.
- **Documentação:** Manter a documentação sempre atualizada.
    - **Sugestão de Implementação:**
        - **Documentação de Novas Funcionalidades:** Exigir que novas funcionalidades sejam documentadas (ex: em `docs/feature.md`).
        - **Atualização Contínua:** Revisar e atualizar `README.md`, `install.md` e outros documentos conforme o sistema evolui.
- [ ] **Logs e Mensagens de Erro:** Melhorar a clareza e utilidade dos logs e mensagens de erro.
    - [ ] Logs e mensagens de erro amigáveis.
