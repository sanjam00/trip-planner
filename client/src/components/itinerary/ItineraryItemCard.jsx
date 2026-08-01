import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import { dateInputToApiFormat, formatDateForDisplay, formatTimeForDisplay, timeInputToApiFormat } from "../../utils/dateTime";
import "../../styles/ItineraryItem.css";

export default function ItineraryCard({
  tripId, itineraryItem, onItineraryItemUpdated, onItineraryItemDeleted
}) {
  const [editing, setEditing] = useState(false);
  const [activity, setActivity] = useState(itineraryItem.activity);
  const [startTime, setStartTime] = useState(itineraryItem.start_time);
  const [endTime, setEndTime] = useState(itineraryItem.end_time);
  const [day, setDay] = useState(itineraryItem.day);
  const [error, setError] = useState('');
  const { token } = useAuth();

  async function handleUpdate(e) {
    e.preventDefault();
    setError('');

    try {
      const updated = await apiFetch(`/trips/${tripId}/itinerary-items/${itineraryItem.id}`, token, {
        method: 'PATCH',
        body: JSON.stringify({
          activity,
          start_time: timeInputToApiFormat(startTime),
          end_time: timeInputToApiFormat(endTime),
          day: dateInputToApiFormat(day),
        }),
      });
      onItineraryItemUpdated(updated);
      setEditing(false);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete() {
    await apiFetch(`/trips/${tripId}/itinerary-items/${itineraryItem.id}`, token, {
      method: 'DELETE',
    });
    onItineraryItemDeleted(itineraryItem.id);
  }

  // if (editing) {
  //   return (
  //     <form onSubmit={handleUpdate}>
  //       {error && <p style={{ color: 'red' }}>{error}</p>}

  //       <input
  //         type="text"
  //         value={activity}
  //         onChange={(e) => setActivity(e.target.value)}
  //         required
  //       />
  //       <input
  //         type="time"
  //         value={startTime}
  //         onChange={(e) => setStartTime(e.target.value)}
  //       />
  //       <input
  //         type="time"
  //         value={endTime}
  //         onChange={(e) => setEndTime(e.target.value)}
  //       />
  //       <input
  //         type="date"
  //         value={day}
  //         onChange={(e) => setDay(e.target.value)}
  //       />

  //       <button type="submit">Save</button>
  //       <button type="button" onClick={() => setEditing(false)}>Cancel</button>
  //     </form>
  //   );
  // }

  return (
    <div className="itinerary-card">
      {editing ? (
        <form className="itinerary-edit-form" onSubmit={handleUpdate}>
          {error && <p className="itinerary-error">{error}</p>}
          <div className="itinerary-edit-row itinerary-edit-row-main">
            <input
              className="itinerary-edit-input"
              type="text"
              value={activity}
              onChange={(e) => setActivity(e.target.value)}
              required
            />
            <div className="itinerary-edit-actions">
              <button type="submit">Save</button>
              <button type="button" onClick={() => setEditing(false)}>Cancel</button>
            </div>
          </div>
          <div className="itinerary-edit-row">
            <input
              className="itinerary-edit-input"
              type="date"
              value={day}
              onChange={(e) => setDay(e.target.value)}
            />
            <input
              className="itinerary-edit-input"
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
            />
            <input
              className="itinerary-edit-input"
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
            />
          </div>
        </form>
      ) : (
        <div className="itinerary-item">
          <div className="itinerary-item-header">
            <h3 className="itinerary-activity" onClick={() => setEditing(true)}>{itineraryItem.activity}</h3>
            <button className="itinerary-delete-btn" type="button" onClick={handleDelete}>Delete item</button>
          </div>
          <p className="itinerary-item-data" onClick={() => setEditing(true)}>{formatDateForDisplay(itineraryItem.day)}: {formatTimeForDisplay(itineraryItem.start_time)}-{formatTimeForDisplay(itineraryItem.end_time)}</p>
        </div>
      )}

      {/* <h3>{itineraryItem.activity}</h3>
      <p>{itineraryItem.day}: {itineraryItem.start_time} – {itineraryItem.end_time}</p>
      <button onClick={() => setEditing(true)}>Edit</button>
      <button onClick={handleDelete}>Delete</button> */}
    </div>
  );
}