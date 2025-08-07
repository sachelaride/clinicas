import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Button, Modal, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LancamentoFinanceiroList = () => {
    const [lancamentos, setLancamentos] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterType, setFilterType] = useState(''); // 'RECEITA' ou 'DESPESA'
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedLancamento, setSelectedLancamento] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchLancamentos();
    }, [filterType]); // Recarrega quando o tipo de filtro muda

    const fetchLancamentos = () => {
        axios.get('/api/lancamentos-financeiros/')
            .then(response => {
                setLancamentos(response.data);
            })
            .catch(error => {
                console.error('Error fetching financial entries: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/lancamentos-financeiros/${selectedLancamento.id}/`)
            .then(() => {
                fetchLancamentos();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting financial entry: ', error);
            });
    };

    const openDeleteModal = (lancamento) => {
        setSelectedLancamento(lancamento);
        setShowDeleteModal(true);
    };

    const filteredLancamentos = lancamentos.filter(lancamento =>
        lancamento.descricao.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canManageLancamentos = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">Lançamentos Financeiros</h1>
            {canManageLancamentos && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/lancamentos-financeiros/new')}>Novo Lançamento</Button>
            )}

            <Form.Group controlId="search" className="mb-3">
                <Form.Control
                    type="text"
                    placeholder="Buscar por descrição..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>

            <Form.Group controlId="filterType" className="mb-3">
                <Form.Label>Filtrar por Tipo</Form.Label>
                <Form.Control as="select" value={filterType} onChange={e => setFilterType(e.target.value)}>
                    <option value="">Todos</option>
                    <option value="RECEITA">Receita</option>
                    <option value="DESPESA">Despesa</option>
                </Form.Control>
            </Form.Group>

            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Tipo</th>
                        <th>Descrição</th>
                        <th>Valor</th>
                        <th>Vencimento</th>
                        <th>Pagamento</th>
                        {canManageLancamentos && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredLancamentos.map(lancamento => (
                        <tr key={lancamento.id}>
                            <td>{lancamento.tipo}</td>
                            <td>{lancamento.descricao}</td>
                            <td>R$ {parseFloat(lancamento.valor).toFixed(2)}</td>
                            <td>{lancamento.data_vencimento}</td>
                            <td>{lancamento.data_pagamento || '-'}</td>
                            {canManageLancamentos && (
                                <td>
                                    <Button variant="primary" size="sm" className="me-2" onClick={() => navigate(`/lancamentos-financeiros/${lancamento.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(lancamento)}>Excluir</Button>
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
                    Tem certeza que deseja excluir o lançamento "{selectedLancamento?.descricao}" (R$ {selectedLancamento?.valor})?
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

export default LancamentoFinanceiroList;