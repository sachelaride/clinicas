import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const CampanhaMarketingForm = () => {
    const { id } = useParams(); // Obtém o ID da campanha da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [nome, setNome] = useState('');
    const [tipo, setTipo] = useState('');
    const [dataInicio, setDataInicio] = useState('');
    const [dataFim, setDataFim] = useState('');
    const [descricao, setDescricao] = useState('');
    const [error, setError] = useState('');

    const TIPO_CHOICES = [
        { value: 'SMS', label: 'SMS' },
        { value: 'WHATSAPP', label: 'WhatsApp' },
        { value: 'EMAIL', label: 'E-mail Marketing' },
        { value: 'OUTRO', label: 'Outro' },
    ];

    useEffect(() => {
        if (id) {
            // Se houver um ID, busca os dados da campanha para edição
            axios.get(`http://127.0.0.1:8000/api/campanhas-marketing/${id}/`)
                .then(response => {
                    const campanhaData = response.data;
                    setNome(campanhaData.nome);
                    setTipo(campanhaData.tipo);
                    setDataInicio(campanhaData.data_inicio);
                    setDataFim(campanhaData.data_fim || '');
                    setDescricao(campanhaData.descricao);
                })
                .catch(error => {
                    console.error('Error fetching campanha marketing data: ', error);
                    setError('Campanha de Marketing não encontrada.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const campanhaData = {
            nome,
            tipo,
            data_inicio: dataInicio,
            data_fim: dataFim || null,
            descricao,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/campanhas-marketing/${id}/`, campanhaData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/campanhas-marketing/', campanhaData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/campanhas-marketing');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar a campanha de marketing.');
            }
            console.error(err);
        }
    };

    const canSaveCampanha = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Campanha de Marketing' : 'Nova Campanha de Marketing'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="nome">
                    <Form.Label>Nome</Form.Label>
                    <Form.Control type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="tipo">
                    <Form.Label>Tipo</Form.Label>
                    <Form.Control as="select" value={tipo} onChange={(e) => setTipo(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {TIPO_CHOICES.map(choice => (
                            <option key={choice.value} value={choice.value}>{choice.label}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="dataInicio">
                    <Form.Label>Data de Início</Form.Label>
                    <Form.Control type="date" value={dataInicio} onChange={(e) => setDataInicio(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="dataFim">
                    <Form.Label>Data de Fim (opcional)</Form.Label>
                    <Form.Control type="date" value={dataFim} onChange={(e) => setDataFim(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="descricao">
                    <Form.Label>Descrição</Form.Label>
                    <Form.Control as="textarea" value={descricao} onChange={(e) => setDescricao(e.target.value)} />
                </Form.Group>
                {canSaveCampanha && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Campanha
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default CampanhaMarketingForm;
