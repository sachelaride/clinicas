import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const ComissaoForm = () => {
    const { id } = useParams(); // Obtém o ID da comissão da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [profissional, setProfissional] = useState('');
    const [atendimento, setAtendimento] = useState('');
    const [valor, setValor] = useState('');
    const [paga, setPaga] = useState(false);
    const [error, setError] = useState('');
    const [profissionais, setProfissionais] = useState([]);
    const [atendimentos, setAtendimentos] = useState([]);

    useEffect(() => {
        // Busca profissionais
        axios.get('/api/users/') // Assumindo que /api/users/ retorna todos os usuários, incluindo profissionais
            .then(response => {
                setProfissionais(response.data.filter(user => user.perfil === 'PROFISSIONAL'));
            })
            .catch(error => {
                console.error('Error fetching professionals: ', error);
            });

        // Busca atendimentos
        axios.get('/api/atendimentos/')
            .then(response => {
                setAtendimentos(response.data);
            })
            .catch(error => {
                console.error('Error fetching atendimentos: ', error);
            });

        if (id) {
            // Se houver um ID, busca os dados da comissão para edição
            axios.get(`http://127.0.0.1:8000/api/comissoes/${id}/`)
                .then(response => {
                    const comissaoData = response.data;
                    setProfissional(comissaoData.profissional);
                    setAtendimento(comissaoData.atendimento);
                    setValor(comissaoData.valor);
                    setPaga(comissaoData.paga);
                })
                .catch(error => {
                    console.error('Error fetching comissao data: ', error);
                    setError('Comissão não encontrada.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const comissaoData = {
            profissional,
            atendimento,
            valor,
            paga,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/comissoes/${id}/`, comissaoData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/comissoes/', comissaoData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/comissoes');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar a comissão.');
            }
            console.error(err);
        }
    };

    const canSaveComissao = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Comissão' : 'Nova Comissão'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
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
                <Form.Group className="mb-3" controlId="atendimento">
                    <Form.Label>Atendimento</Form.Label>
                    <Form.Control as="select" value={atendimento} onChange={(e) => setAtendimento(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {atendimentos.map(atend => (
                            <option key={atend.id} value={atend.id}>{atend.paciente} - {new Date(atend.data_inicio).toLocaleString()}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="valor">
                    <Form.Label>Valor</Form.Label>
                    <Form.Control type="number" step="0.01" value={valor} onChange={(e) => setValor(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="paga">
                    <Form.Check type="checkbox" label="Paga" checked={paga} onChange={(e) => setPaga(e.target.checked)} />
                </Form.Group>
                {canSaveComissao && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Comissão
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default ComissaoForm;