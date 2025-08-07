import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PacienteAgendamentos = () => {
    const [agendamentos, setAgendamentos] = useState([]);
    const [error, setError] = useState('');
    const { user } = useAuth();

    useEffect(() => {
        if (user && user.perfil === 'PACIENTE') {
            axios.get('http://127.0.0.1:8000/api/paciente/agendamentos/')
                .then(response => {
                    setAgendamentos(response.data);
                })
                .catch(error => {
                    console.error('Error fetching patient appointments: ', error);
                    setError('Ocorreu um erro ao carregar seus agendamentos.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    return (
        <Container>
            <h1 className="my-4">Meus Agendamentos</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {user && user.perfil === 'PACIENTE' ? (
                <Table striped bordered hover className="mt-4">
                    <thead>
                        <tr>
                            <th>Profissional</th>
                            <th>Data</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {agendamentos.length > 0 ? (
                            agendamentos.map(agendamento => (
                                <tr key={agendamento.id}>
                                    <td>{agendamento.profissional__user__username}</td>
                                    <td>{new Date(agendamento.data).toLocaleString()}</td>
                                    <td>{agendamento.status}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="3">Nenhum agendamento encontrado.</td>
                            </tr>
                        )}
                    </tbody>
                </Table>
            ) : (
                <Alert variant="warning">Acesso restrito a pacientes.</Alert>
            )}
        </Container>
    );
};

export default PacienteAgendamentos;
