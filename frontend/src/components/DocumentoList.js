import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const DocumentoList = () => {
    const [documentos, setDocumentos] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedDocumento, setSelectedDocumento] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth();

    useEffect(() => {
        fetchDocumentos();
    }, []);

    const fetchDocumentos = () => {
        axios.get('/api/documentos/')
            .then(response => {
                setDocumentos(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/documentos/${selectedDocumento.id}/`)
            .then(() => {
                fetchDocumentos();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (documento) => {
        setSelectedDocumento(documento);
        setShowDeleteModal(true);
    };

    const filteredDocumentos = documentos.filter(documento => {
        const pacienteNome = documento.paciente_nome || '';
        return pacienteNome.toLowerCase().includes(searchTerm.toLowerCase());
    });

    const canManageDocumentos = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">Lista de Documentos</h1>
            {canManageDocumentos && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/documentos/new')}>Novo Documento</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome do paciente..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Paciente</th>
                        <th>Pasta</th>
                        <th>Arquivo</th>
                        <th>Data de Upload</th>
                        {canManageDocumentos && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredDocumentos.map(documento => (
                        <tr key={documento.id}>
                            <td>{documento.paciente_nome}</td>
                            <td>{documento.pasta_nome}</td>
                            <td><a href={documento.arquivo} target="_blank" rel="noreferrer">{documento.arquivo}</a></td>
                            <td>{new Date(documento.uploaded_at).toLocaleString()}</td>
                            {canManageDocumentos && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/documentos/${documento.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(documento)}>Excluir</Button>
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
                    Tem certeza que deseja excluir o documento de <strong>{selectedDocumento?.paciente__nome}</strong>?
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

export default DocumentoList;
