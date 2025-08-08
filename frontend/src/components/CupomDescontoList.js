import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const CupomDescontoList = () => {
    const [cupons, setCupons] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedCupom, setSelectedCupom] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchCupons();
    }, []);

    const fetchCupons = () => {
        axios.get('/api/cupons-desconto/')
            .then(response => {
                setCupons(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/cupons-desconto/${selectedCupom.id}/`)
            .then(() => {
                fetchCupons();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (cupom) => {
        setSelectedCupom(cupom);
        setShowDeleteModal(true);
    };

    const filteredCupons = cupons.filter(cupom =>
        cupom.codigo.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (cupom.campanha__nome && cupom.campanha__nome.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    const canCreateCupons = hasPermission(user, 'criar_cupons_desconto');
    const canUpdateCupons = hasPermission(user, 'atualizar_cupons_desconto');
    const canDeleteCupons = hasPermission(user, 'excluir_cupons_desconto');

    return (
        <Container>
            <h1 className="my-4">Lista de Cupons de Desconto</h1>
            {canCreateCupons && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/cupons-desconto/new')}>Novo Cupom</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por código ou campanha..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Valor de Desconto</th>
                        <th>Data de Validade</th>
                        <th>Ativo</th>
                        <th>Campanha</th>
                        {(canUpdateCupons || canDeleteCupons) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredCupons.map(cupom => (
                        <tr key={cupom.id}>
                            <td>{cupom.codigo}</td>
                            <td>R$ {parseFloat(cupom.valor_desconto).toFixed(2)}</td>
                            <td>{new Date(cupom.data_validade).toLocaleDateString()}</td>
                            <td>{cupom.ativo ? 'Sim' : 'Não'}</td>
                            <td>{cupom.campanha__nome || '-'}</td>
                            {(canUpdateCupons || canDeleteCupons) && (
                                <td>
                                    {canUpdateCupons && <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/cupons-desconto/${cupom.id}/edit`)}>Editar</Button>}
                                    {canDeleteCupons && <Button variant="danger" size="sm" onClick={() => openDeleteModal(cupom)}>Excluir</Button>}
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
                    Tem certeza que deseja excluir o cupom <strong>{selectedCupom?.codigo}</strong>?
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

export default CupomDescontoList;
