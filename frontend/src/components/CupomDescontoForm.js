import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const CupomDescontoForm = () => {
    const { id } = useParams(); // Obtém o ID do cupom da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [codigo, setCodigo] = useState('');
    const [valorDesconto, setValorDesconto] = useState('');
    const [dataValidade, setDataValidade] = useState('');
    const [ativo, setAtivo] = useState(true);
    const [campanha, setCampanha] = useState('');
    const [error, setError] = useState('');
    const [campanhas, setCampanhas] = useState([]);

    useEffect(() => {
        // Busca campanhas para o select
        axios.get('/api/campanhas-marketing/')
            .then(response => {
                setCampanhas(response.data);
            })
            .catch(error => {
                console.error('Error fetching campanhas: ', error);
            });

        if (id) {
            // Se houver um ID, busca os dados do cupom para edição
            axios.get(`http://127.0.0.1:8000/api/cupons-desconto/${id}/`)
                .then(response => {
                    const cupomData = response.data;
                    setCodigo(cupomData.codigo);
                    setValorDesconto(cupomData.valor_desconto);
                    setDataValidade(cupomData.data_validade);
                    setAtivo(cupomData.ativo);
                    setCampanha(cupomData.campanha || '');
                })
                .catch(error => {
                    console.error('Error fetching cupom desconto data: ', error);
                    setError('Cupom de Desconto não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const cupomData = {
            codigo,
            valor_desconto: valorDesconto,
            data_validade: dataValidade,
            ativo,
            campanha: campanha || null,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/cupons-desconto/${id}/`, cupomData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/cupons-desconto/', cupomData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/cupons-desconto');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o cupom de desconto.');
            }
            console.error(err);
        }
    };

    const canSaveCupom = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Cupom de Desconto' : 'Novo Cupom de Desconto'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="codigo">
                    <Form.Label>Código</Form.Label>
                    <Form.Control type="text" value={codigo} onChange={(e) => setCodigo(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="valorDesconto">
                    <Form.Label>Valor de Desconto</Form.Label>
                    <Form.Control type="number" step="0.01" value={valorDesconto} onChange={(e) => setValorDesconto(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="dataValidade">
                    <Form.Label>Data de Validade</Form.Label>
                    <Form.Control type="date" value={dataValidade} onChange={(e) => setDataValidade(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="ativo">
                    <Form.Check type="checkbox" label="Ativo" checked={ativo} onChange={(e) => setAtivo(e.target.checked)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="campanha">
                    <Form.Label>Campanha (opcional)</Form.Label>
                    <Form.Control as="select" value={campanha} onChange={(e) => setCampanha(e.target.value)}>
                        <option value="">Nenhuma</option>
                        {campanhas.map(camp => (
                            <option key={camp.id} value={camp.id}>{camp.nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                {canSaveCupom && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Cupom
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default CupomDescontoForm;
