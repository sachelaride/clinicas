import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Table, Button, Form, Modal, Alert } from 'react-bootstrap';

const GerenciamentoPerfis = () => {
    const [perfis, setPerfis] = useState([]);
    const [permissoes, setPermissoes] = useState([]);
    const [selectedPerfil, setSelectedPerfil] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [newPerfilName, setNewPerfilName] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        fetchPerfis();
        fetchPermissoes();
    }, []);

    const fetchPerfis = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/perfis/');
            setPerfis(response.data);
        } catch (err) {
            setError('Erro ao buscar perfis.');
            console.error('Erro ao buscar perfis:', err);
        }
    };

    const fetchPermissoes = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/permissoes/');
            setPermissoes(response.data);
        } catch (err) {
            setError('Erro ao buscar permissões.');
            console.error('Erro ao buscar permissões:', err);
        }
    };

    const handleCreatePerfil = async () => {
        try {
            await axios.post('http://127.0.0.1:8000/api/perfis/', { nome: newPerfilName });
            setNewPerfilName('');
            setShowModal(false);
            fetchPerfis();
        } catch (err) {
            setError('Erro ao criar perfil.');
            console.error('Erro ao criar perfil:', err);
        }
    };

    const handleUpdatePerfil = async () => {
        if (!selectedPerfil) return;
        try {
            const updatedPermissoes = permissoes.filter(p => p.isChecked).map(p => p.id);
            await axios.put(`http://127.0.0.1:8000/api/perfis/${selectedPerfil.id}/`, {
                nome: selectedPerfil.nome,
                permissoes: updatedPermissoes,
            });
            setShowModal(false);
            fetchPerfis();
        } catch (err) {
            setError('Erro ao atualizar perfil.');
            console.error('Erro ao atualizar perfil:', err);
        }
    };

    const handleDeletePerfil = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/api/perfis/${id}/`);
            fetchPerfis();
        } catch (err) {
            setError('Erro ao deletar perfil.');
            console.error('Erro ao deletar perfil:', err);
        }
    };

    const openEditModal = (perfil) => {
        setSelectedPerfil({
            ...perfil,
            permissoes: perfil.permissoes.map(p => p.id) // Store only IDs for comparison
        });
        // Initialize checkboxes based on current perfil permissions
        setPermissoes(permissoes.map(p => ({
            ...p,
            isChecked: perfil.permissoes.some(pp => pp.id === p.id)
        })));
        setShowModal(true);
    };

    const handleCheckboxChange = (permissaoId) => {
        setPermissoes(permissoes.map(p => 
            p.id === permissaoId ? { ...p, isChecked: !p.isChecked } : p
        ));
    };

    return (
        <Container>
            <h1 className="my-4">Gerenciamento de Perfis e Permissões</h1>
            {error && <Alert variant="danger">{error}</Alert>}

            <Button variant="primary" onClick={() => { setSelectedPerfil(null); setNewPerfilName(''); setShowModal(true); }}>
                Criar Novo Perfil
            </Button>

            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome do Perfil</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {perfis.map((perfil) => (
                        <tr key={perfil.id}>
                            <td>{perfil.id}</td>
                            <td>{perfil.nome}</td>
                            <td>
                                <Button variant="info" size="sm" className="me-2" onClick={() => openEditModal(perfil)}>
                                    Editar Permissões
                                </Button>
                                <Button variant="danger" size="sm" onClick={() => handleDeletePerfil(perfil.id)}>
                                    Excluir
                                </Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>{selectedPerfil ? `Editar Permissões do Perfil: ${selectedPerfil.nome}` : 'Criar Novo Perfil'}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {!selectedPerfil && (
                        <Form.Group className="mb-3">
                            <Form.Label>Nome do Novo Perfil</Form.Label>
                            <Form.Control
                                type="text"
                                value={newPerfilName}
                                onChange={(e) => setNewPerfilName(e.target.value)}
                            />
                        </Form.Group>
                    )}

                    {selectedPerfil && (
                        <div>
                            <h5>Permissões:</h5>
                            <div className="row">
                                {permissoes.map((permissao) => (
                                    <div key={permissao.id} className="col-md-4">
                                        <Form.Check
                                            type="checkbox"
                                            id={`permissao-${permissao.id}`}
                                            label={permissao.nome}
                                            checked={permissao.isChecked}
                                            onChange={() => handleCheckboxChange(permissao.id)}
                                        />
                                        <small className="text-muted">{permissao.descricao}</small>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Cancelar
                    </Button>
                    {selectedPerfil ? (
                        <Button variant="primary" onClick={handleUpdatePerfil}>
                            Salvar Alterações
                        </Button>
                    ) : (
                        <Button variant="primary" onClick={handleCreatePerfil}>
                            Criar Perfil
                        </Button>
                    )}
                </Modal.Footer>
            </Modal>
        </Container>
    );
};

export default GerenciamentoPerfis;
