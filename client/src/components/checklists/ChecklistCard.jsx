// one checklist with its items

import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import ChecklistItemRow from "./ChecklistItemRow";
import ChecklistItemForm from "./ChecklistItemForm.jsx";

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
    <div>
      {editing ? (
        <form onSubmit={handleRename}>
          <input value={title} onChange={(e) => setTitle(e.target.value)} required />
          <button type="submit">Save</button>
          <button type="button" onClick={() => setEditing(false)}>Cancel</button>
        </form>
      ) : (
        <h3 onClick={() => setEditing(true)}>{checklist.title}</h3>
      )}

      <button onClick={handleDelete}>Delete checklist</button>

      <ul>
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
    </div>
  );
}