import ItineraryCard from "./ItineraryItemCard";
import ItineraryForm from "./ItineraryItemForm";


export default function ItinerarySection({
  tripId, itineraryItems, 
  onItineraryItemCreated, onItineraryItemUpdated, onItineraryItemDeleted
  }){

  return(
    <section className="itinerary-section">
      {itineraryItems.length === 0 && <p className="itinerary-empty">No itinerary items yet.</p>}

      {itineraryItems.map(item => (
        <ItineraryCard
          key={item.id}
          tripId={tripId}
          itineraryItem={item}
          onItineraryItemUpdated={onItineraryItemUpdated}
          onItineraryItemDeleted={onItineraryItemDeleted}
        />
      ))}

      <ItineraryForm tripId={tripId} onItineraryItemCreated={onItineraryItemCreated} />
    </section>
  )
}