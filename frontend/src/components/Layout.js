/**
 * Layout component
 * 
 * This component renders the main layout of the application, including the navigation bar and the main content area.
 */
import React, { useState, useEffect } from 'react';
import { Link, Outlet } from 'react-router-dom';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

import { hasPermission } from '../utils/permissions';

const Layout = () => {
    const { user } = useAuth();
    const [clinicName, setClinicName] = useState('Sistema de Clínicas');

    useEffect(() => {
        const fetchClinicData = async () => {
            if (user && user.clinica_id) {
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/api/clinicas/${user.clinica_id}/`);
                    setClinicName(response.data.nome);
                } catch (error) {
                    console.error('Erro ao buscar nome da clínica:', error);
                    setClinicName('Erro ao carregar nome da clínica');
                }
            } else {
                setClinicName('Sistema de Clínicas');
            }
        };

        fetchClinicData();
    }, [user]); // Dependência do user para re-executar quando o usuário for carregado

    return (
        <>
            {console.log("Layout.js rendered. User:", user)}
            <Navbar bg="primary" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand as={Link} to="/">{clinicName}</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            {user && (
                                <>
                                    {/* Cadastros Dropdown */}
                                    {(hasPermission(user, 'ler_pacientes') || hasPermission(user, 'ler_agendamentos') || hasPermission(user, 'ler_atendimentos') || hasPermission(user, 'ler_prontuarios')) && (
                                        <NavDropdown title={<><i className="fa-solid fa-notes-medical"></i> Cadastros</>} id="cadastros-dropdown">
                                            {hasPermission(user, 'ler_pacientes') && <NavDropdown.Item as={Link} to="/pacientes">Pacientes</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_agendamentos') && <NavDropdown.Item as={Link} to="/agendamentos">Agendamentos</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_atendimentos') && <NavDropdown.Item as={Link} to="/atendimentos">Atendimentos</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_prontuarios') && <NavDropdown.Item as={Link} to="/prontuarios">Prontuários</NavDropdown.Item>}
                                        </NavDropdown>
                                    )}

                                    {/* CRM Dropdown */}
                                    {(hasPermission(user, 'ler_leads')) && (
                                        <NavDropdown title={<><i className="fa-solid fa-users-line"></i> CRM</>} id="crm-dropdown">
                                            {hasPermission(user, 'ler_leads') && <NavDropdown.Item as={Link} to="/crm">Leads</NavDropdown.Item>}
                                        </NavDropdown>
                                    )}

                                    {/* Financeiro Dropdown */}
                                    {(hasPermission(user, 'ler_faturas') || hasPermission(user, 'ler_lancamentos_financeiros') || hasPermission(user, 'ler_comissoes')) && (
                                        <NavDropdown title={<><i className="fa-solid fa-dollar-sign"></i> Financeiro</>} id="financeiro-dropdown">
                                            {hasPermission(user, 'ler_faturas') && <NavDropdown.Item as={Link} to="/faturas">Faturas</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_lancamentos_financeiros') && <NavDropdown.Item as={Link} to="/financeiro">Lançamentos Financeiros</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_comissoes') && <NavDropdown.Item as={Link} to="/comissoes">Comissões</NavDropdown.Item>}
                                        </NavDropdown>
                                    )}

                                    {/* Marketing Dropdown */}
                                    {(hasPermission(user, 'ler_campanhas_marketing') || hasPermission(user, 'ler_pesquisas_satisfacao') || hasPermission(user, 'ler_cupons_desconto')) && (
                                        <NavDropdown title={<><i className="fa-solid fa-bullhorn"></i> Marketing</>} id="marketing-dropdown">
                                            {hasPermission(user, 'ler_campanhas_marketing') && <NavDropdown.Item as={Link} to="/campanhas-marketing">Campanhas de Marketing</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_pesquisas_satisfacao') && <NavDropdown.Item as={Link} to="/pesquisas-satisfacao">Pesquisas de Satisfação</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_cupons_desconto') && <NavDropdown.Item as={Link} to="/cupons-desconto">Cupons de Desconto</NavDropdown.Item>}
                                        </NavDropdown>
                                    )}

                                    {/* Configurações Dropdown */}
                                    {hasPermission(user, 'admin_acesso') && (
                                        <NavDropdown title={<><i className="fa-solid fa-tags"></i> Configurações</>} id="configuracoes-dropdown">
                                            {hasPermission(user, 'ler_usuarios') && <NavDropdown.Item as={Link} to="/users">Usuários</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_clinicas') && <NavDropdown.Item as={Link} to="/clinicas">Clínicas</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_tipos_tratamento') && <NavDropdown.Item as={Link} to="/tipos-tratamento">Tipos de Tratamento</NavDropdown.Item>}
                                            {hasPermission(user, 'ler_perfis') && <NavDropdown.Item as={Link} to="/admin/perfis">Gerenciamento de Perfis</NavDropdown.Item>}
                                        </NavDropdown>
                                    )}
                                </>
                            )}
                        </Nav>
                        <Nav>
                            {user ? (
                                <NavDropdown title={<><i className="fa-solid fa-user"></i> {user.username} ({user.perfil.nome})</>} id="basic-nav-dropdown">
                                    <NavDropdown.Item href="/logout"><i className="fa-solid fa-right-from-bracket"></i> Sair</NavDropdown.Item>
                                </NavDropdown>
                            ) : (
                                <Nav.Link as={Link} to="/login">Login</Nav.Link>
                            )}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            <Container className="mt-4">
                <Outlet />
            </Container>
        </>
    );
};

export default Layout;
