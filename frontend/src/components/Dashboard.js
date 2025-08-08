import React, { useEffect, useState } from 'react';
import { Container, Alert, Row, Col, Card, Button } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

// Configura o localizador para o calendário
const localizer = momentLocalizer(moment);

const Dashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [calendarEvents, setCalendarEvents] = useState([]);
    const [currentView, setCurrentView] = useState('month'); // Estado para a visualização atual
    const [currentDate, setCurrentDate] = useState(new Date()); // Estado para a data atual

    useEffect(() => {
        if (!user) return; // Só executa se o usuário estiver logado

        // Buscar agendamentos para o calendário
        axios.get('http://127.0.0.1:8000/api/agendamentos/')
            .then(response => {
                const events = response.data.map(agendamento => ({
                    title: `Agendamento: ${agendamento.paciente_nome} (${agendamento.profissional_username})`,
                    start: new Date(agendamento.data),
                    end: new Date(moment(agendamento.data).add(1, 'hour').toISOString()), // Assume 1 hora de duração
                    allDay: false,
                    resource: agendamento, // Armazena o objeto completo do agendamento
                }));
                setCalendarEvents(events);
            })
            .catch(error => {
                console.error('Erro ao buscar agendamentos:', error);
            });

    }, [user]);

    if (!user) {
        return (
            <Container>
                <Alert variant="warning">
                    <h4>Acesso Restrito</h4>
                    <p>Você precisa fazer login para acessar o sistema.</p>
                    <Button variant="primary" onClick={() => navigate('/login')}>Fazer Login</Button>
                </Alert>
            </Container>
        );
    }

    return (
        <Container fluid>
            <Row>
                <Col md={12} className="mb-4">
                    <Card>
                        <Card.Header className="bg-primary text-white">
                            <h5 className="card-title mb-0">Calendário de Agendamentos</h5>
                        </Card.Header>
                        <Card.Body style={{ height: '500px' }}>
                            <Calendar
                                localizer={localizer}
                                events={calendarEvents}
                                startAccessor="start"
                                endAccessor="end"
                                style={{ height: '100%' }}
                                min={new Date(0, 0, 0, 7, 0, 0)} // 7 AM
                                max={new Date(0, 0, 0, 22, 0, 0)} // 10 PM
                                dayPropGetter={(date) => {
                                    const dayOfWeek = date.getDay();
                                    if (dayOfWeek === 0) { // Sunday
                                        return {
                                            style: {
                                                display: 'none',
                                            },
                                        };
                                    }
                                    return {};
                                }}
                                messages={{
                                    next: "Próximo",
                                    previous: "Anterior",
                                    today: "Hoje",
                                    month: "Mês",
                                    week: "Semana",
                                    day: "Dia",
                                    agenda: "Agenda",
                                    date: "Data",
                                    time: "Hora",
                                    event: "Evento",
                                    noEventsInRange: "Nenhum agendamento neste período.",
                                    showMore: total => `+ ${total} mais`
                                }}
                                onSelectEvent={event => alert(event.title)}
                                onSelectSlot={slotInfo => alert(
                                    `Novo agendamento em: ${slotInfo.start.toLocaleString()} - ${slotInfo.end.toLocaleString()}`
                                )}
                                selectable
                                view={currentView} // Controla a visualização
                                date={currentDate} // Controla a data
                                onNavigate={date => setCurrentDate(date)} // Atualiza a data ao navegar
                                onView={view => setCurrentView(view)} // Atualiza a visualização
                            />
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            
        </Container>
    );
};

export default Dashboard;