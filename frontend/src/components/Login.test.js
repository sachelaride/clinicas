import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Login from './Login';
import axios from 'axios';
import { AuthProvider, useAuth } from '../context/AuthContext';

// Mock axios
jest.mock('axios');

// Mock useAuth
jest.mock('../context/AuthContext', () => ({
  useAuth: jest.fn(),
  AuthProvider: ({ children }) => <div>{children}</div>, // Simple mock for AuthProvider
}));

describe('Login Component', () => {
  const mockSetUser = jest.fn();
  const mockNavigate = jest.fn();

  beforeEach(() => {
    // Reset mocks before each test
    axios.get.mockClear();
    axios.post.mockClear();
    require('react-router-dom').useNavigate.mockReturnValue(mockNavigate); // Access mock directly
    useAuth.mockReturnValue({ setUser: mockSetUser });

    // Mock successful clinic fetch
    axios.get.mockResolvedValueOnce({
      data: [{ id: 1, nome: 'Clinica A' }, { id: 2, nome: 'Clinica B' }],
    });
  });

  test('renders login form correctly', async () => {
    render(<Login />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Usuário/i)).toBeInTheDocument();
    });
    expect(screen.getByLabelText(/Senha/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Selecionar Clínica/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Entrar/i })).toBeInTheDocument();
  });

  test('displays error message on failed login', async () => {
    axios.post.mockRejectedValueOnce(new Error('Network Error'));

    render(<Login />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Usuário/i)).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/Usuário/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/Senha/i), { target: { value: 'wrongpassword' } });
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Ocorreu um erro ao tentar fazer login.');
    });
  });

  test('logs in successfully and navigates to dashboard', async () => {
    axios.post.mockResolvedValueOnce({
      data: { access_token: 'fake-token', token_type: 'Bearer' },
    });
    axios.get.mockResolvedValueOnce({
      data: { username: 'admin', perfil: { nome: 'ADMIN' } },
    });

    render(<Login />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Usuário/i)).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/Usuário/i), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText(/Senha/i), { target: { value: 'admin' } });
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => {
      expect(mockSetUser).toHaveBeenCalledWith({ username: 'admin', perfil: { nome: 'ADMIN' } });
    });
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });
});