import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Card, Row, Col, Alert } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PacienteDashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [error, setError] = useState('');
    const { user } = useAuth();

    useEffect(() => {
        if (user && user.perfil === 'PACIENTE') {
            axios.get('http://127.0.0.1:8000/api/paciente/dashboard/')
                .then(response => {
                    setDashboardData(response.data);
                })
                .catch(error => {
                    console.error('Error fetching patient dashboard data: ', error);
                    setError('Ocorreu um erro ao carregar o dashboard do paciente.');
                });
        } else if (user) {
            setError('Você não tem permissão para acessar esta página.');
        }
    }, [user]);

    if (error) {
        return <Container><Alert variant="danger">{error}</Alert></Container>;
    }

    if (!dashboardData) {
        return <Container>Carregando dashboard...</Container>;
    }

    return (
        <Container>
            <h1 className="my-4">Bem-vindo, {dashboardData.paciente.nome}!</h1>
            <Row>
                <Col md={4}>
                    <Card className="text-center mb-3">
                        <Card.Body>
                            <Card.Title>Agendamentos Futuros</Card.Title>
                            <Card.Text className="fs-1">{dashboardData.agendamentos_futuros.length}</Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={4}>
                    <Card className="text-center mb-3">
                        <Card.Body>
                            <Card.Title>Últimos Prontuários</Card.Title>
                            <Card.Text className="fs-1">{dashboardData.ultimos_prontuarios.length}</Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={4}>
                    <Card className="text-center mb-3">
                        <Card.Body>
                            <Card.Title>Últimos Lançamentos Financeiros</Card.Title>
                            <Card.Text className="fs-1">{dashboardData.ultimos_lancamentos.length}</Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            {/* Você pode adicionar mais seções aqui, como agendamentos futuros, etc. */}
        </Container>
    );
};

export default PacienteDashboard;