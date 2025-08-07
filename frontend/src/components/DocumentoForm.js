import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const DocumentoForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user } = useAuth();

    const [pastas, setPastas] = useState([]);
    const [pacientes, setPacientes] = useState([]);
    const [selectedPasta, setSelectedPasta] = useState('');
    const [selectedPaciente, setSelectedPaciente] = useState('');
    const [arquivo, setArquivo] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        // Fetch pastas for dropdown
        axios.get('/api/pastas-documento/') // Assumindo que você terá uma API para pastas de documento
            .then(response => {
                setPastas(response.data);
            })
            .catch(error => {
                console.error('Error fetching document folders: ', error);
                setError('Erro ao carregar pastas de documento.');
            });

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
            // Fetch documento data for editing
            axios.get(`http://127.0.0.1:8000/api/documentos/${id}/`)
                .then(response => {
                    const documentoData = response.data;
                    setSelectedPasta(documentoData.pasta);
                    setSelectedPaciente(documentoData.paciente);
                    // Não preenche o campo de arquivo para edição por segurança
                })
                .catch(error => {
                    console.error('Error fetching documento data: ', error);
                    setError('Documento não encontrado.');
                });
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('pasta', selectedPasta);
        formData.append('paciente', selectedPaciente);
        if (arquivo) {
            formData.append('arquivo', arquivo);
        }

        try {
            let response;
            if (id) {
                response = await axios.put(`http://127.0.0.1:8000/api/documentos/${id}/`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
            } else {
                response = await axios.post('http://127.0.0.1:8000/api/documentos/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/documentos');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o documento.');
            }
            console.error(err);
        }
    };

    const canSaveDocumento = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Documento' : 'Novo Documento'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="pasta">
                    <Form.Label>Pasta</Form.Label>
                    <Form.Control as="select" value={selectedPasta} onChange={(e) => setSelectedPasta(e.target.value)} required>
                        <option value="">Selecione uma Pasta</option>
                        {pastas.map(pasta => (
                            <option key={pasta.id} value={pasta.id}>
                                {pasta.nome}
                            </option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group className="mb-3" controlId="paciente">
                    <Form.Label>Paciente (Opcional)</Form.Label>
                    <Form.Control as="select" value={selectedPaciente} onChange={(e) => setSelectedPaciente(e.target.value)}>
                        <option value="">Selecione um Paciente</option>
                        {pacientes.map(paciente => (
                            <option key={paciente.id} value={paciente.id}>
                                {paciente.nome}
                            </option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group className="mb-3" controlId="arquivo">
                    <Form.Label>Arquivo</Form.Label>
                    <Form.Control type="file" onChange={(e) => setArquivo(e.target.files[0])} required={!id} />
                </Form.Group>

                {canSaveDocumento && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Documento
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default DocumentoForm;
