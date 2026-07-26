import { NavLink } from "react-router"
// import "./NavBar.css"

export default function NavBar() {

  return (
    <nav className="navbar">

      <div className="nav-icons">
        <NavLink to='/trips'>
          Trips Page📗
        </NavLink>

        <NavLink to='/trips/new'>
          New Trip ➕
        </NavLink>

        <NavLink to='/whoami'>
          Profile 🚹
        </NavLink>
      </div>

    </nav>
  )
}