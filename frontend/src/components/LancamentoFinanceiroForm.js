import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const LancamentoFinanceiroForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user } = useAuth();

    const [tipo, setTipo] = useState('');
    const [descricao, setDescricao] = useState('');
    const [valor, setValor] = useState('');
    const [dataVencimento, setDataVencimento] = useState('');
    const [dataPagamento, setDataPagamento] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        if (id) {
            axios.get(`http://127.0.0.1:8000/api/lancamentos-financeiros/${id}/`)
                .then(response => {
                    const lancamentoData = response.data;
                    setTipo(lancamentoData.tipo);
                    setDescricao(lancamentoData.descricao);
                    setValor(lancamentoData.valor);
                    setDataVencimento(lancamentoData.data_vencimento);
                    setDataPagamento(lancamentoData.data_pagamento || '');
                })
                .catch(error => {
                    console.error('Error fetching financial entry data: ', error);
                    setError('Lançamento financeiro não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const lancamentoData = {
            tipo,
            descricao,
            valor,
            data_vencimento: dataVencimento,
            data_pagamento: dataPagamento || null, // Envia null se estiver vazio
        };

        try {
            let response;
            if (id) {
                response = await axios.put(`http://127.0.0.1:8000/api/lancamentos-financeiros/${id}/`, lancamentoData);
            } else {
                response = await axios.post('http://127.0.0.1:8000/api/lancamentos-financeiros/', lancamentoData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/lancamentos-financeiros');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o lançamento financeiro.');
            }
            console.error(err);
        }
    };

    const canSaveLancamento = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Lançamento Financeiro' : 'Novo Lançamento Financeiro'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="tipo">
                    <Form.Label>Tipo</Form.Label>
                    <Form.Control as="select" value={tipo} onChange={(e) => setTipo(e.target.value)} required>
                        <option value="">Selecione o Tipo</option>
                        <option value="RECEITA">Receita</option>
                        <option value="DESPESA">Despesa</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="descricao">
                    <Form.Label>Descrição</Form.Label>
                    <Form.Control type="text" value={descricao} onChange={(e) => setDescricao(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="valor">
                    <Form.Label>Valor</Form.Label>
                    <Form.Control type="number" step="0.01" value={valor} onChange={(e) => setValor(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="dataVencimento">
                    <Form.Label>Data de Vencimento</Form.Label>
                    <Form.Control type="date" value={dataVencimento} onChange={(e) => setDataVencimento(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="dataPagamento">
                    <Form.Label>Data de Pagamento (Opcional)</Form.Label>
                    <Form.Control type="date" value={dataPagamento} onChange={(e) => setDataPagamento(e.target.value)} />
                </Form.Group>
                {canSaveLancamento && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Lançamento
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default LancamentoFinanceiroForm;