//display a card on TripsPage (fetches all trips)
import "../../styles/TripCard.css";

export default function TripCard({ props, trip}){

  return (
    <article className="trip-card">
      <h2>{trip.title}</h2>
      <div className="trip-meta">
        <p className="trip-date">Start: {trip.start_date}</p>
        <p className="trip-date">End: {trip.end_date}</p>
      </div>
    </article>
  )
}