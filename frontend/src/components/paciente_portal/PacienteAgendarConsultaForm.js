import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PacienteAgendarConsultaForm = () => {
    const navigate = useNavigate();
    const { user } = useAuth();

    const [profissional, setProfissional] = useState('');
    const [data, setData] = useState('');
    const [guicheNumero, setGuicheNumero] = useState('');
    const [error, setError] = useState('');
    const [profissionais, setProfissionais] = useState([]);

    useEffect(() => {
        if (user && user.perfil === 'PACIENTE') {
            // Busca profissionais para o select
            axios.get('/api/users/') // Assumindo que /api/users/ retorna todos os usuários
                .then(response => {
                    setProfissionais(response.data.filter(user => user.perfil === 'PROFISSIONAL'));
                })
                .catch(error => {
                    console.error('Error fetching professionals: ', error);
                    setError('Erro ao carregar profissionais.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const agendamentoData = {
            profissional,
            data,
            guiche_numero: guicheNumero,
            status: 'AGENDADO', // Status padrão para novo agendamento
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/paciente/agendar-consulta/', agendamentoData);
            if (response.data.success) {
                navigate('/portal-paciente/agendamentos');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao agendar a consulta.');
            }
            console.error(err);
        }
    };

    return (
        <Container>
            <h1 className="my-4">Agendar Nova Consulta</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            {user && user.perfil === 'PACIENTE' ? (
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3" controlId="profissional">
                        <Form.Label>Profissional</Form.Label>
                        <Form.Control as="select" value={profissional} onChange={(e) => setProfissional(e.target.value)} required>
                            <option value="">Selecione...</option>
                            {profissionais.map(prof => (
                                <option key={prof.id} value={prof.id}>{prof.username}</option>
                            ))}
                        </Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="data">
                        <Form.Label>Data e Hora</Form.Label>
                        <Form.Control type="datetime-local" value={data} onChange={(e) => setData(e.target.value)} required />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="guicheNumero">
                        <Form.Label>Número do Guichê</Form.Label>
                        <Form.Control type="number" value={guicheNumero} onChange={(e) => setGuicheNumero(e.target.value)} />
                    </Form.Group>
                    <Button variant="primary" type="submit" className="mt-3">
                        Agendar Consulta
                    </Button>
                </Form>
            ) : (
                <Alert variant="warning">Acesso restrito a pacientes.</Alert>
            )}
        </Container>
    );
};

export default PacienteAgendarConsultaForm;