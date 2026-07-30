// converting backend ISO strings to user-friendly formats

// ---- DISPLAY: API format → user-friendly ----

// "2026-07-31" -> "July 31, 2026"
export function formatDateForDisplay(isoDate) {
  if (!isoDate) return '';
  const date = new Date(`${isoDate}T00:00:00`); // avoid timezone shift
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

// "14:30:00" -> "2:30 PM"
export function formatTimeForDisplay(isoTime) {
  if (!isoTime) return '';
  const [hours, minutes] = isoTime.split(':');
  const date = new Date();
  date.setHours(Number(hours), Number(minutes));
  return date.toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  });
}

// ---- SENDING: <input> value → API format ----

// <input type="time"> gives "14:30" (no seconds) — API needs "14:30:00"
export function timeInputToApiFormat(inputValue) {
  if (!inputValue) return '';
  return inputValue.length === 5 ? `${inputValue}:00` : inputValue;
}

// <input type="date"> already gives "2026-07-31" — API-ready as-is
export function dateInputToApiFormat(inputValue) {
  return inputValue;
}