import React, { useState } from 'react';

const Signup = ({ onSignup, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    role: 'member'
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // ✅ VERY IMPORTANT

    console.log("Form submitted"); // Debug

    setLoading(true);
    setError('');

    try {
      const response = await fetch('https://task-manager-backend-l0h5.onrender.com/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Registration Successful, Now login! ")
        setFormData({
          username:"",
          password:"",
          role:"member"
        })
        onSwitchToLogin();
        // onSignup(data.user, data.access_token);
      
      } else {
        setError(data.error || 'Signup failed');
      }
    } catch (err) {
      console.error(err);
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">Sign Up</h2>

        {/* ✅ CLEAN FORM */}
        <form onSubmit={handleSubmit}>
          
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              name="username"
              className="form-input"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Role</label>
            <select
              name="role"
              className="form-select"
              value={formData.role}
              onChange={handleChange}
            >
              <option value="member">Member</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>

        <div className="auth-switch">
          Already have an account?{' '}
          <button type="button" onClick={onSwitchToLogin}>
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default Signup;