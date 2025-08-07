import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const FaturaForm = () => {
    const { id } = useParams(); // Obtém o ID da fatura da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [convenio, setConvenio] = useState('');
    const [mesReferencia, setMesReferencia] = useState('');
    const [valorTotal, setValorTotal] = useState('');
    const [status, setStatus] = useState('');
    const [error, setError] = useState('');
    const [convenios, setConvenios] = useState([]);

    const STATUS_CHOICES = [
        { value: 'ABERTA', label: 'Aberta' },
        { value: 'FECHADA', label: 'Fechada' },
        { value: 'PAGA', label: 'Paga' },
        { value: 'GLOSADA', label: 'Glosada' },
    ];

    useEffect(() => {
        // Busca convênios
        axios.get('/api/convenios/') // Você precisará criar esta API no Django
            .then(response => {
                setConvenios(response.data);
            })
            .catch(error => {
                console.error('Error fetching convenios: ', error);
            });

        if (id) {
            // Se houver um ID, busca os dados da fatura para edição
            axios.get(`http://127.0.0.1:8000/api/faturas/${id}/`)
                .then(response => {
                    const faturaData = response.data;
                    setConvenio(faturaData.convenio);
                    setMesReferencia(faturaData.mes_referencia);
                    setValorTotal(faturaData.valor_total);
                    setStatus(faturaData.status);
                })
                .catch(error => {
                    console.error('Error fetching fatura data: ', error);
                    setError('Fatura não encontrada.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const faturaData = {
            convenio,
            mes_referencia: mesReferencia,
            valor_total: valorTotal,
            status,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/faturas/${id}/`, faturaData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/faturas/', faturaData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/faturas');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar a fatura.');
            }
            console.error(err);
        }
    };

    const canSaveFatura = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Fatura' : 'Nova Fatura'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="convenio">
                    <Form.Label>Convênio</Form.Label>
                    <Form.Control as="select" value={convenio} onChange={(e) => setConvenio(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {convenios.map(conv => (
                            <option key={conv.id} value={conv.id}>{conv.nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="mesReferencia">
                    <Form.Label>Mês de Referência</Form.Label>
                    <Form.Control type="date" value={mesReferencia} onChange={(e) => setMesReferencia(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="valorTotal">
                    <Form.Label>Valor Total</Form.Label>
                    <Form.Control type="number" step="0.01" value={valorTotal} onChange={(e) => setValorTotal(e.target.value)} required />
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
                {canSaveFatura && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Fatura
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default FaturaForm;
