import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Form, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AgendamentoForm = () => {
    const [agendamento, setAgendamento] = useState({
        paciente: '',
        profissional: '',
        data: '',
        status: 'AGENDADO'
    });
    const [pacientes, setPacientes] = useState([]);
    const [profissionais, setProfissionais] = useState([]);
    const navigate = useNavigate();
    const { id } = useParams();
    const { user } = useAuth();

    useEffect(() => {
        axios.get('/api/pacientes/')
            .then(response => setPacientes(response.data))
            .catch(error => console.error('Error fetching pacientes:', error));

        axios.get('/api/profissionais/')
            .then(response => setProfissionais(response.data))
            .catch(error => console.error('Error fetching profissionais:', error));

        if (id) {
            axios.get(`http://127.0.0.1:8000/api/agendamentos/${id}/`)
                .then(response => {
                    setAgendamento({
                        ...response.data,
                        data: response.data.data.substring(0, 16) // Formata para datetime-local
                    });
                })
                .catch(error => console.error('Error fetching agendamento:', error));
        }
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAgendamento(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const method = id ? 'put' : 'post';
        const url = id ? `http://127.0.0.1:8000/api/agendamentos/${id}/` : 'http://127.0.0.1:8000/api/agendamentos/';

        axios[method](url, agendamento)
            .then(() => {
                navigate('/agendamentos');
            })
            .catch(error => {
                console.error('Error saving agendamento:', error.response ? error.response.data : error);
            });
    };

    const canSaveAgendamento = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR' || user.perfil === 'ATENDENTE');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar' : 'Novo'} Agendamento</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="paciente">
                    <Form.Label>Paciente</Form.Label>
                    <Form.Control as="select" name="paciente" value={agendamento.paciente} onChange={handleChange} required>
                        <option value="">Selecione um paciente</option>
                        {pacientes.map(paciente => (
                            <option key={paciente.id} value={paciente.id}>{paciente.nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="profissional">
                    <Form.Label>Profissional</Form.Label>
                    <Form.Control as="select" name="profissional" value={agendamento.profissional} onChange={handleChange} required>
                        <option value="">Selecione um profissional</option>
                        {profissionais.map(profissional => (
                            <option key={profissional.id} value={profissional.id}>{profissional.user.username}</option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="data">
                    <Form.Label>Data e Hora</Form.Label>
                    <Form.Control type="datetime-local" name="data" value={agendamento.data} onChange={handleChange} required />
                </Form.Group>

                <Form.Group controlId="status">
                    <Form.Label>Status</Form.Label>
                    <Form.Control as="select" name="status" value={agendamento.status} onChange={handleChange} required>
                        <option value="AGENDADO">Agendado</option>
                        <option value="CONCLUIDO">Concluído</option>
                        <option value="CANCELADO">Cancelado</option>
                    </Form.Control>
                </Form.Group>

                {canSaveAgendamento && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default AgendamentoForm;