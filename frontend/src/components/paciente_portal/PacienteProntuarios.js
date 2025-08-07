import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PacienteProntuarios = () => {
    const [prontuarios, setProntuarios] = useState([]);
    const [error, setError] = useState('');
    const { user } = useAuth();

    useEffect(() => {
        if (user && user.perfil === 'PACIENTE') {
            axios.get('http://127.0.0.1:8000/api/paciente/prontuarios/')
                .then(response => {
                    setProntuarios(response.data);
                })
                .catch(error => {
                    console.error('Error fetching patient medical records: ', error);
                    setError('Ocorreu um erro ao carregar seus prontuários.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    return (
        <Container>
            <h1 className="my-4">Meus Prontuários</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {user && user.perfil === 'PACIENTE' ? (
                <Table striped bordered hover className="mt-4">
                    <thead>
                        <tr>
                            <th>Tipo de Tratamento</th>
                            <th>Data de Criação</th>
                            <th>Finalizado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {prontuarios.length > 0 ? (
                            prontuarios.map(prontuario => (
                                <tr key={prontuario.id}>
                                    <td>{prontuario.tipo_tratamento_definido__nome}</td>
                                    <td>{new Date(prontuario.data_criacao).toLocaleDateString()}</td>
                                    <td>{prontuario.is_finalized ? 'Sim' : 'Não'}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="3">Nenhum prontuário encontrado.</td>
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

export default PacienteProntuarios;