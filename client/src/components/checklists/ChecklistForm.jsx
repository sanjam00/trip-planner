// create checklist title

import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { useNavigate, useParams } from "react-router";
import { apiFetch } from "../../api/api";

const initialFormData = {
  title: ''
}

export default function ChecklistForm(){
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState(initialFormData)  
  const { token } = useAuth();
  const { trip_id } = useParams();
  // const navigate = useNavigate();

  function handleChange(field){
    return (e) => {
      setFormData(prev => ({...prev, [field]: e.target.value}));
    }
  }

  async function handleSubmit(e) {
      e.preventDefault();
      setError('');
      setSuccessMsg('');
      setLoading(true);
  
      try {
        const newChecklist = await apiFetch(`/trips/${trip_id}/checklists`, token, {
          method: 'POST',
          body: JSON.stringify(formData),
        });
        console.log(newChecklist);
        setFormData(initialFormData);
        setSuccessMsg('Checklist created successfully! Reload to view new trip');
        // navigate(`/trips/${newTrip.id}`);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

  return (
    <div>
      <h1>Create a new checklist</h1>
      <p>Start with the title, then add items.</p>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {successMsg && <p style={{ color: 'green' }}>{successMsg}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            type="text"
            value={formData.title}
            onChange={handleChange('title')}
            required
          />
        </div>
      </form>
    </div>
  )
}