import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext"
import { apiFetch } from "../api/api";
import TripCard from "../components/trips/TripCard";

export default function TripsPage(){
  const { token } = useAuth();
  const [trips, setTrips] = useState([]);

  // GET all trips, display trip card
  useEffect(() => {
    apiFetch('/trips', token)
      // breaks when i add this part:
      // .then(r => {
      //   if (!r.ok) {throw new Error("Failed to fetch")};
      //   return r.json();
      // })
      .then(data => {
        setTrips(data.trips);
        console.log(data.trips);
      })
      .catch(err => console.error(err));
  }, [token])
  
  return (
    <>
      <h1> Trips page</h1>
    
      <div>
        {/* {trips.map(trip => (
          <div key={trip.id}>{trip.title} {trip.start_date}</div>
        ))} */}

        {trips.map(trip => (
          <TripCard key={trip.id} trip={trip}/>
        ))}
      </div>
    </>

  )
}