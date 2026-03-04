import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Adjusted port to match backend
const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = axios.create({
    baseURL: API_URL,
});

export const login = async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Login failed');
    }
    return response.json();
};

export const getRecords = async () => {
    const token = localStorage.getItem('authToken');
    const response = await api.get('/records', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
};

export const updateRecord = async (recordData) => {
    const token = localStorage.getItem('authToken');
    console.log('API Service: Sending PATCH request to /records with data:', recordData);
    const response = await api.patch('/records', recordData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    console.log('API Service: Response:', response.data);
    return response.data;
};
