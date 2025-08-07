import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import PacienteList from './components/PacienteList';
import Dashboard from './components/Dashboard';
import AgendamentoList from './components/AgendamentoList';
import AgendamentoForm from './components/AgendamentoForm';
import AtendimentoList from './components/AtendimentoList';
import AtendimentoForm from './components/AtendimentoForm';
import DocumentoList from './components/DocumentoList';
import DocumentoForm from './components/DocumentoForm';
import UserList from './components/UserList';
import UserForm from './components/UserForm';
import ClinicaList from './components/ClinicaList';
import ClinicaForm from './components/ClinicaForm';
import LancamentoFinanceiroList from './components/LancamentoFinanceiroList';
import LancamentoFinanceiroForm from './components/LancamentoFinanceiroForm';
import LeadList from './components/LeadList';
import LeadForm from './components/LeadForm';
import TipoTratamentoList from './components/TipoTratamentoList';
import TipoTratamentoForm from './components/TipoTratamentoForm';
import ProfissionalAgenda from './components/ProfissionalAgenda';
import PacienteDashboard from './components/paciente_portal/PacienteDashboard';
import PacienteAgendamentos from './components/paciente_portal/PacienteAgendamentos';
import PacienteProntuarios from './components/paciente_portal/PacienteProntuarios';
import PacienteDocumentos from './components/paciente_portal/PacienteDocumentos';
import PacienteLancamentosFinanceiros from './components/paciente_portal/PacienteLancamentosFinanceiros';
import PacienteAgendarConsultaForm from './components/paciente_portal/PacienteAgendarConsultaForm';
import CampanhaMarketingList from './components/CampanhaMarketingList';
import CampanhaMarketingForm from './components/CampanhaMarketingForm';
import ComissaoList from './components/ComissaoList';
import ComissaoForm from './components/ComissaoForm';
import FaturaList from './components/FaturaList';
import FaturaForm from './components/FaturaForm';
import PesquisaSatisfacaoList from './components/PesquisaSatisfacaoList';
import PesquisaSatisfacaoForm from './components/PesquisaSatisfacaoForm';
import CupomDescontoList from './components/CupomDescontoList';
import CupomDescontoForm from './components/CupomDescontoForm';
import ProntuarioList from './components/ProntuarioList';
import ProntuarioForm from './components/ProntuarioForm';
import GerenciamentoPerfis from './components/GerenciamentoPerfis';

import { AuthProvider } from './context/AuthContext';

import Login from './components/Login';

import PacienteForm from './components/PacienteForm';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="pacientes" element={<PacienteList />} />
            <Route path="pacientes/new" element={<PacienteForm />} />
            <Route path="pacientes/:id/edit" element={<PacienteForm />} />
            <Route path="agendamentos" element={<AgendamentoList />} />
            <Route path="agendamentos/new" element={<AgendamentoForm />} />
            <Route path="agendamentos/:id/edit" element={<AgendamentoForm />} />
            <Route path="atendimentos" element={<AtendimentoList />} />
            <Route path="atendimentos/new" element={<AtendimentoForm />} />
            <Route path="atendimentos/:id/edit" element={<AtendimentoForm />} />
            <Route path="documentos" element={<DocumentoList />} />
            <Route path="documentos/new" element={<DocumentoForm />} />
            <Route path="documentos/:id/edit" element={<DocumentoForm />} />
            <Route path="users" element={<UserList />} />
            <Route path="users/new" element={<UserForm />} />
            <Route path="users/:id/edit" element={<UserForm />} />
            <Route path="clinicas" element={<ClinicaList />} />
            <Route path="clinicas/new" element={<ClinicaForm />} />
            <Route path="clinicas/:id/edit" element={<ClinicaForm />} />
            <Route path="financeiro" element={<LancamentoFinanceiroList />} />
            <Route path="financeiro/new" element={<LancamentoFinanceiroForm />} />
            <Route path="financeiro/:id/edit" element={<LancamentoFinanceiroForm />} />
            <Route path="crm" element={<LeadList />} />
            <Route path="crm/new" element={<LeadForm />} />
            <Route path="crm/:id/edit" element={<LeadForm />} />
            <Route path="tipos-tratamento" element={<TipoTratamentoList />} />
            <Route path="tipos-tratamento/new" element={<TipoTratamentoForm />} />
            <Route path="tipos-tratamento/:id/edit" element={<TipoTratamentoForm />} />
            <Route path="portal-profissional" element={<ProfissionalAgenda />} />
            <Route path="portal-paciente" element={<PacienteDashboard />} />
            <Route path="portal-paciente/agendamentos" element={<PacienteAgendamentos />} />
            <Route path="portal-paciente/prontuarios" element={<PacienteProntuarios />} />
            <Route path="portal-paciente/documentos" element={<PacienteDocumentos />} />
            <Route path="portal-paciente/lancamentos-financeiros" element={<PacienteLancamentosFinanceiros />} />
            <Route path="portal-paciente/agendar-consulta" element={<PacienteAgendarConsultaForm />} />
            <Route path="campanhas-marketing" element={<CampanhaMarketingList />} />
            <Route path="campanhas-marketing/new" element={<CampanhaMarketingForm />} />
            <Route path="campanhas-marketing/:id/edit" element={<CampanhaMarketingForm />} />
            <Route path="comissoes" element={<ComissaoList />} />
            <Route path="comissoes/new" element={<ComissaoForm />} />
            <Route path="comissoes/:id/edit" element={<ComissaoForm />} />
            <Route path="faturas" element={<FaturaList />} />
            <Route path="faturas/new" element={<FaturaForm />} />
            <Route path="faturas/:id/edit" element={<FaturaForm />} />
            <Route path="pesquisas-satisfacao" element={<PesquisaSatisfacaoList />} />
            <Route path="pesquisas-satisfacao/new" element={<PesquisaSatisfacaoForm />} />
            <Route path="pesquisas-satisfacao/:id/edit" element={<PesquisaSatisfacaoForm />} />
            <Route path="cupons-desconto" element={<CupomDescontoList />} />
            <Route path="cupons-desconto/new" element={<CupomDescontoForm />} />
            <Route path="cupons-desconto/:id/edit" element={<CupomDescontoForm />} />
            <Route path="prontuarios" element={<ProntuarioList />} />
            <Route path="prontuarios/new" element={<ProntuarioForm />} />
            <Route path="prontuarios/:id/edit" element={<ProntuarioForm />} />
            <Route path="admin/perfis" element={<GerenciamentoPerfis />} />
            {/* Outras rotas serão adicionadas aqui */}
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;