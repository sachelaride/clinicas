import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AtendimentoList = () => {
    const [atendimentos, setAtendimentos] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedAtendimento, setSelectedAtendimento] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchAtendimentos();
    }, []);

    const fetchAtendimentos = () => {
        axios.get('/api/atendimentos/')
            .then(response => {
                setAtendimentos(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/atendimentos/${selectedAtendimento.id}/`)
            .then(() => {
                fetchAtendimentos();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (atendimento) => {
        setSelectedAtendimento(atendimento);
        setShowDeleteModal(true);
    };

    const filteredAtendimentos = atendimentos.filter(atendimento => {
        const pacienteNome = atendimento.paciente_nome || '';
        return pacienteNome.toLowerCase().includes(searchTerm.toLowerCase());
    });

    const canManageAtendimentos = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR' || user.perfil === 'ATENDENTE');

    return (
        <Container>
            <h1 className="my-4">Lista de Atendimentos</h1>
            {canManageAtendimentos && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/atendimentos/new')}>Novo Atendimento</Button>
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
                        <th>Data de Início</th>
                        <th>Status</th>
                        {canManageAtendimentos && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredAtendimentos.map(atendimento => (
                        <tr key={atendimento.id}>
                            <td>{atendimento.paciente_nome}</td>
                            <td>{atendimento.profissional_username}</td>
                            <td>{new Date(atendimento.data_inicio).toLocaleString()}</td>
                            <td>{atendimento.status}</td>
                            {canManageAtendimentos && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/atendimentos/${atendimento.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(atendimento)}>Excluir</Button>
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
                    Tem certeza que deseja excluir o atendimento do paciente <strong>{selectedAtendimento?.agendamento__paciente__nome}</strong>?
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

export default AtendimentoList;
