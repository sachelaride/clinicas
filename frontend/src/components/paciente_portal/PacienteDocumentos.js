import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Alert, Button } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PacienteDocumentos = () => {
    const [documentos, setDocumentos] = useState([]);
    const [error, setError] = useState('');
    const { user } = useAuth();

    useEffect(() => {
        if (user && user.perfil === 'PACIENTE') {
            axios.get('http://127.0.0.1:8000/api/paciente/documentos/')
                .then(response => {
                    setDocumentos(response.data);
                })
                .catch(error => {
                    console.error('Error fetching patient documents: ', error);
                    setError('Ocorreu um erro ao carregar seus documentos.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    return (
        <Container>
            <h1 className="my-4">Meus Documentos</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {user && user.perfil === 'PACIENTE' ? (
                <Table striped bordered hover className="mt-4">
                    <thead>
                        <tr>
                            <th>Pasta</th>
                            <th>Arquivo</th>
                            <th>Data de Upload</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {documentos.length > 0 ? (
                            documentos.map(documento => (
                                <tr key={documento.id}>
                                    <td>{documento.pasta__nome}</td>
                                    <td><a href={documento.arquivo} target="_blank" rel="noreferrer">{documento.arquivo}</a></td>
                                    <td>{new Date(documento.uploaded_at).toLocaleDateString()}</td>
                                    <td>
                                        <Button variant="info" size="sm" href={documento.arquivo} target="_blank">Visualizar</Button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="4">Nenhum documento encontrado.</td>
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

export default PacienteDocumentos;