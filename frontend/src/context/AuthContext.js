import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const tokenType = localStorage.getItem('token_type');

        if (token && tokenType) {
            axios.defaults.headers.common['Authorization'] = `${tokenType} ${token}`;
            console.log("Token being sent:", `${tokenType} ${token}`);
            axios.get('http://127.0.0.1:8000/api/users/me')
                .then(response => {
                    console.log("User data from /users/me:", JSON.stringify(response.data, null, 2));
                    setUser(response.data);
                })
                .catch(error => {
                    console.error('Error fetching user data: ', error);
                    // Clear token if it's invalid
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('token_type');
                });
        }
    }, []);

    return (
        <AuthContext.Provider value={{ user, setUser }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
