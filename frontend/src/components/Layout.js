import React, { useState, useEffect } from 'react';
import { Link, Outlet } from 'react-router-dom';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const Layout = () => {
    const { user } = useAuth();
    const [clinicName, setClinicName] = useState('Sistema de Clínicas');

    // Função auxiliar para verificar permissões
    const hasPermission = (permissionName) => {
        console.log(`Checking permission: ${permissionName}`);
        console.log("User permissions:", user && user.perfil && user.perfil.permissoes);
        return user && user.perfil && user.perfil.permissoes.some(p => p.nome === permissionName);
    };

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
            {console.log("User object in Layout.js:", user)}
            <Navbar bg="primary" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand as={Link} to="/">{clinicName}</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            {user && (
                                <>
                                    {hasPermission('admin_acesso') && (
                                        <NavDropdown title={<><i className="fa-solid fa-tags"></i> Configurações</>} id="configuracoes-dropdown">
                                            {hasPermission('ler_usuarios') && <NavDropdown.Item as={Link} to="/users">Usuários</NavDropdown.Item>}
                                            {hasPermission('ler_clinicas') && <NavDropdown.Item as={Link} to="/clinicas">Clínicas</NavDropdown.Item>}
                                            {hasPermission('ler_tipos_tratamento') && <NavDropdown.Item as={Link} to="/tipos-tratamento">Tipos de Tratamento</NavDropdown.Item>}
                                            {hasPermission('ler_perfis') && <NavDropdown.Item as={Link} to="/admin/perfis">Gerenciamento de Perfis</NavDropdown.Item>}
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
