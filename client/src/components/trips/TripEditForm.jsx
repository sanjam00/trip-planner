import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import { timeInputToApiFormat, dateInputToApiFormat } from "../../utils/dateTime";
import { useNavigate } from "react-router";

export default function TripEditForm({ tripId, trip, onTripUpdated, onTripDeleted }) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(trip.title);
  const [destination, setDestination] = useState(trip.destination);
  const [description, setDescription] = useState(trip.description);
  const [startDate, setStartDate] = useState(trip.start_date);
  const [endDate, setEndDate] = useState(trip.end_date);
  const [notes, setNotes] = useState(trip.notes);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();
  const navigate = useNavigate();

  async function handleSave(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const updated = await apiFetch(`/trips/${tripId}`, token, {
        method: 'PATCH',
        body: JSON.stringify({
          title,
          destination,
          description,
          start_date: dateInputToApiFormat(startDate),
          end_date: dateInputToApiFormat(endDate),
          notes,
        }),
      });
      onTripUpdated(updated);
      setEditing(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete() {
    const confirmed = window.confirm(`Delete "${trip.title}"? This CANNOT be undone.`);
    if (!confirmed) return;

    try {
      await apiFetch(`/trips/${tripId}`, token, { method: 'DELETE' });
      onTripDeleted();
    } catch (err) {
      setError(err.message);
    } finally {
      navigate(`/trips`)
    }
  }

  if (!editing) {
    return (
      <div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button onClick={() => setEditing(true)}>Edit Trip</button>
        <button onClick={handleDelete}>Delete Trip</button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSave}>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <input value={title} onChange={(e) => setTitle(e.target.value)} required />
      <input value={destination} onChange={(e) => setDestination(e.target.value)} />
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
      <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
      <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
      <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />

      <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save"}</button>
      <button type="button" onClick={() => setEditing(false)}>Cancel</button>
    </form>
  );
}