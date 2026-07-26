
import { BrowserRouter, Routes, Route} from 'react-router'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import TripsPage from './pages/TripsPage'
import ProtectedRoute from './components/ProtectedRoute'
import NavBar from './components/Navbar'
import TripForm from './pages/TripFormPage'

export default function App(){

  return(
    <BrowserRouter>
      <NavBar />
      <Routes>
        < Route path="/login" element={ <LoginPage /> } />
        < Route path="/signup" element={ <SignupPage /> } />
        < Route 
          path="/trips"
          element={
            <ProtectedRoute>
              <TripsPage />
            </ProtectedRoute>
          } 
        />
        < Route
          path="/trips/new"
          element={
            <ProtectedRoute>
              <TripForm />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}