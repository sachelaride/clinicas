import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const PacienteList = () => {
    const [pacientes, setPacientes] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedPaciente, setSelectedPaciente] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchPacientes();
    }, []);

    const fetchPacientes = () => {
        axios.get('/api/pacientes/')
            .then(response => {
                setPacientes(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/pacientes/${selectedPaciente.id}/`)
            .then(() => {
                fetchPacientes();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (paciente) => {
        setSelectedPaciente(paciente);
        setShowDeleteModal(true);
    };

    const filteredPacientes = pacientes.filter(paciente =>
        paciente.nome.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canCreatePacientes = hasPermission(user, 'criar_pacientes');
    const canUpdatePacientes = hasPermission(user, 'atualizar_pacientes');
    const canDeletePacientes = hasPermission(user, 'excluir_pacientes');

    return (
        <Container>
            <h1 className="my-4">Lista de Pacientes</h1>
            {canCreatePacientes && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/pacientes/new')}>Novo Paciente</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>CPF</th>
                        <th>Email</th>
                        <th>Telefone</th>
                        {(canUpdatePacientes || canDeletePacientes) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredPacientes.map(paciente => (
                        <tr key={paciente.id}>
                            <td>{paciente.nome}</td>
                            <td>{paciente.cpf}</td>
                            <td>{paciente.email}</td>
                            <td>{paciente.telefone}</td>
                            {(canUpdatePacientes || canDeletePacientes) && (
                                <td>
                                    {canUpdatePacientes && <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/pacientes/${paciente.id}/edit`)}>Editar</Button>}
                                    {canDeletePacientes && <Button variant="danger" size="sm" onClick={() => openDeleteModal(paciente)}>Excluir</Button>}
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
                    Atenção: Ao excluir este paciente, todos os seus agendamentos e prontuários associados também serão permanentemente removidos. Deseja continuar?
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

export default PacienteList;
