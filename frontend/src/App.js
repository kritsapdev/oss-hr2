import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [citizenId, setCitizenId] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [leaves, setLeaves] = useState([]);

  const login = async () => {
    const res = await axios.post('http://localhost:8000/login', { citizen_id: citizenId, password });
    setToken(res.data.token);
  };

  const fetchLeaves = async () => {
    const res = await axios.get('http://localhost:8000/leaves', {
      headers: { Authorization: `Bearer ${token}` }
    });
    setLeaves(res.data);
  };

  return (
    <div>
      <h1>Login</h1>
      <input value={citizenId} onChange={e => setCitizenId(e.target.value)} placeholder="Citizen ID" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button onClick={login}>Login</button>

      <h2>Leaves</h2>
      <button onClick={fetchLeaves}>Fetch Leaves</button>
      <ul>{leaves.map((l, i) => <li key={i}>{l.leave_type} ({l.start_date} to {l.end_date})</li>)}</ul>
    </div>
  );
}

export default App;
