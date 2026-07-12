import axios, { AxiosError, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios';

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000, 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const mockToken = 'mock-jwt-token-xyz-123';
    
    if (config.headers) {
      config.headers.Authorization = `Bearer ${mockToken}`;
    }
    
    console.log(`[API Request] ${config.method?.toUpperCase()} -> ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data;
  },
  (error: AxiosError) => {
    const statusCode = error.response?.status || 500;
    const message = (error.response?.data as any)?.message || error.message || 'An unexpected network error occurred.';

    console.error(`[API Error - ${statusCode}]: ${message}`);
    const standardizedError = new Error(message);
    (standardizedError as any).statusCode = statusCode;

    return Promise.reject(standardizedError);
  }
);

export default apiClient;