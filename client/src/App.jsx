
import { BrowserRouter, Routes, Route} from 'react-router'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import TripsPage from './pages/TripsPage'
import ProtectedRoute from './components/ProtectedRoute'

export default function App(){

  return(
    <BrowserRouter>
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
      </Routes>
    </BrowserRouter>
  )
}