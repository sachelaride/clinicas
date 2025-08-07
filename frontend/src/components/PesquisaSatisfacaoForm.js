import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const PesquisaSatisfacaoForm = () => {
    const { id } = useParams(); // Obtém o ID da pesquisa da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [paciente, setPaciente] = useState('');
    const [notaNps, setNotaNps] = useState('');
    const [comentarios, setComentarios] = useState('');
    const [error, setError] = useState('');
    const [pacientes, setPacientes] = useState([]);

    const NOTA_NPS_CHOICES = Array.from({ length: 11 }, (_, i) => ({ value: i, label: i.toString() }));

    useEffect(() => {
        // Busca pacientes para o select
        axios.get('/api/pacientes/')
            .then(response => {
                setPacientes(response.data);
            })
            .catch(error => {
                console.error('Error fetching patients: ', error);
            });

        if (id) {
            // Se houver um ID, busca os dados da pesquisa para edição
            axios.get(`http://127.0.0.1:8000/api/pesquisas-satisfacao/${id}/`)
                .then(response => {
                    const pesquisaData = response.data;
                    setPaciente(pesquisaData.paciente);
                    setNotaNps(pesquisaData.nota_nps);
                    setComentarios(pesquisaData.comentarios);
                })
                .catch(error => {
                    console.error('Error fetching pesquisa satisfacao data: ', error);
                    setError('Pesquisa de Satisfação não encontrada.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const pesquisaData = {
            paciente,
            nota_nps: notaNps,
            comentarios,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/pesquisas-satisfacao/${id}/`, pesquisaData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/pesquisas-satisfacao/', pesquisaData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/pesquisas-satisfacao');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar a pesquisa de satisfação.');
            }
            console.error(err);
        }
    };

    const canSavePesquisa = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Pesquisa de Satisfação' : 'Nova Pesquisa de Satisfação'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="paciente">
                    <Form.Label>Paciente</Form.Label>
                    <Form.Control as="select" value={paciente} onChange={(e) => setPaciente(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {pacientes.map(pac => (
                            <option key={pac.id} value={pac.id}>{pac.nome}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="notaNps">
                    <Form.Label>Nota NPS</Form.Label>
                    <Form.Control as="select" value={notaNps} onChange={(e) => setNotaNps(e.target.value)} required>
                        <option value="">Selecione...</option>
                        {NOTA_NPS_CHOICES.map(choice => (
                            <option key={choice.value} value={choice.value}>{choice.label}</option>
                        ))}
                    </Form.Control>
                </Form.Group>
                <Form.Group className="mb-3" controlId="comentarios">
                    <Form.Label>Comentários</Form.Label>
                    <Form.Control as="textarea" value={comentarios} onChange={(e) => setComentarios(e.target.value)} />
                </Form.Group>
                {canSavePesquisa && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Pesquisa
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default PesquisaSatisfacaoForm;
