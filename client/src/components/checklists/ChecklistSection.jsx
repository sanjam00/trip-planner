// shown inside TripDetailPage, lists all checklists for that trip

import ChecklistCard from "./ChecklistCard";
import ChecklistForm from "./ChecklistForm";

export default function ChecklistSection({
  tripId, checklists,
  onChecklistCreated, onChecklistUpdated, onChecklistDeleted,
  onItemCreated, onItemChanged, onItemDeleted
  }) {

  return (
    <section>
      {checklists.length === 0 && <p>No checklists yet.</p>}

      {checklists.map(checklist => (
        <ChecklistCard
          key={checklist.id}
          tripId={tripId}
          checklist={checklist}
          onChecklistUpdated={onChecklistUpdated}
          onChecklistDeleted={onChecklistDeleted}
          onItemCreated={onItemCreated}
          onItemChanged={onItemChanged}
          onItemDeleted={onItemDeleted}
        />
      ))}

      <ChecklistForm tripId={tripId} onChecklistCreated={onChecklistCreated} />
    </section>
  );
}