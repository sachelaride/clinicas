import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const FaturaList = () => {
    const [faturas, setFaturas] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedFatura, setSelectedFatura] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchFaturas();
    }, []);

    const fetchFaturas = () => {
        axios.get('/api/faturas/')
            .then(response => {
                setFaturas(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/faturas/${selectedFatura.id}/`)
            .then(() => {
                fetchFaturas();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (fatura) => {
        setSelectedFatura(fatura);
        setShowDeleteModal(true);
    };

    const filteredFaturas = faturas.filter(fatura =>
        fatura.convenio__nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        fatura.status.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canCreateFaturas = hasPermission(user, 'criar_faturas');
    const canUpdateFaturas = hasPermission(user, 'atualizar_faturas');
    const canDeleteFaturas = hasPermission(user, 'excluir_faturas');

    return (
        <Container>
            <h1 className="my-4">Lista de Faturas</h1>
            {canCreateFaturas && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/faturas/new')}>Nova Fatura</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por convênio ou status..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Convênio</th>
                        <th>Mês de Referência</th>
                        <th>Valor Total</th>
                        <th>Status</th>
                        {(canUpdateFaturas || canDeleteFaturas) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredFaturas.map(fatura => (
                        <tr key={fatura.id}>
                            <td>{fatura.convenio__nome}</td>
                            <td>{new Date(fatura.mes_referencia).toLocaleDateString()}</td>
                            <td>R$ {parseFloat(fatura.valor_total).toFixed(2)}</td>
                            <td>{fatura.status}</td>
                            {(canUpdateFaturas || canDeleteFaturas) && (
                                <td>
                                    {canUpdateFaturas && <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/faturas/${fatura.id}/edit`)}>Editar</Button>}
                                    {canDeleteFaturas && <Button variant="danger" size="sm" onClick={() => openDeleteModal(fatura)}>Excluir</Button>}
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
                    Tem certeza que deseja excluir a fatura de <strong>{selectedFatura?.convenio__nome}</strong> referente a <strong>{selectedFatura?.mes_referencia ? new Date(selectedFatura.mes_referencia).toLocaleDateString() : ''}</strong>?
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

export default FaturaList;
