import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const TipoTratamentoList = () => {
    const [tiposTratamento, setTiposTratamento] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedTipoTratamento, setSelectedTipoTratamento] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchTiposTratamento();
    }, []);

    const fetchTiposTratamento = () => {
        axios.get('/api/tipos-tratamento/')
            .then(response => {
                setTiposTratamento(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/tipos-tratamento/${selectedTipoTratamento.id}/`)
            .then(() => {
                fetchTiposTratamento();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (tipo) => {
        setSelectedTipoTratamento(tipo);
        setShowDeleteModal(true);
    };

    const filteredTiposTratamento = tiposTratamento.filter(tipo =>
        tipo.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        tipo.descricao.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canManageTiposTratamento = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">Lista de Tipos de Tratamento</h1>
            {canManageTiposTratamento && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/tipos-tratamento/new')}>Novo Tipo de Tratamento</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome ou descrição..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Descrição</th>
                        <th>Tempo Mínimo Atendimento</th>
                        <th>Clínica</th>
                        {canManageTiposTratamento && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredTiposTratamento.map(tipo => (
                        <tr key={tipo.id}>
                            <td>{tipo.nome}</td>
                            <td>{tipo.descricao}</td>
                            <td>{tipo.tempo_minimo_atendimento} min</td>
                            <td>{tipo.clinica_nome}</td>
                            {canManageTiposTratamento && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/tipos-tratamento/${tipo.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(tipo)}>Excluir</Button>
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
                    Tem certeza que deseja excluir o tipo de tratamento <strong>{selectedTipoTratamento?.nome}</strong>?
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

export default TipoTratamentoList;
