import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext"
import { apiFetch } from "../api/api";
import TripCard from "../components/trips/TripCard";
import "../styles/TripsPage.css";

export default function TripsPage(){
  const { token } = useAuth();
  const [trips, setTrips] = useState([]);

  // GET all trips, display trip card
  useEffect(() => {
    apiFetch('/trips', token)
      .then(data => {
        setTrips(data.trips);
        console.log(data.trips);
      })
      .catch(err => console.error(err));
  }, [token])
  
  return (
    <main className="trips-page">
      <h1>Trips</h1>

      <div className="trips-grid">
        {trips.map(trip => (
          <TripCard key={trip.id} trip={trip}/>
        ))}
      </div>
    </main>
  )
}