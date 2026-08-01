// single item with checkbox/status toggle, edit, delete

import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";
import "../../styles/ChecklistItem.css";

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
    <li className="checklist-item">
      <input
        className="checklist-item-checkbox"
        type="checkbox"
        checked={item.status === 'packed'}
        onChange={toggleStatus}
      />
      <span className={`checklist-item-name ${item.status === 'packed' ? 'is-packed' : ''}`}>
        {item.item_name}
      </span>
      <button className="checklist-item-delete" type="button" onClick={handleDelete}>×</button>
    </li>
  );
}