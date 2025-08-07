import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const navigate = useNavigate();
    const { user } = useAuth(); // Get the current user from AuthContext

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = () => {
        axios.get('/api/users/')
            .then(response => {
                setUsers(response.data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    };

    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:8000/api/users/${selectedUser.id}/`)
            .then(() => {
                fetchUsers();
                setShowDeleteModal(false);
            })
            .catch(error => {
                console.error('Error deleting data: ', error);
            });
    };

    const openDeleteModal = (user) => {
        setSelectedUser(user);
        setShowDeleteModal(true);
    };

    const filteredUsers = users.filter(user =>
        user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.perfil.nome.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const canManageUsers = user && user.perfil && (user.perfil.nome === 'ADMIN' || user.perfil.nome === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">Lista de Usuários</h1>
            {canManageUsers && (
                <Button variant="success" className="mb-3" onClick={() => navigate('/users/new')}>Novo Usuário</Button>
            )}
            <Form.Group controlId="search">
                <Form.Control
                    type="text"
                    placeholder="Buscar por nome de usuário ou perfil..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </Form.Group>
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Nome de Usuário</th>
                        <th>Email</th>
                        <th>Perfil</th>
                        {canManageUsers && <th>Ações</th>}
                    </tr>
                </thead>
                <tbody>
                    {filteredUsers.map(user => (
                        <tr key={user.id}>
                            <td>{user.username}</td>
                            <td>{user.email}</td>
                            <td>{user.perfil.nome}</td>
                            {canManageUsers && (
                                <td>
                                    <Button variant="primary" size="sm" className="mr-2" onClick={() => navigate(`/users/${user.id}/edit`)}>Editar</Button>
                                    <Button variant="danger" size="sm" onClick={() => openDeleteModal(user)}>Excluir</Button>
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
                    Tem certeza que deseja excluir o usuário <strong>{selectedUser?.username}</strong>?
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

export default UserList;
