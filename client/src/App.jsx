
import { BrowserRouter, Routes, Route} from 'react-router'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import TripsPage from './pages/TripsPage'
import ProtectedRoute from './components/layout/ProtectedRoute'
import NavBar from './components/layout/Navbar'
import TripForm from './pages/TripFormPage'
import TripDetailsPage from './pages/TripDetailsPage'
import { useAuth } from './context/AuthContext'
import NotFoundPage from './pages/NotFoundPage'

export default function App(){
  const { token } = useAuth()

  return(
    <BrowserRouter>
      {token ? <NavBar /> : null}
      <div className="app-shell">
      <Routes>
        < Route path="/*" element={<NotFoundPage />} />
        < Route path="/login" element={ <LoginPage /> } />
        < Route path="/signup" element={ <SignupPage /> } />
        {/* < Route element={<ProtectedRoute />}>
          <Route path="/trips" element={<TripsPage />}/>
        </Route> */}
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
        < Route
          path="/trips/:trip_id"
          element={
            <ProtectedRoute>
              <TripDetailsPage />
            </ProtectedRoute>
          }
        />
      </Routes>
      </div>
    </BrowserRouter>
  )
}