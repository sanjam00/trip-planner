import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import { dateInputToApiFormat } from "../../utils/dateTime";
import { useNavigate } from "react-router";
import "../../styles/TripEditForm.css";

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
      <div className="trip-edit-actions-toggle">
        {error && <p className="trip-edit-error">{error}</p>}
        <button className="trip-edit-button" type="button" onClick={() => setEditing(true)}>Edit Trip</button>
        <button className="trip-edit-button trip-edit-delete-button" type="button" onClick={handleDelete}>Delete Trip</button>
      </div>
    );
  }

  return (
    <div className="trip-edit-form-wrapper">
      <form className="trip-edit-form" onSubmit={handleSave}>
        {error && <p className="trip-edit-error">{error}</p>}

        <div className="trip-edit-form-row">
          <input className="trip-edit-input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Trip title" required />
        </div>

        <div className="trip-edit-form-row">
          <input className="trip-edit-input" value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="Destination" />
          <input className="trip-edit-input" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          <input className="trip-edit-input" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>

        <textarea className="trip-edit-textarea" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" />
        <textarea className="trip-edit-textarea" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Notes" />

        <div className="trip-edit-actions">
          <button className="trip-edit-button" type="submit" disabled={loading}>{loading ? "Saving..." : "Save"}</button>
          <button className="trip-edit-button trip-edit-cancel-button" type="button" onClick={() => setEditing(false)}>Cancel</button>
        </div>
      </form>
    </div>
  );
}