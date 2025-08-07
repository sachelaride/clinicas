import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Form, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AtendimentoForm = () => {
    const [atendimento, setAtendimento] = useState({
        agendamento: '',
        observacoes: '',
        data_fim: '',
        status: 'INICIADO',
        tipo_tratamento_realizado: '',
        prontuario: ''
    });
    const [agendamentos, setAgendamentos] = useState([]);
    const [tiposTratamento, setTiposTratamento] = useState([]);
    const [prontuarios, setProntuarios] = useState([]); // Para o campo prontuario
    const navigate = useNavigate();
    const { id } = useParams();
    const { user } = useAuth();

    useEffect(() => {
        axios.get('/api/agendamentos/')
            .then(response => setAgendamentos(response.data))
            .catch(error => console.error('Error fetching agendamentos:', error));

        axios.get('/api/tipos-tratamento/') // Assumindo que você terá uma API para tipos de tratamento
            .then(response => setTiposTratamento(response.data))
            .catch(error => console.error('Error fetching tipos de tratamento:', error));

        axios.get('/api/prontuarios/') // Assumindo que você terá uma API para prontuarios
            .then(response => setProntuarios(response.data))
            .catch(error => console.error('Error fetching prontuarios:', error));

        if (id) {
            axios.get(`http://127.0.0.1:8000/api/atendimentos/${id}/`)
                .then(response => {
                    setAtendimento({
                        ...response.data,
                        data_fim: response.data.data_fim ? response.data.data_fim.substring(0, 16) : '' // Formata para datetime-local
                    });
                })
                .catch(error => console.error('Error fetching atendimento:', error));
        }
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAtendimento(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const method = id ? 'put' : 'post';
        const url = id ? `http://127.0.0.1:8000/api/atendimentos/${id}/` : 'http://127.0.0.1:8000/api/atendimentos/';

        axios[method](url, atendimento)
            .then(() => {
                navigate('/atendimentos');
            })
            .catch(error => {
                console.error('Error saving atendimento:', error.response ? error.response.data : error);
            });
    };

    const canSaveAtendimento = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR' || user.perfil === 'ATENDENTE');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar' : 'Novo'} Atendimento</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="agendamento">
                    <Form.Label>Agendamento</Form.Label>
                    <Form.Control as="select" name="agendamento" value={atendimento.agendamento} onChange={handleChange} required>
                        <option value="">Selecione um agendamento</option>
                        {agendamentos.map(agendamento => (
                            <option key={agendamento.id} value={agendamento.id}>Agendamento de {agendamento.paciente_nome} em {new Date(agendamento.data).toLocaleString()}</option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="tipo_tratamento_realizado">
                    <Form.Label>Tipo de Tratamento Realizado</Form.Label>
                    <Form.Control as="select" name="tipo_tratamento_realizado" value={atendimento.tipo_tratamento_realizado} onChange={handleChange}>
                        <option value="">Selecione um tipo de tratamento</option>
                        {tiposTratamento.map(tipo => (
                            <option key={tipo.id} value={tipo.id}>{tipo.nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="prontuario">
                    <Form.Label>Prontuário</Form.Label>
                    <Form.Control as="select" name="prontuario" value={atendimento.prontuario} onChange={handleChange}>
                        <option value="">Selecione um prontuário</option>
                        {prontuarios.map(prontuario => (
                            <option key={prontuario.id} value={prontuario.id}>Prontuário {prontuario.id} - {prontuario.paciente_nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="observacoes">
                    <Form.Label>Observações</Form.Label>
                    <Form.Control as="textarea" name="observacoes" value={atendimento.observacoes} onChange={handleChange} />
                </Form.Group>

                <Form.Group controlId="data_fim">
                    <Form.Label>Data Fim</Form.Label>
                    <Form.Control type="datetime-local" name="data_fim" value={atendimento.data_fim} onChange={handleChange} />
                </Form.Group>

                <Form.Group controlId="status">
                    <Form.Label>Status</Form.Label>
                    <Form.Control as="select" name="status" value={atendimento.status} onChange={handleChange} required>
                        <option value="INICIADO">Iniciado</option>
                        <option value="FINALIZADO">Finalizado</option>
                    </Form.Control>
                </Form.Group>

                {canSaveAtendimento && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default AtendimentoForm;