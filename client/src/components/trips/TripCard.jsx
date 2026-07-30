//display a card on TripsPage (fetches all trips)
import "../../styles/TripCard.css";
import { formatDateForDisplay } from "../../utils/dateTime";

export default function TripCard({ trip }){

  return (
    <article className="trip-card">
      <h2>{trip.title}</h2>
      <div className="trip-meta">
        <p className="trip-date">{formatDateForDisplay(trip.start_date)} - </p>
        <p className="trip-date">{formatDateForDisplay(trip.end_date)}</p>
      </div>
    </article>
  )
}