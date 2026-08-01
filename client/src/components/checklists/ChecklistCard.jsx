// one checklist with its items

import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import ChecklistItemRow from "./ChecklistItemRow";
import ChecklistItemForm from "./ChecklistItemForm.jsx";
import "../../styles/ChecklistItem.css";

export default function ChecklistCard({
  tripId, checklist,
  onChecklistUpdated, onChecklistDeleted,
  onItemCreated, onItemChanged, onItemDeleted
}) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(checklist.title);
  const { token } = useAuth();

  async function handleRename(e) {
    e.preventDefault();
    const updated = await apiFetch(`/trips/${tripId}/checklists/${checklist.id}`, token, {
      method: 'PATCH',
      body: JSON.stringify({ title }),
    });
    onChecklistUpdated(updated);
    setTitle(updated)
    setEditing(false);
  }

  async function handleDelete() {
    await apiFetch(`/trips/${tripId}/checklists/${checklist.id}`, token, {
      method: 'DELETE',
    });
    onChecklistDeleted(checklist.id);
  }

  return (
    <div className="checklist-card" id={`checklist-card-${checklist.id}`}>
      {editing ? (
        <form className="checklist-edit-form" onSubmit={handleRename}>
          <input
            className="checklist-edit-input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <div className="checklist-edit-actions">
            <button type="submit">Save</button>
            <button type="button" onClick={() => setEditing(false)}>Cancel</button>
          </div>
        </form>
      ) : (
        <div className="checklist-header">
          <h3 className="checklist-title" onClick={() => setEditing(true)}>{checklist.title}</h3>
          <button className="checklist-delete-btn" type="button" onClick={handleDelete}>Delete checklist</button>
        </div>
      )}

      {!editing && (
        <>
          <ul className="checklist-list">
            {checklist.items.map(item => (
              <ChecklistItemRow
                key={item.id}
                tripId={tripId}
                checklistId={checklist.id}
                item={item}
                onItemChanged={onItemChanged}
                onItemDeleted={onItemDeleted}
              />
            ))}
          </ul>

          <ChecklistItemForm
            tripId={tripId}
            checklistId={checklist.id}
            onItemCreated={onItemCreated}
          />
        </>
      )}
    </div>
  );
}