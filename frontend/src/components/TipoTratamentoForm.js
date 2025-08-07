import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const TipoTratamentoForm = () => {
    const { id } = useParams(); // Obtém o ID do tipo de tratamento da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [nome, setNome] = useState('');
    const [descricao, setDescricao] = useState('');
    const [tempoMinimoAtendimento, setTempoMinimoAtendimento] = useState('');
    const [clinicas, setClinicas] = useState([]);
    const [selectedClinica, setSelectedClinica] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        // Fetch clinics for dropdown
        axios.get('/api/clinicas/')
            .then(response => {
                setClinicas(response.data);
            })
            .catch(error => {
                console.error('Error fetching clinics: ', error);
                setError('Erro ao carregar clínicas.');
            });

        if (id) {
            // Se houver um ID, busca os dados do tipo de tratamento para edição
            axios.get(`http://127.0.0.1:8000/api/tipos-tratamento/${id}/`)
                .then(response => {
                    const tipoData = response.data;
                    setNome(tipoData.nome);
                    setDescricao(tipoData.descricao);
                    setTempoMinimoAtendimento(tipoData.tempo_minimo_atendimento);
                    setSelectedClinica(tipoData.clinica); // Assume que o backend retorna o ID da clínica
                })
                .catch(error => {
                    console.error('Error fetching tipo de tratamento data: ', error);
                    setError('Tipo de Tratamento não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const tipoData = {
            nome,
            descricao,
            tempo_minimo_atendimento: tempoMinimoAtendimento,
            clinica: selectedClinica, // Adiciona o ID da clínica
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/tipos-tratamento/${id}/`, tipoData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/tipos-tratamento/', tipoData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/tipos-tratamento');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o tipo de tratamento.');
            }
            console.error(err);
        }
    };

    const canSaveTipoTratamento = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Tipo de Tratamento' : 'Novo Tipo de Tratamento'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="clinica">
                    <Form.Label>Clínica</Form.Label>
                    <Form.Control as="select" value={selectedClinica} onChange={(e) => setSelectedClinica(e.target.value)} required>
                        <option value="">Selecione uma Clínica</option>
                        {clinicas.map(clinica => (
                            <option key={clinica.id} value={clinica.id}>
                                {clinica.nome}
                            </option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="nome">
                    <Form.Label>Nome</Form.Label>
                    <Form.Control type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="descricao">
                    <Form.Label>Descrição</Form.Label>
                    <Form.Control as="textarea" value={descricao} onChange={(e) => setDescricao(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="tempoMinimoAtendimento">
                    <Form.Label>Tempo Mínimo de Atendimento (minutos)</Form.Label>
                    <Form.Control type="number" value={tempoMinimoAtendimento} onChange={(e) => setTempoMinimoAtendimento(e.target.value)} required />
                </Form.Group>
                {canSaveTipoTratamento && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Tipo de Tratamento
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default TipoTratamentoForm;
