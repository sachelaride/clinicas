import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const ProntuarioForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user } = useAuth();

    const [pacientes, setPacientes] = useState([]);
    const [selectedPaciente, setSelectedPaciente] = useState('');
    const [tipoTratamentoDefinido, setTipoTratamentoDefinido] = useState('');
    const [queixaPrincipal, setQueixaPrincipal] = useState('');
    const [isFinalized, setIsFinalized] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        // Fetch pacientes for dropdown
        axios.get('/api/pacientes/')
            .then(response => {
                setPacientes(response.data);
            })
            .catch(error => {
                console.error('Error fetching patients: ', error);
                setError('Erro ao carregar pacientes.');
            });

        if (id) {
            // Fetch prontuario data for editing
            axios.get(`http://127.0.0.1:8000/api/prontuarios/${id}/`)
                .then(response => {
                    const prontuarioData = response.data;
                    setSelectedPaciente(prontuarioData.paciente);
                    setTipoTratamentoDefinido(prontuarioData.tipo_tratamento_definido || '');
                    setQueixaPrincipal(prontuarioData.queixa_principal);
                    setIsFinalized(prontuarioData.is_finalized);
                })
                .catch(error => {
                    console.error('Error fetching prontuario data: ', error);
                    setError('Prontuário não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const prontuarioData = {
            paciente: selectedPaciente,
            tipo_tratamento_definido: tipoTratamentoDefinido || null,
            queixa_principal: queixaPrincipal,
            is_finalized: isFinalized,
        };

        try {
            let response;
            if (id) {
                response = await axios.put(`http://127.0.0.1:8000/api/prontuarios/${id}/`, prontuarioData);
            } else {
                response = await axios.post('http://127.0.0.1:8000/api/prontuarios/', prontuarioData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/prontuarios');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o prontuário.');
            }
            console.error(err);
        }
    };

    const canSaveProntuario = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR' || user.perfil === 'PROFISSIONAL');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Prontuário' : 'Novo Prontuário'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="paciente">
                    <Form.Label>Paciente</Form.Label>
                    <Form.Control as="select" value={selectedPaciente} onChange={(e) => setSelectedPaciente(e.target.value)} required>
                        <option value="">Selecione um Paciente</option>
                        {pacientes.map(paciente => (
                            <option key={paciente.id} value={paciente.id}>
                                {paciente.nome}
                            </option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group className="mb-3" controlId="tipoTratamentoDefinido">
                    <Form.Label>Tipo de Tratamento Definido (Opcional)</Form.Label>
                    <Form.Control type="text" value={tipoTratamentoDefinido} onChange={(e) => setTipoTratamentoDefinido(e.target.value)} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="queixaPrincipal">
                    <Form.Label>Queixa Principal</Form.Label>
                    <Form.Control as="textarea" rows={3} value={queixaPrincipal} onChange={(e) => setQueixaPrincipal(e.target.value)} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="isFinalized">
                    <Form.Check
                        type="checkbox"
                        label="Finalizado"
                        checked={isFinalized}
                        onChange={(e) => setIsFinalized(e.target.checked)}
                    />
                </Form.Group>

                {canSaveProntuario && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Prontuário
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default ProntuarioForm;
