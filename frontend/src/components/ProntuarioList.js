import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Button, Modal, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const ProntuarioList = () => {
    const [prontuarios, setProntuarios] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedProntuario, setSelectedProntuario] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchProntuarios();
    }, []);

    const fetchProntuarios = () => {
        axios.get('/api/prontuarios/')
            .then(response => {
                setProntuarios(response.data);
            })
            .catch(error => {
                console.error('Error fetching prontuarios: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/prontuarios/${selectedProntuario.id}/`)
            .then(() => {
                fetchProntuarios();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting prontuario: ', error);
            });
    };

    const openDeleteModal = (prontuario) => {
        setSelectedProntuario(prontuario);
        setShowDeleteModal(true);
    };

    const filteredProntuarios = prontuarios.filter(prontuario =>
        prontuario.paciente_nome.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canCreateProntuarios = hasPermission(user, 'criar_prontuarios');
    const canUpdateProntuarios = hasPermission(user, 'atualizar_prontuarios');
    const canDeleteProntuarios = hasPermission(user, 'excluir_prontuarios');

    return (
        <Container>
            <h1 className="my-4">Lista de Prontuários</h1>
            {canCreateProntuarios && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/prontuarios/new')}>Novo Prontuário</Button>
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
                        <th>ID</th>
                        <th>Paciente</th>
                        <th>Data de Criação</th>
                        <th>Finalizado</th>
                        {(canUpdateProntuarios || canDeleteProntuarios) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredProntuarios.map(prontuario => (
                        <tr key={prontuario.id}>
                            <td>{prontuario.id}</td>
                            <td>{prontuario.paciente_nome}</td>
                            <td>{new Date(prontuario.data_criacao).toLocaleDateString()}</td>
                            <td>{prontuario.is_finalized ? 'Sim' : 'Não'}</td>
                            {(canUpdateProntuarios || canDeleteProntuarios) && (
                                <td>
                                    {canUpdateProntuarios && <Button variant="primary" size="sm" className="me-2" onClick={() => navigate(`/prontuarios/${prontuario.id}/edit`)}>Editar</Button>}
                                    {canDeleteProntuarios && <Button variant="danger" size="sm" onClick={() => openDeleteModal(prontuario)}>Excluir</Button>}
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
                    Tem certeza que deseja excluir o prontuário do paciente "{selectedProntuario?.paciente_nome}" (ID: {selectedProntuario?.id})?
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
};

export default ProntuarioList;
