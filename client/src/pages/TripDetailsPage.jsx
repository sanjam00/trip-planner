// details for a singular trip

import { useState, useEffect } from "react"
import { useParams } from "react-router";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../api/api";

export default function TripDetailsPage(){
  const { trip_id } = useParams();  // grabs trip_id from /trips/<trip_id>
  const { token } = useAuth();
  const [tripData, setTripData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    apiFetch(`/trips/${trip_id}`, token)
      .then(data => {
        setTripData(data);
        console.log(data);
      })
      .catch(err => {
        setError(err.message)
        console.error(err)
      })
      .finally(() => setLoading(false));
  }, [trip_id, token])

  // make laoding and errors universal and uniform
  if (loading) return <p>Loading...</p>
  if (error) return <p style={{ color: 'red' }}>{error}</p>
  if (!tripData) return <p>Trip not found...</p>

  // add checklists and itineraryitems
  // style page
  return (
    <div>
      <h1>{tripData.title}</h1>
      <p>{tripData.destination}</p>
      <p>{tripData.description}</p>
      <p>{tripData.start_date} - {tripData.end_date}</p>
      <p>{tripData.notes}</p>
    </div>
  )
}