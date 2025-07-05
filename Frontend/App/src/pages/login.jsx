import {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import api from '../services/api';

function Login(){
    const [formData, setFormData] = useState({
                                             username: '',
                                             password: '',
    });

    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData, [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try{
            await api.getCSRFToken();

            const response = await api.login(formData);

            if (response.status === 200){
                navigate('/home')
            }
        } catch (error){
            setError(error.response?.data?.error || 'Login faild')
        };

    }


    return(
        <>
            <div className="auth-form">
                <h2>Login</h2>
                {error && <div className="error">{error}</div>}

                <form onSubmit={handleSubmit} >

                    <input type="text" name="username" value={formData} onChange={handleChange} placeholder="username" required />
                    
                    <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="password" required />

                    <button type="submit">Log In</button>

                    <button type="button" onClick={() => navigate('/signup')}>Sign Up</button>

                </form>
            </div>
        </>
    );




};

export default Login