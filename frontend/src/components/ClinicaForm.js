import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const ClinicaForm = () => {
    const { id } = useParams(); // Obtém o ID da clínica da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [nome, setNome] = useState('');
    const [endereco, setEndereco] = useState('');
    const [telefone, setTelefone] = useState('');
    const [numGuiches, setNumGuiches] = useState('');
    const [tempoMinimoAtendimento, setTempoMinimoAtendimento] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        if (id) {
            // Se houver um ID, busca os dados da clínica para edição
            axios.get(`http://127.0.0.1:8000/api/clinicas/${id}/`)
                .then(response => {
                    const clinicaData = response.data;
                    setNome(clinicaData.nome);
                    setEndereco(clinicaData.endereco);
                    setTelefone(clinicaData.telefone);
                    setNumGuiches(clinicaData.num_guiches);
                    setTempoMinimoAtendimento(clinicaData.tempo_minimo_atendimento);
                })
                .catch(error => {
                    console.error('Error fetching clinica data: ', error);
                    setError('Clínica não encontrada.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const clinicaData = {
            nome,
            endereco,
            telefone,
            num_guiches: numGuiches,
            tempo_minimo_atendimento: tempoMinimoAtendimento,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/clinicas/${id}/`, clinicaData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/clinicas/', clinicaData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/clinicas');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar a clínica.');
            }
            console.error(err);
        }
    };

    const canSaveClinica = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Clínica' : 'Nova Clínica'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="nome">
                    <Form.Label>Nome</Form.Label>
                    <Form.Control type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="endereco">
                    <Form.Label>Endereço</Form.Label>
                    <Form.Control as="textarea" value={endereco} onChange={(e) => setEndereco(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="telefone">
                    <Form.Label>Telefone</Form.Label>
                    <Form.Control type="text" value={telefone} onChange={(e) => setTelefone(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="numGuiches">
                    <Form.Label>Número de Guichês</Form.Label>
                    <Form.Control type="number" value={numGuiches} onChange={(e) => setNumGuiches(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="tempoMinimoAtendimento">
                    <Form.Label>Tempo Mínimo de Atendimento (minutos)</Form.Label>
                    <Form.Control type="number" value={tempoMinimoAtendimento} onChange={(e) => setTempoMinimoAtendimento(e.target.value)} required />
                </Form.Group>
                {canSaveClinica && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Clínica
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default ClinicaForm;