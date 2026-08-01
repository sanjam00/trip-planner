import { NavLink } from "react-router"
import "../../styles/Navbar.css"

export default function NavBar() {

  return (
    <nav className="navbar">

      <div className="nav-icons">
        <NavLink to='/trips/new'>
          ➕
        </NavLink>

        <NavLink to='/trips' id="site-name" style={{ fontSize: '2em'}}>
          B
        </NavLink>

        <NavLink to='/whoami'>
          🚹
        </NavLink>
      </div>

    </nav>
  )
}