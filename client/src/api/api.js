
// fetch wrapper with auth header

const BASE_URL = 'http://127.0.0.1:5000'

export async function apiFetch(endpoint, token, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ... options,
    headers: {
      'Content-Type': 'application/json',
      ... (token && {'Authorization': `Bearer ${token}`}),
      ... options.headers,
    }
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message =
      errorData.error ||
      errorData.errors?.[0] ||
      `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  // handle 204 No Content or empty bodies gracefully
  const text = await response.text();
  return text ? JSON.parse(text) : null;

}