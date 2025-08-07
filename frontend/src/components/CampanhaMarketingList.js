import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const CampanhaMarketingList = () => {
    const [campanhas, setCampanhas] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedCampanha, setSelectedCampanha] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchCampanhas();
    }, []);

    const fetchCampanhas = () => {
        axios.get('/api/campanhas-marketing/')
            .then(response => {
                setCampanhas(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/campanhas-marketing/${selectedCampanha.id}/`)
            .then(() => {
                fetchCampanhas();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (campanha) => {
        setSelectedCampanha(campanha);
        setShowDeleteModal(true);
    };

    const filteredCampanhas = campanhas.filter(campanha =>
        campanha.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        campanha.tipo.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canManageCampanhas = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">Lista de Campanhas de Marketing</h1>
            {canManageCampanhas && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/campanhas-marketing/new')}>Nova Campanha</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome ou tipo..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Tipo</th>
                        <th>Data de Início</th>
                        <th>Data de Fim</th>
                        {canManageCampanhas && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredCampanhas.map(campanha => (
                        <tr key={campanha.id}>
                            <td>{campanha.nome}</td>
                            <td>{campanha.tipo}</td>
                            <td>{new Date(campanha.data_inicio).toLocaleDateString()}</td>
                            <td>{campanha.data_fim ? new Date(campanha.data_fim).toLocaleDateString() : '-'}</td>
                            {canManageCampanhas && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/campanhas-marketing/${campanha.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(campanha)}>Excluir</Button>
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
                    Tem certeza que deseja excluir a campanha <strong>{selectedCampanha?.nome}</strong>?
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

export default CampanhaMarketingList;
