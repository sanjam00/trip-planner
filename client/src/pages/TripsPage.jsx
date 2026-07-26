import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext"
import { apiFetch } from "../api/api";
import TripCard from "../components/trips/TripCard";
import "../styles/TripsPage.css";
import { useNavigate } from "react-router";

export default function TripsPage(){
  const { token } = useAuth();
  const [trips, setTrips] = useState([]);

  const navigate = useNavigate();

  // GET all trips, display trip card
  useEffect(() => {
    apiFetch('/trips', token)
      .then(data => {
        setTrips(data.trips);
        console.log(data.trips);
      })
      .catch(err => console.error(err));
  }, [token])

  function tripDetailsNav(tripData){
    navigate(`/trips/${tripData.id}`)
  }
  
  return (
    <main className="trips-page">
      <h1>Trips</h1>

      <div className="trips-grid">
        {trips.map(trip => (
          <div onClick={() => tripDetailsNav(trip)}>
            <TripCard key={trip.id} trip={trip}/>
          </div>
        ))}
      </div>
    </main>
  )
}