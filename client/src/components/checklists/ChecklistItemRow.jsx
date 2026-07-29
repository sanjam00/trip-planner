// single item with checkbox/status toggle, edit, delete

import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";

export default function ChecklistItemRow({ tripId, checklistId, item, onItemChanged, onItemDeleted }) {
  const { token } = useAuth();

  async function toggleStatus() {
    const newStatus = item.status === 'packed' ? 'not packed' : 'packed';
    const updated = await apiFetch(`/trips/${tripId}/checklists/${checklistId}/checklist-items/${item.id}`, token, {
      method: 'PATCH',
      body: JSON.stringify({ status: newStatus }),
    });
    onItemChanged(checklistId, updated);
  }

  async function handleDelete() {
    await apiFetch(`/trips/${tripId}/checklists/${checklistId}/checklist-items/${item.id}`, token, {
      method: 'DELETE',
    });
    onItemDeleted(checklistId, item.id);
  }

  return (
    <li>
      <input
        type="checkbox"
        checked={item.status === 'packed'}
        onChange={toggleStatus}
      />
      {item.item_name}
      <button onClick={handleDelete}>×</button>
    </li>
  );
}