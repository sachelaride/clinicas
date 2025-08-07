import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Alert } from 'react-bootstrap';

const ProfissionalProntuarios = () => {
    const [prontuarios, setProntuarios] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/profissional/prontuarios/')
            .then(response => {
                setProntuarios(response.data);
            })
            .catch(error => {
                console.error('Error fetching professional medical records: ', error);
                setError('Ocorreu um erro ao carregar os prontuários do profissional.');
            });
    }, []);

    return (
        <Container>
            <h1 className="my-4">Prontuários de Pacientes</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            <Table striped bordered hover className="mt-4">
                <thead>
                    <tr>
                        <th>Paciente</th>
                        <th>Tipo de Tratamento</th>
                        <th>Data de Criação</th>
                        <th>Finalizado</th>
                    </tr>
                </thead>
                <tbody>
                    {prontuarios.length > 0 ? (
                        prontuarios.map(prontuario => (
                            <tr key={prontuario.id}>
                                <td>{prontuario.paciente}</td>
                                <td>{prontuario.tipo_tratamento}</td>
                                <td>{new Date(prontuario.data_criacao).toLocaleDateString()}</td>
                                <td>{prontuario.is_finalized ? 'Sim' : 'Não'}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="4">Nenhum prontuário encontrado.</td>
                        </tr>
                    )}
                </tbody>
            </Table>
        </Container>
    );
};

export default ProfissionalProntuarios;
