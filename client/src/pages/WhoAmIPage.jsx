import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../api/api";
import "../styles/WhoAmIPage.css";

export default function WhoAmIPage(){
  const [userData, setUserData] = useState({ username: "", email: "" });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  useEffect(() => {
    setLoading(true);
    apiFetch(`/whoami`, token)
      .then(data => {
        setUserData(data);
        console.log(data);
      })
      .catch(err => {
        setError(err.message)
        console.error(err)
      })
      .finally(() => setLoading(false));
  }, [token])

  return(
    <div className="whoami-page">
      <div className="whoami-card">
        <div className="whoami-avatar">
          <img
            id="placeholder-img"
            src="https://placehold.net/avatar.png"
            alt="Profile photo"
          />
        </div>

        <div className="whoami-info">
          <h2>{userData.username || "Your profile"}</h2>
          <p>{userData.email || "email"}</p>
        </div>
      </div>
    </div>
  )
}