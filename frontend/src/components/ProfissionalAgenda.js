import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const ProfissionalAgenda = () => {
    const [agendamentos, setAgendamentos] = useState([]);
    const [error, setError] = useState('');
    const { user } = useAuth();

    useEffect(() => {
        // Only fetch if the user is a PROFESSIONAL
        if (user && user.perfil === 'PROFISSIONAL') {
            axios.get('http://127.0.0.1:8000/api/profissional/agenda/')
                .then(response => {
                    setAgendamentos(response.data);
                })
                .catch(error => {
                    console.error('Error fetching professional agenda: ', error);
                    setError('Ocorreu um erro ao carregar a agenda do profissional.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    return (
        <Container>
            <h1 className="my-4">Minha Agenda</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {user && user.perfil === 'PROFISSIONAL' ? (
                <Table striped bordered hover className="mt-4">
                    <thead>
                        <tr>
                            <th>Paciente</th>
                            <th>Data</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {agendamentos.length > 0 ? (
                            agendamentos.map(agendamento => (
                                <tr key={agendamento.id}>
                                    <td>{agendamento.paciente__nome}</td>
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
                <Alert variant="warning">Acesso restrito a profissionais.</Alert>
            )}
        </Container>
    );
};

export default ProfissionalAgenda;
