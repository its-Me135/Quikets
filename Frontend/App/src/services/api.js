import axios from 'axios';

const api = axios.create({
    baseURL: Process.env.REACT_APP_API_URL || 'http://localhost:3000/api',
    withCredentials: true,
});


api.interceptors.request.use(
    (config) => {
        const csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
        if (csrfToken){
            config.headers['X-CSRFToken'] = csrfToken;
        }
        return config;
    }
);

export default{
    login: (credentials) => api.post('/login/', credentials),
    signupCustomer: (data) => api.post('signup/customer/', data),
    signupEventOwner: (data) => api.post('signup/event-owner', data),

    getCSRFToken: () => api.get('/csrf/')
};