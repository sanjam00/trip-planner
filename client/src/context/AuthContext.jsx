
// where the token actually lives
import { createContext, useContext, useState } from "react";
import { apiFetch } from "../api/api";

const AuthContext = createContext(null);

export function AuthProvider({children}) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);

  async function login(username, password) {
    const date = await apiFetch('/login', null, {
      method: 'POST',
      body: JSON.stringify({username, password}),
    });
    setToken(data.token);
    setUser(data.user);
  }

  function logout() {
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout }} >
      {children}
    </AuthContext.Provider>
  );
}

export function userAuth() {
  return useContext(AuthContext);
}