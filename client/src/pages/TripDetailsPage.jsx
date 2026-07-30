// details for a singular trip

import { useState, useEffect, act } from "react"
import { useParams } from "react-router";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../api/api";
import "../styles/TripDetailsPage.css";
import "../styles/ChecklistItinerary.css";
import ChecklistSection from "../components/checklists/ChecklistSection";
import ChecklistForm from "../components/checklists/ChecklistForm";
import ItinerarySection from "../components/itinerary/ItinerarySection";

export default function TripDetailsPage(){
  const { trip_id } = useParams();  // grabs trip_id from /trips/<trip_id>
  const { token } = useAuth();
  const [tripData, setTripData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(1);
  const [isScrolled, setIsScrolled] = useState(false);

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

  // checklist and checklistitem CRUD
  function handleChecklistCreated(newChecklist){
    setTripData(prev => ({
      ...prev,
      checklists:[ ...prev.checklists, { ...newChecklist, items: [] }]
    }));
  }

  function handleChecklistUpdated(updatedChecklist) {
    setTripData(prev => ({
      ...prev,
      checklists: prev.checklists.map(c =>
        c.id === updatedChecklist.id ? { ...c, ...updatedChecklist } : c
      )
    }));
  }

  function handleChecklistDeleted(checklistId){
    setTripData(prev => ({
      ...prev,
      checklists: prev.checklists.filter(c => c.id !== checklistId)
    }));
  }
  
  function handleItemCreated(checklistId, newItem){
    setTripData(prev => ({
      ...prev,
      checklists: prev.checklists.map(c =>
        c.id !== checklistId ? c : {...c, items: [...c.items, newItem]}
      )
    }));
  }

  function handleItemChanged(checklistId, updatedItem){
    setTripData( prev => ({
      ...prev,
      checklists: prev.checklists.map(c => 
        c.id !== checklistId ? c : {
          ...c,
          items: c.items.map(i => i.id === updatedItem.id ? updatedItem : i)
        }
      )
    }));
  }

  function handleItemDeleted(checklistId, itemId){
    setTripData(prev => ({
      ...prev,
      checklists: prev.checklists.map(c => 
        c.id !== checklistId ? c : {...c, items: c.items.filter(i => i.id !== itemId)}
      )
    }));
  }

  // itinerary item CRUD
  function handleItineraryItemCreated(newItem) {
    setTripData(prev => ({
      ...prev,
      itinerary_items: [...prev.itinerary_items, newItem]
    }));
  }

  function handleItineraryItemUpdated(updatedItem) {
    setTripData(prev => ({
      ...prev,
      itinerary_items: prev.itinerary_items.map(i =>
        i.id === updatedItem.id ? { ...i, ...updatedItem } : i
      )
    }));
  }

  function handleItineraryItemDeleted(itemId) {
    setTripData(prev => ({
      ...prev,
      itinerary_items: prev.itinerary_items.filter(i => i.id !== itemId)
    }));
  }

  // scroll event listener
  useEffect(() => {
    const handleScroll = () => {
      // let ticking = false;

      // const handleScroll = () => {
      //   if (!ticking) {
      //     window.requestAnimationFrame(() => {
      //       setIsScrolled(window.scrollY > 6);
      //       ticking = false;
      //     });

      //     ticking = true;
      //   }
      // }
      setIsScrolled(window.scrollY > 8);
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // eventually make laoding and errors universal and uniform
  if (loading) return <p>Loading...</p>
  if (error) return <p style={{ color: 'red' }}>{error}</p>
  if (!tripData) return <p>Trip not found...</p>

  function updateTabs(id){
    setActiveTab(id);
  }

  return (
    <div className="trip-details-page">
      {/* <div className="header-buttons-container">  
      added new classname bc someone on stack overflow said to group in the same container to make sticky work properly 
      but that messed up the sticky of the header alone*/}
        <header className={`trip-details-header${isScrolled ? " trip-details-header-scrolled" : ""}`}>
          <div className="trip-details-title-group">
            <h1>{tripData.title}</h1>
          </div>

          <div className="trip-details-meta">
            <div className="trip-details-meta-item">
              <span className="trip-details-label">Destination</span>
              <p>{tripData.destination}</p>
            </div>
            <div className="trip-details-meta-item">
              <span className="trip-details-label">Dates</span>
              <p>{tripData.start_date} – {tripData.end_date}</p>
            </div>
          </div>
        </header>

        <div className="tab-buttons">
          <button className={activeTab === 1 ? "active-tab" : ""} onClick={() => updateTabs(1)}>
            Overview
          </button>
          <button className={activeTab === 2 ? "active-tab" : ""} onClick={() => updateTabs(2)}>
            Checklists
          </button>
          <button className={activeTab === 3 ? "active-tab" : ""} onClick={() => updateTabs(3)}>
            Itinerary
          </button>
        </div>
      {/* </div> */}

    {/* overview */}
      <div className={activeTab === 1 ? "show-content" : "content"}>
        <div className={"trip-details-content"}>
          <section className="trip-details-card">
            <h2>Description</h2>
            <p>{tripData.description || "No description yet."}</p>
          </section>

          <section className="trip-details-card">
            <h2>Notes</h2>
            <p>{tripData.notes || "No notes yet."}</p>
          </section>
        </div>
      </div>

    {/* checklists */}
      <div className={activeTab === 2 ? "show-content" : "content"}>
        <div className="trip-checklists">
          < ChecklistSection 
          tripId={trip_id}
          checklists={tripData.checklists}
          onChecklistCreated={handleChecklistCreated}
          onChecklistUpdated={handleChecklistUpdated}
          onChecklistDeleted={handleChecklistDeleted}
          onItemCreated={handleItemCreated}
          onItemChanged={handleItemChanged}
          onItemDeleted={handleItemDeleted}
          />
        </div>
      </div>

    {/* itinerary */}
      <div className={activeTab === 3 ? "show-content" : "content"}>
        <div className="trip-itinerary">
          {/* {tripData.itinerary_items.length === 0 ? (
            <p className="trip-empty-state">No itinerary yet.</p>
          ) : (
              tripData.itinerary_items.map(item => (
              <div key={item.id} className="trip-itinerary-card">
                <h3>{item.activity}</h3>
                <p className="trip-itinerary-day">{item.day}</p>
                <p className="trip-itinerary-time">{item.start_time} - {item.end_time}</p>
              </div>
            ))
          )} */}
          <ItinerarySection 
            tripId={trip_id}
            itineraryItems={tripData.itinerary_items}
            onItineraryItemCreated={handleItineraryItemCreated}
            onItineraryItemUpdated={handleItineraryItemUpdated}
            onItineraryItemDeleted={handleItineraryItemDeleted}/>
        </div>
      </div>
    </div>
  )
}