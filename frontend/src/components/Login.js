import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Form, Button, Container, Alert } from 'react-bootstrap';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [clinicas, setClinicas] = useState([]);
    const [selectedClinica, setSelectedClinica] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { setUser } = useAuth();

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/clinicas-public/')
            .then(response => {
                setClinicas(response.data);
                if (response.data.length > 0) {
                    setSelectedClinica(response.data[0].id); // Select first clinic by default
                }
            })
            .catch(err => {
                console.error('Error fetching clinics:', err);
                setError('Erro ao carregar clínicas.');
            });
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/token', { username, password, clinic_id: selectedClinica });
            console.log("Token response:", response.data);
            const { access_token, token_type } = response.data;

            localStorage.setItem('access_token', access_token);
            localStorage.setItem('token_type', token_type);

            axios.defaults.headers.common['Authorization'] = `${token_type} ${access_token}`;

            // Fetch user data after successful login
            const userResponse = await axios.get('http://127.0.0.1:8000/api/users/me');
            console.log("User data after login:", userResponse.data);
            setUser(userResponse.data);
            navigate('/');
        } catch (err) {
            setError('Ocorreu um erro ao tentar fazer login.');
        }
    };

    return (
        <Container>
            <h1 className="my-4">Login</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="username">
                    <Form.Label>Usuário</Form.Label>
                    <Form.Control
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </Form.Group>
                <Form.Group controlId="password">
                    <Form.Label>Senha</Form.Label>
                    <Form.Control
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </Form.Group>
                <Form.Group controlId="clinicSelect" className="mb-3">
                    <Form.Label>Selecionar Clínica</Form.Label>
                    <Form.Control as="select" value={selectedClinica} onChange={e => setSelectedClinica(e.target.value)} required>
                        {clinicas.map(clinica => (
                            <option key={clinica.id} value={clinica.id}>
                                {clinica.nome}
                            </option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Button variant="primary" type="submit" className="mt-3">
                    Entrar
                </Button>
            </Form>
        </Container>
    );
};

export default Login;
