import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const login = async (email, password) => {
  const response = await axios.post(`${API_URL}/login`, { email, password });
  return response.data;
};

const calculateEmissions = async (token) => {
  const response = await axios.get(`${API_URL}/calculate-emissions`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

const getRecommendation = async (token) => {
  const response = await axios.get(`${API_URL}/recommendation`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export { login, calculateEmissions, getRecommendation };
