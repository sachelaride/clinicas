import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

// Mock react-router-dom with only necessary mocks
jest.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }) => <div>{children}</div>,
  Routes: ({ children }) => <div>{children}</div>,
  Route: ({ children }) => <div>{children}</div>,
  useNavigate: () => jest.fn(),
  Link: ({ children, to }) => <a href={to}>{children}</a>,
}));

jest.mock('./context/AuthContext', () => ({
  AuthProvider: ({ children }) => <div>{children}</div>,
  useAuth: () => ({ user: null, setUser: jest.fn() }),
}));

// Mock components used in App.js to avoid deep rendering issues
jest.mock('./components/Layout', () => () => <div>Layout Component</div>);
jest.mock('./components/Dashboard', () => () => <div>Dashboard Component</div>);
jest.mock('./components/Login', () => () => <div>Login Component</div>);
jest.mock('./components/PacienteList', () => () => <div>PacienteList Component</div>);
jest.mock('./components/AgendamentoList', () => () => <div>AgendamentoList Component</div>);
jest.mock('./components/AtendimentoList', () => () => <div>AtendimentoList Component</div>);
jest.mock('./components/DocumentoList', () => () => <div>DocumentoList Component</div>);
jest.mock('./components/UserList', () => () => <div>UserList Component</div>);
jest.mock('./components/ClinicaList', () => () => <div>ClinicaList Component</div>);
jest.mock('./components/LancamentoFinanceiroList', () => () => <div>LancamentoFinanceiroList Component</div>);
jest.mock('./components/LeadList', () => () => <div>LeadList Component</div>);
jest.mock('./components/TipoTratamentoList', () => () => <div>TipoTratamentoList Component</div>);
jest.mock('./components/ProfissionalAgenda', () => () => <div>ProfissionalAgenda Component</div>);
jest.mock('./components/paciente_portal/PacienteDashboard', () => () => <div>PacienteDashboard Component</div>);
jest.mock('./components/paciente_portal/PacienteAgendamentos', () => () => <div>PacienteAgendamentos Component</div>);
jest.mock('./components/paciente_portal/PacienteProntuarios', () => () => <div>PacienteProntuarios Component</div>);
jest.mock('./components/paciente_portal/PacienteDocumentos', () => () => <div>PacienteDocumentos Component</div>);
jest.mock('./components/paciente_portal/PacienteLancamentosFinanceiros', () => () => <div>PacienteLancamentosFinanceiros Component</div>);
jest.mock('./components/paciente_portal/PacienteAgendarConsultaForm', () => () => <div>PacienteAgendarConsultaForm Component</div>);
jest.mock('./components/CampanhaMarketingList', () => () => <div>CampanhaMarketingList Component</div>);
jest.mock('./components/CampanhaMarketingForm', () => () => <div>CampanhaMarketingForm Component</div>);
jest.mock('./components/ComissaoList', () => () => <div>ComissaoList Component</div>);
jest.mock('./components/ComissaoForm', () => () => <div>ComissaoForm Component</div>);
jest.mock('./components/FaturaList', () => () => <div>FaturaList Component</div>);
jest.mock('./components/FaturaForm', () => () => <div>FaturaForm Component</div>);
jest.mock('./components/PesquisaSatisfacaoList', () => () => <div>PesquisaSatisfacaoList Component</div>);
jest.mock('./components/PesquisaSatisfacaoForm', () => () => <div>PesquisaSatisfacaoForm Component</div>);
jest.mock('./components/CupomDescontoList', () => () => <div>CupomDescontoList Component</div>);
jest.mock('./components/CupomDescontoForm', () => () => <div>CupomDescontoForm Component</div>);
jest.mock('./components/ProntuarioList', () => () => <div>ProntuarioList Component</div>);
jest.mock('./components/ProntuarioForm', () => () => <div>ProntuarioForm Component</div>);
jest.mock('./components/GerenciamentoPerfis', () => () => <div>GerenciamentoPerfis Component</div>);
jest.mock('./components/PacienteForm', () => () => <div>PacienteForm Component</div>);

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    // If render does not throw an error, the component rendered successfully
  });
});