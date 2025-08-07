# Roadmap do Sistema de Clínicas

Este documento descreve o estado atual do sistema e um possível caminho de evolução, com sugestões de melhorias e novas funcionalidades a curto, médio e longo prazo.

##  Estado Atual do Sistema (As-Is)

Esta seção detalha a arquitetura, as tecnologias e as funcionalidades que já foram implementadas e estão operacionais no sistema.

### Arquitetura e Tecnologia

- **Linguagem de Backend:** Python 3
- **Framework:** Django 4.2
- **Banco de Dados:** PostgreSQL
- **Frontend:** O sistema utiliza uma abordagem híbrida:
    - A maior parte da interface é renderizada diretamente pelo sistema de **templates do Django**, seguindo uma arquitetura mais tradicional (Monolith).
    - Existe um diretório `frontend/` com uma aplicação **React (JavaScript)**, sugerindo que partes do sistema podem ser ou foram planejadas para serem mais interativas e desacopladas, no estilo de uma Single Page Application (SPA).
- **Dependências Principais:**
    - `django`: O núcleo do sistema.
    - `psycopg2`: Driver para a comunicação com o banco de dados PostgreSQL.
    - `Faker`: Utilizado para popular o banco de dados com dados de teste.

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

---

## Roadmap de Melhorias (To-Be)

A seguir, são apresentadas sugestões de evolução para o sistema.

### Curto Prazo (Próximos 3 meses)

- **Refatoração e Unificação do Frontend:** Finalizar a migração do frontend para **React**, unificando a experiência do usuário em uma SPA (Single Page Application) moderna. Isso melhorará a performance, a interatividade e a manutenibilidade da interface.
- **Testes Automatizados:** Aumentar a cobertura de testes unitários e de integração, especialmente para as funcionalidades críticas de agendamento, faturamento e prontuário eletrônico, garantindo maior estabilidade.

### Médio Prazo (3 a 6 meses)

- **API para Integrações:** Desenvolver uma API RESTful segura para permitir a integração do sistema com serviços externos, como:
    - Plataformas de telemedicina.
    - Gateways de pagamento para cobrança online.
    - Sistemas de laboratórios para recebimento de resultados de exames.
- **Notificações em Tempo Real:** Implementar notificações (via WebSockets) para eventos importantes, como:
    - Lembretes de consulta para pacientes.
    - Avisos de chegada de paciente para profissionais.
    - Alertas sobre atualizações em prontuários.

### Longo Prazo (6 a 12 meses)

- **Módulo de Business Intelligence (BI):** Criar um painel de BI com relatórios e gráficos interativos para que os gestores possam analisar métricas importantes, como faturamento, taxa de ocupação, eficácia de campanhas de marketing, etc.
- **Aplicativo Móvel (PWA ou Nativo):** Desenvolver um aplicativo móvel para pacientes, permitindo que eles agendem consultas, acessem seus prontuários, recebam notificações e realizem pagamentos de forma conveniente.