# Checklist de Progresso do Sistema de Clínicas

Este checklist acompanha o progresso das funcionalidades e melhorias do sistema, baseado no roadmap.

## Estado Atual do Sistema (As-Is) - Concluído

- [x] **Arquitetura e Tecnologia:**
    - [x] Linguagem de Backend: Python 3
    - [x] Framework: Django 4.2
    - [x] Banco de Dados: PostgreSQL
    - [x] Frontend: Abordagem híbrida (templates Django e aplicação React no diretório `frontend/`)
    - [x] Dependências Principais: `django`, `psycopg2`, `Faker`

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

## Roadmap de Melhorias (To-Be) - Próximas Etapas

### Curto Prazo (Próximos 3 meses)

- [x] **Refatoração e Unificação do Frontend:** Finalizar a migração do frontend para React, unificando a experiência do usuário em uma SPA (Single Page Application) moderna.
- [ ] **Testes Automatizados:** Aumentar a cobertura de testes unitários e de integração, especialmente para as funcionalidades críticas de agendamento, faturamento e prontuário eletrônico, garantindo maior estabilidade.

### Médio Prazo (3 a 6 meses)

- [ ] **API para Integrações:** Desenvolver uma API RESTful segura para permitir a integração do sistema com serviços externos, como:
    - [ ] Plataformas de telemedicina.
    - [ ] Gateways de pagamento para cobrança online.
    - [ ] Sistemas de laboratórios para recebimento de resultados de exames.
- [ ] **Notificações em Tempo Real:** Implementar notificações (via WebSockets) para eventos importantes, como:
    - [ ] Lembretes de consulta para pacientes.
    - [ ] Avisos de chegada de paciente para profissionais.
    - [ ] Alertas sobre atualizações em prontuários.

### Longo Prazo (6 a 12 meses)

- [ ] **Módulo de Business Intelligence (BI):** Criar um painel de BI com relatórios e gráficos interativos para que os gestores possam analisar métricas importantes, como faturamento, taxa de ocupação, eficácia de campanhas de marketing, etc.
- [ ] **Aplicativo Móvel (PWA ou Nativo):** Desenvolver um aplicativo móvel para pacientes, permitindo que eles agendem consultas, acessem seus prontuários, recebam notificações e realizem pagamentos de forma conveniente.