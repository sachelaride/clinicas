import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const LeadForm = () => {
    const { id } = useParams(); // Obtém o ID do lead da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [nome, setNome] = useState('');
    const [email, setEmail] = useState('');
    const [telefone, setTelefone] = useState('');
    const [origem, setOrigem] = useState('');
    const [status, setStatus] = useState('');
    const [error, setError] = useState('');

    const STATUS_CHOICES = [
        { value: 'NOVO', label: 'Novo' },
        { value: 'CONTATO', label: 'Em Contato' },
        { value: 'QUALIFICADO', label: 'Qualificado' },
        { value: 'CONVERTIDO', label: 'Convertido' },
        { value: 'PERDIDO', label: 'Perdido' },
    ];

    useEffect(() => {
        if (id) {
            // Se houver um ID, busca os dados do lead para edição
            axios.get(`http://127.0.0.1:8000/api/leads/${id}/`)
                .then(response => {
                    const leadData = response.data;
                    setNome(leadData.nome);
                    setEmail(leadData.email);
                    setTelefone(leadData.telefone);
                    setOrigem(leadData.origem);
                    setStatus(leadData.status);
                })
                .catch(error => {
                    console.error('Error fetching lead data: ', error);
                    setError('Lead não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const leadData = {
            nome,
            email,
            telefone,
            origem,
            status,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/leads/${id}/`, leadData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/leads/', leadData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/crm');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o lead.');
            }
            console.error(err);
        }
    };

    const canSaveLead = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Lead' : 'Novo Lead'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="nome">
                    <Form.Label>Nome</Form.Label>
                    <Form.Control type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="telefone">
                    <Form.Label>Telefone</Form.Label>
                    <Form.Control type="text" value={telefone} onChange={(e) => setTelefone(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="origem">
                    <Form.Label>Origem</Form.Label>
                    <Form.Control type="text" value={origem} onChange={(e) => setOrigem(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="status">
                    <Form.Label>Status</Form.Label>
                    <Form.Control as="select" value={status} onChange={(e) => setStatus(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {STATUS_CHOICES.map(choice => (
                            <option key={choice.value} value={choice.value}>{choice.label}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                {canSaveLead && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Lead
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default LeadForm;
