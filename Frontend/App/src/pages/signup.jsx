import { useState } from 'react';
import {useNavigate} from 'react-router-dom';
import api from '../services/api';

function Signup(){

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        role: 'customer',
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

            const signupMethod = formData.role ==='customer' ? api.signupCustomer 
                                                             : api.signupEventOwner;

            const response = await signupMethod(formData);

            if(response.status === 201){
                navigate('/login');
            }

        }catch (err) {
            setError(err.response?.data?.error || 'signup failed');
        }
    
    }

    return(
        <>
            <div className="signup">
                <h2>SignUp</h2>
                {error && <div className="error">error</div>}
                <form>
                    <input type="text" name="username" value={formData.username} onChange={handleChange} placeholder="Username" required/>

                    <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="example@gmail.com" required />

                    <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="password" required />

                    <select name="role" value={formData.role} onChange={handleChange}>
                        <option value="customer">User</option>
                        <option value="event_owner">Organizer</option>
                    </select>

                     <button type="submit" onSubmit={handleSubmit}>Sign Up</button>

                </form>
            </div>
        </>
    )
};

export default Signup