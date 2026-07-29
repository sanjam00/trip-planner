import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiFetch } from "../../api/api";

export default function ChecklistItemForm({ tripId, checklistId, onItemCreated }) {
  const [itemName, setItemName] = useState('');
  const { token } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    const newItem = await apiFetch(`/trips/${tripId}/checklists/${checklistId}/checklist-items`, token, {
      method: 'POST',
      body: JSON.stringify({ item_name: itemName }),
    });
    onItemCreated(checklistId, newItem);
    setItemName('');
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={itemName}
        onChange={(e) => setItemName(e.target.value)}
        placeholder="Add item"
        required
      />
      <button type="submit">Add</button>
    </form>
  );
}