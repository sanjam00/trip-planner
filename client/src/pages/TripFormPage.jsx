// add a new trip

import { useState } from "react";
import { useAuth } from "../context/AuthContext"
import { apiFetch } from "../api/api";
import "../styles/TripForm.css"
import { useNavigate } from "react-router";

const initialFormData = {
  title: '',
  description: '',
  destination: '',
  start_date: '',
  end_date: '',
  notes: ''
};

export default function TripForm(){
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState(initialFormData);
  const { token } = useAuth();
  const navigate = useNavigate();

  function handleChange(field) {
    return (e) => {
      setFormData(prev => ({ ...prev, [field]: e.target.value }));
    };
  }

  // useEffect(() => {
  //   apiFetch('/trips', token, {
  //     method: "POST",
  //     body: JSON.stringify(formData)
  //   })
  //   .then(data => {
  //     console.log(data)
  //   })
  //   .catch(err => console.log(err))
  // }, [])

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const newTrip = await apiFetch('/trips', token, {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      console.log(newTrip);
      setFormData(initialFormData);
      setSuccessMsg('Trip created successfully! Redirecting to trip details...');
      navigate(`/trips/${newTrip.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="trip-form-page">
      <h1>Create a new trip</h1>

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

        <div>
          <label htmlFor="destination">Destination</label>
          <input
            id="destination"
            type="text"
            value={formData.destination}
            onChange={handleChange('destination')}
          />
        </div>

        <div>
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={formData.description}
            onChange={handleChange('description')}
          />
        </div>

        <div>
          <label htmlFor="start_date">Start Date</label>
          <input
            id="start_date"
            type="date"
            value={formData.start_date}
            onChange={handleChange('start_date')}
          />
        </div>

        <div>
          <label htmlFor="end_date">End Date</label>
          <input
            id="end_date"
            type="date"
            value={formData.end_date}
            onChange={handleChange('end_date')}
          />
        </div>

        <div>
          <label htmlFor="notes">Notes</label>
          <textarea
            id="notes"
            value={formData.notes}
            onChange={handleChange('notes')}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
    </div>
  )
}