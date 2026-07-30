import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import { dateInputToApiFormat, timeInputToApiFormat } from "../../utils/dateTime";
import "../../styles/ItineraryItem.css";

export default function ItineraryForm({ tripId, onItineraryItemCreated }) {
  const [activity, setActivity] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [day, setDay] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const newItineraryItem = await apiFetch(`/trips/${tripId}/itinerary-items`, token, {
        method: 'POST',
        body: JSON.stringify({
          activity,
          start_time: timeInputToApiFormat(startTime),
          end_time: timeInputToApiFormat(endTime),
          day: dateInputToApiFormat(day),
        }),
      });
      onItineraryItemCreated(newItineraryItem);
      setActivity('');
      setStartTime('');
      setEndTime('');
      setDay('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="itinerary-form" onSubmit={handleSubmit}>
      {error && <p className="itinerary-error">{error}</p>}
      <div className="itinerary-form-row itinerary-form-row-main">
        <input
          className="itinerary-form-input"
          type="text"
          value={activity}
          onChange={(e) => setActivity(e.target.value)}
          placeholder="Activity"
          required
        />
        <button className="itinerary-form-button" type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add item"}
        </button>
      </div>
      <div className="itinerary-form-row">
        <input
          className="itinerary-form-input"
          type="date"
          value={day}
          onChange={(e) => setDay(e.target.value)}
          placeholder="Date"
          required
        />
        <input
          className="itinerary-form-input"
          type="time"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          placeholder="Start time"
          required
        />
        <input
          className="itinerary-form-input"
          type="time"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          placeholder="End time"
          required
        />
      </div>
    </form>
  )
}