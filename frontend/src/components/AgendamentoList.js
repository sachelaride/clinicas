import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AgendamentoList = () => {
    const [agendamentos, setAgendamentos] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedAgendamento, setSelectedAgendamento] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchAgendamentos();
    }, []);

    const fetchAgendamentos = () => {
        axios.get('/api/agendamentos/')
            .then(response => {
                setAgendamentos(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/agendamentos/${selectedAgendamento.id}/`)
            .then(() => {
                fetchAgendamentos();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (agendamento) => {
        setSelectedAgendamento(agendamento);
        setShowDeleteModal(true);
    };

    const filteredAgendamentos = agendamentos.filter(agendamento => {
        const pacienteNome = agendamento.paciente_nome || '';
        return pacienteNome.toLowerCase().includes(searchTerm.toLowerCase());
    });

    const canManageAgendamentos = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR' || user.perfil === 'ATENDENTE');

    return (
        <Container>
            <h1 className="my-4">Lista de Agendamentos</h1>
            {canManageAgendamentos && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/agendamentos/new')}>Novo Agendamento</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome do paciente..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Paciente</th>
                        <th>Profissional</th>
                        <th>Data</th>
                        <th>Status</th>
                        {canManageAgendamentos && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredAgendamentos.map(agendamento => (
                        <tr key={agendamento.id}>
                            <td>{agendamento.paciente_nome}</td>
                            <td>{agendamento.profissional_username}</td>
                            <td>{new Date(agendamento.data).toLocaleString()}</td>
                            <td>{agendamento.status}</td>
                            {canManageAgendamentos && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/agendamentos/${agendamento.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(agendamento)}>Excluir</Button>
                                </td>
                            )}
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Confirmar Exclusão</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Tem certeza que deseja excluir o agendamento de <strong>{selectedAgendamento?.paciente__nome}</strong> em <strong>{selectedAgendamento?.data ? new Date(selectedAgendamento.data).toLocaleString() : ''}</strong>?
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
                        Cancelar
                    </Button>
                    <Button variant="danger" onClick={handleDelete}>
                        Excluir
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}

export default AgendamentoList;
