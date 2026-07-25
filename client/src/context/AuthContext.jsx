
// where the token actually lives
// api calls go through useAuth when they need to update global state (such as logins)
  // but one offs (like TripsPage) don't need to update gloabal state, so they go directly to apiFetch in api.js
import { createContext, useContext, useState } from "react";
import { apiFetch } from "../api/api";

const AuthContext = createContext(null);

export function AuthProvider({children}) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);

  async function login(username, password) {
    const data = await apiFetch('/login', null, {
      method: 'POST',
      body: JSON.stringify({username, password}),
    });
    setToken(data.token);
    setUser(data.user);
  }

  async function signup(username, email, password, passwordConfirmation) {
    const data = await apiFetch('/signup', null, {
      method: 'POST',
      body: JSON.stringify({
        username,
        email,
        password,
        password_confirmation: passwordConfirmation,
      }),
    });
    setToken(data.token);
    setUser(data.user);
  }

  function logout() {
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ token, user, login, signup, logout }} >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}