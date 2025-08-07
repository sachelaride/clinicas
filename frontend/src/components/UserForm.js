import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const UserForm = () => {
    const { id } = useParams(); // Obtém o ID do usuário da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth(); // Get the current user from AuthContext

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [perfilId, setPerfilId] = useState('');
    const [availableProfiles, setAvailableProfiles] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProfiles = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/perfis/');
                setAvailableProfiles(response.data);
            } catch (err) {
                console.error('Error fetching profiles:', err);
                setError('Erro ao carregar perfis.');
            }
        };
        fetchProfiles();

        if (id) {
            // Se houver um ID, busca os dados do usuário para edição
            axios.get(`http://127.0.0.1:8000/api/users/${id}/`)
                .then(response => {
                    const userData = response.data;
                    setUsername(userData.username);
                    setEmail(userData.email);
                    setPerfilId(userData.perfil.id); // Set perfilId from fetched user data
                })
                .catch(error => {
                    console.error('Error fetching user data: ', error);
                    setError('Usuário não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const userData = {
            username,
            email,
            perfil_id: perfilId,
        };

        if (password) {
            userData.password = password;
        }

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/users/${id}/`, userData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/users/', userData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/users');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o usuário.');
            }
            console.error(err);
        }
    };

    const canSaveUser = user && user.perfil && (user.perfil.nome === 'ADMIN' || user.perfil.nome === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Usuário' : 'Novo Usuário'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label>Nome de Usuário</Form.Label>
                    <Form.Control type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="password">
                    <Form.Label>Senha {id && '(deixe em branco para não alterar)'}</Form.Label>
                    <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="perfil">
                    <Form.Label>Perfil</Form.Label>
                    <Form.Control as="select" value={perfilId} onChange={(e) => setPerfilId(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {availableProfiles.map(profile => (
                            <option key={profile.id} value={profile.id}>{profile.nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                {canSaveUser && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Usuário
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default UserForm;
