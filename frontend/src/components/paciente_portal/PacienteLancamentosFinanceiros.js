import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Container, Alert } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PacienteLancamentosFinanceiros = () => {
    const [lancamentos, setLancamentos] = useState([]);
    const [error, setError] = useState('');
    const { user } = useAuth();

    useEffect(() => {
        if (user && user.perfil === 'PACIENTE') {
            axios.get('http://127.0.0.1:8000/api/paciente/lancamentos-financeiros/')
                .then(response => {
                    setLancamentos(response.data);
                })
                .catch(error => {
                    console.error('Error fetching patient financial entries: ', error);
                    setError('Ocorreu um erro ao carregar seus lançamentos financeiros.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    return (
        <Container>
            <h1 className="my-4">Meus Lançamentos Financeiros</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {user && user.perfil === 'PACIENTE' ? (
                <Table striped bordered hover className="mt-4">
                    <thead>
                        <tr>
                            <th>Descrição</th>
                            <th>Tipo</th>
                            <th>Valor</th>
                            <th>Data de Vencimento</th>
                            <th>Data de Pagamento</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lancamentos.length > 0 ? (
                            lancamentos.map(lancamento => (
                                <tr key={lancamento.id}>
                                    <td>{lancamento.descricao}</td>
                                    <td>{lancamento.tipo}</td>
                                    <td>R$ {parseFloat(lancamento.valor).toFixed(2)}</td>
                                    <td>{new Date(lancamento.data_vencimento).toLocaleDateString()}</td>
                                    <td>{lancamento.data_pagamento ? new Date(lancamento.data_pagamento).toLocaleDateString() : '-'}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="5">Nenhum lançamento financeiro encontrado.</td>
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

export default PacienteLancamentosFinanceiros;