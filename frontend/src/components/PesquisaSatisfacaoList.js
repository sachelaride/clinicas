import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const PesquisaSatisfacaoList = () => {
    const [pesquisas, setPesquisas] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedPesquisa, setSelectedPesquisa] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchPesquisas();
    }, []);

    const fetchPesquisas = () => {
        axios.get('/api/pesquisas-satisfacao/')
            .then(response => {
                setPesquisas(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/pesquisas-satisfacao/${selectedPesquisa.id}/`)
            .then(() => {
                fetchPesquisas();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (pesquisa) => {
        setSelectedPesquisa(pesquisa);
        setShowDeleteModal(true);
    };

    const filteredPesquisas = pesquisas.filter(pesquisa =>
        pesquisa.paciente__nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        pesquisa.comentarios.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canCreatePesquisas = hasPermission(user, 'criar_pesquisas_satisfacao');
    const canUpdatePesquisas = hasPermission(user, 'atualizar_pesquisas_satisfacao');
    const canDeletePesquisas = hasPermission(user, 'excluir_pesquisas_satisfacao');

    return (
        <Container>
            <h1 className="my-4">Lista de Pesquisas de Satisfação</h1>
            {canCreatePesquisas && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/pesquisas-satisfacao/new')}>Nova Pesquisa</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por paciente ou comentários..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Paciente</th>
                        <th>Data da Pesquisa</th>
                        <th>Nota NPS</th>
                        <th>Comentários</th>
                        {(canUpdatePesquisas || canDeletePesquisas) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredPesquisas.map(pesquisa => (
                        <tr key={pesquisa.id}>
                            <td>{pesquisa.paciente__nome}</td>
                            <td>{new Date(pesquisa.data_pesquisa).toLocaleDateString()}</td>
                            <td>{pesquisa.nota_nps}</td>
                            <td>{pesquisa.comentarios}</td>
                            {(canUpdatePesquisas || canDeletePesquisas) && (
                                <td>
                                    {canUpdatePesquisas && <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/pesquisas-satisfacao/${pesquisa.id}/edit`)}>Editar</Button>}
                                    {canDeletePesquisas && <Button variant="danger" size="sm" onClick={() => openDeleteModal(pesquisa)}>Excluir</Button>}
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
                    Tem certeza que deseja excluir a pesquisa de <strong>{selectedPesquisa?.paciente__nome}</strong>?
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

export default PesquisaSatisfacaoList;
