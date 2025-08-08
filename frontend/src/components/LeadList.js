import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasPermission } from '../utils/permissions';

const LeadList = () => {
    const [leads, setLeads] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedLead, setSelectedLead] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchLeads();
    }, []);

    const fetchLeads = () => {
        axios.get('/api/leads/')
            .then(response => {
                setLeads(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/leads/${selectedLead.id}/`)
            .then(() => {
                fetchLeads();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (lead) => {
        setSelectedLead(lead);
        setShowDeleteModal(true);
    };

    const filteredLeads = leads.filter(lead =>
        lead.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.telefone.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canCreateLeads = hasPermission(user, 'criar_leads');
    const canUpdateLeads = hasPermission(user, 'atualizar_leads');
    const canDeleteLeads = hasPermission(user, 'excluir_leads');

    return (
        <Container>
            <h1 className="my-4">Lista de Leads</h1>
            {canCreateLeads && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/crm/new')}>Novo Lead</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome, email ou telefone..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Telefone</th>
                        <th>Origem</th>
                        <th>Status</th>
                        {(canUpdateLeads || canDeleteLeads) && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredLeads.map(lead => (
                        <tr key={lead.id}>
                            <td>{lead.nome}</td>
                            <td>{lead.email}</td>
                            <td>{lead.telefone}</td>
                            <td>{lead.origem}</td>
                            <td>{lead.status}</td>
                            {(canUpdateLeads || canDeleteLeads) && (
                                <td>
                                    {canUpdateLeads && <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/crm/${lead.id}/edit`)}>Editar</Button>}
                                    {canDeleteLeads && <Button variant="danger" size="sm" onClick={() => openDeleteModal(lead)}>Excluir</Button>}
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
                    Tem certeza que deseja excluir o lead <strong>{selectedLead?.nome}</strong>?
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

export default LeadList;
