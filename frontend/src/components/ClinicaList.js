import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const ClinicaList = () => {
    const [clinicas, setClinicas] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedClinica, setSelectedClinica] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchClinicas();
    }, []);

    const fetchClinicas = () => {
        axios.get('/api/clinicas/')
            .then(response => {
                setClinicas(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/clinicas/${selectedClinica.id}/`)
            .then(() => {
                fetchClinicas();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (clinica) => {
        setSelectedClinica(clinica);
        setShowDeleteModal(true);
    };

    const filteredClinicas = clinicas.filter(clinica =>
        clinica.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        clinica.endereco.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canCreateClinicas = hasPermission(user, 'criar_clinicas');
    const canUpdateClinicas = hasPermission(user, 'atualizar_clinicas');
    const canDeleteClinicas = hasPermission(user, 'excluir_clinicas');

    return (
        <Container>
            <h1 className="my-4">Lista de Clínicas</h1>
            {canCreateClinicas && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/clinicas/new')}>Nova Clínica</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome ou endereço..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Endereço</th>
                        <th>Telefone</th>
                        <th>Guichês</th>
                        <th>Tempo Mínimo Atendimento</th>
                        {(canUpdateClinicas || canDeleteClinicas) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredClinicas.map(clinica => (
                        <tr key={clinica.id}>
                            <td>{clinica.nome}</td>
                            <td>{clinica.endereco}</td>
                            <td>{clinica.telefone}</td>
                            <td>{clinica.num_guiches}</td>
                            <td>{clinica.tempo_minimo_atendimento} min</td>
                            {(canUpdateClinicas || canDeleteClinicas) && (
                                <td>
                                    {canUpdateClinicas && <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/clinicas/${clinica.id}/edit`)}>Editar</Button>}
                                    {canDeleteClinicas && <Button variant="danger" size="sm" onClick={() => openDeleteModal(clinica)}>Excluir</Button>}
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
                    Tem certeza que deseja excluir a clínica <strong>{selectedClinica?.nome}</strong>?
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

export default ClinicaList;