//display a card on TripsPage (fetches all trips)

export default function TripCard({ props, trip}){

  return (
    <div id="tripCard">
      <h2>{trip.title}</h2>
      <p>{trip.start_date}</p>
      <p>{trip.end_date}</p>
    </div>
  )
}