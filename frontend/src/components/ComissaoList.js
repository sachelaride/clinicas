import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ComissaoList = () => {
    const [comissoes, setComissoes] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedComissao, setSelectedComissao] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchComissoes();
    }, []);

    const fetchComissoes = () => {
        axios.get('/api/comissoes/')
            .then(response => {
                setComissoes(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/comissoes/${selectedComissao.id}/`)
            .then(() => {
                fetchComissoes();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (comissao) => {
        setSelectedComissao(comissao);
        setShowDeleteModal(true);
    };

    const filteredComissoes = comissoes.filter(comissao =>
        comissao.profissional__user__username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        comissao.atendimento__id.toString().includes(searchTerm.toLowerCase())
    );

    const canManageComissoes = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">Lista de Comissões</h1>
            {canManageComissoes && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/comissoes/new')}>Nova Comissão</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por profissional ou atendimento..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Profissional</th>
                        <th>Atendimento ID</th>
                        <th>Valor</th>
                        <th>Paga</th>
                        {canManageComissoes && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredComissoes.map(comissao => (
                        <tr key={comissao.id}>
                            <td>{comissao.profissional__user__username}</td>
                            <td>{comissao.atendimento__id}</td>
                            <td>R$ {parseFloat(comissao.valor).toFixed(2)}</td>
                            <td>{comissao.paga ? 'Sim' : 'Não'}</td>
                            {canManageComissoes && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/comissoes/${comissao.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(comissao)}>Excluir</Button>
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
                    Tem certeza que deseja excluir a comissão do atendimento <strong>{selectedComissao?.atendimento__id}</strong>?
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

export default ComissaoList;
