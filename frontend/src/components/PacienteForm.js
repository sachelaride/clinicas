import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const PacienteForm = () => {
    const { id } = useParams(); // Obtém o ID do paciente da URL, se houver
    const navigate = useNavigate();
    const { user } = useAuth();

    const [nome, setNome] = useState('');
    const [cpf, setCpf] = useState('');
    const [rg, setRg] = useState('');
    const [dataNascimento, setDataNascimento] = useState('');
    const [email, setEmail] = useState('');
    const [telefone, setTelefone] = useState('');
    const [endereco, setEndereco] = useState('');
    const [responsavelLegal, setResponsavelLegal] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        if (id) {
            // Se houver um ID, busca os dados do paciente para edição
            axios.get(`http://127.0.0.1:8000/api/pacientes/${id}/`)
                .then(response => {
                    const pacienteData = response.data;
                    setNome(pacienteData.nome);
                    setCpf(pacienteData.cpf);
                    setRg(pacienteData.rg);
                    setDataNascimento(pacienteData.data_nascimento);
                    setEmail(pacienteData.email);
                    setTelefone(pacienteData.telefone);
                    setEndereco(pacienteData.endereco);
                    setResponsavelLegal(pacienteData.responsavel_legal);
                })
                .catch(error => {
                    console.error('Error fetching patient data: ', error);
                    setError('Paciente não encontrado.');
                });
        }
    }, [id]);

    const handleChangeCpf = (e) => {
        let value = e.target.value;
        value = value.replace(/\D/g, ''); // Remove tudo que não é dígito
        if (value.length > 11) {
            value = value.substring(0, 11);
        }
        if (value.length > 9) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, '$1.$2.$3-$4');
        } else if (value.length > 6) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})$/, '$1.$2.$3');
        } else if (value.length > 3) {
            value = value.replace(/^(\d{3})(\d{3})$/, '$1.$2');
        }
        setCpf(value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const pacienteData = {
            nome,
            cpf,
            rg,
            data_nascimento: dataNascimento,
            email,
            telefone,
            endereco,
            responsavel_legal: responsavelLegal,
        };

        try {
            let response;
            if (id) {
                // Edição
                response = await axios.put(`http://127.0.0.1:8000/api/pacientes/${id}/`, pacienteData);
            } else {
                // Criação
                response = await axios.post('http://127.0.0.1:8000/api/pacientes/', pacienteData);
            }

            if (response.status === 200 || response.status === 201) {
                navigate('/pacientes');
            } else {
                setError(response.data.errors);
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                setError(err.response.data.errors);
            } else {
                setError('Ocorreu um erro ao salvar o paciente.');
            }
            console.error(err);
        }
    };

    const canSavePaciente = user && (user.perfil === 'ADMIN' || user.perfil === 'COORDENADOR' || user.perfil === 'ATENDENTE');

    return (
        <Container>
            <h1 className="my-4">{id ? 'Editar Paciente' : 'Novo Paciente'}</h1>
            {error && <Alert variant="danger">{JSON.stringify(error)}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="nome">
                    <Form.Label>Nome</Form.Label>
                    <Form.Control type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="cpf">
                    <Form.Label>CPF</Form.Label>
                    <Form.Control
                        type="text"
                        value={cpf}
                        onChange={handleChangeCpf}
                        required
                        maxLength="14" // Limita o tamanho máximo do campo com a máscara
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="rg">
                    <Form.Label>RG</Form.Label>
                    <Form.Control type="text" value={rg} onChange={(e) => setRg(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="dataNascimento">
                    <Form.Label>Data de Nascimento</Form.Label>
                    <Form.Control type="date" value={dataNascimento} onChange={(e) => setDataNascimento(e.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3" controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="telefone">
                    <Form.Label>Telefone</Form.Label>
                    <Form.Control type="text" value={telefone} onChange={(e) => setTelefone(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="endereco">
                    <Form.Label>Endereço</Form.Label>
                    <Form.Control as="textarea" value={endereco} onChange={(e) => setEndereco(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="responsavelLegal">
                    <Form.Label>Responsável Legal</Form.Label>
                    <Form.Control type="text" value={responsavelLegal} onChange={(e) => setResponsavelLegal(e.target.value)} />
                </Form.Group>
                {canSavePaciente && (
                    <Button variant="primary" type="submit" className="mt-3">
                        Salvar Paciente
                    </Button>
                )}
            </Form>
        </Container>
    );
};

export default PacienteForm;
