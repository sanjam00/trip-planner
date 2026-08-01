import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import "../../styles/ChecklistItem.css";

export default function ChecklistForm({ tripId, onChecklistCreated }) {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const newChecklist = await apiFetch(`/trips/${tripId}/checklists`, token, {
        method: 'POST',
        body: JSON.stringify({ title }),
      });
      onChecklistCreated(newChecklist);
      setTitle('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="checklist-form" onSubmit={handleSubmit}>
      {error && <p className="checklist-error">{error}</p>}
      <input
        className="checklist-form-input"
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New checklist title"
        required
      />
      <button className="checklist-form-button" type="submit" disabled={loading}>
        {loading ? "Adding..." : "Add Checklist"}
      </button>
    </form>
  );
}