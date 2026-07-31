# Trip Planner

A full-stack web app for planning trips — create trips, build packing/to-do checklists, and schedule itinerary items, all scoped to your own account.

## Features

- **User authentication** — signup/login with JWT-based sessions
- **Trips** — create, view, edit, and delete trips (title, destination, dates, description, notes)
- **Checklists** — add multiple checklists per trip (e.g. "Packing List," "Documents"), each with its own items
- **Checklist items** — add items to a checklist and toggle their status (`packed`, `not packed`, `planned`)
- **Itinerary** — schedule activities per trip with a date, start time, and end time
- All trip data (checklists, checklist items, itinerary items) is scoped to the trip's owner — users can only see and modify their own trips

## Tech Stack

**Backend**
- Flask + Flask-RESTful
- SQLAlchemy + Flask-Migrate (Alembic)
- Flask-JWT-Extended for authentication
- Flask-Bcrypt for password hashing
- Marshmallow for serialization
- SQLite (dev)

**Frontend**
- React (Vite)
- React Router
- Fetch-based API layer with a shared auth-aware wrapper

## Project Structure

```
trip-planner/
├── server/
│   ├── config.py                # Flask app, db, jwt, bcrypt, api setup
│   ├── app.py                   # route registration
│   ├── seed.py                  # populates the db with fake data (Faker)
│   ├── models/
│   │   ├── User.py
│   │   ├── Trip.py
│   │   ├── CheckList.py
│   │   ├── CheckListItem.py     # includes the Status enum
│   │   ├── ItineraryItem.py
│   │   └── schemas/             # Marshmallow schemas
│   ├── controllers/
│   │   ├── Signup.py / Login.py / WhoAmI.py
│   │   ├── TripIndex.py / TripById.py
│   │   ├── CheckListIndex.py / CheckListById.py
│   │   ├── CheckListItemIndex.py / CheckListItemById.py
│   │   └── ItineraryItemIndex.py / ItineraryItemById.py
│   └── migrations/               # Alembic migration history
│
└── client/ (or project root, depending on setup)
    └── src/
        ├── api/
        │   └── api.js            # fetch wrapper, attaches Authorization header
        ├── context/
        │   └── AuthContext.jsx   # holds token/user, exposes login/signup/logout
        ├── utils/
        │   └── dateTime.js       # formats ISO dates/times for display vs. API
        ├── components/
        │   ├── layout/           # Navbar, ProtectedRoute
        │   ├── trips/            # TripCard, TripForm, TripEditForm
        │   ├── checklists/       # ChecklistSection, ChecklistCard, ChecklistForm, ChecklistItemRow, ChecklistItemForm
        │   └── itinerary/        # ItinerarySection, ItineraryCard
        └── pages/
            ├── LoginPage.jsx / SignupPage.jsx
            ├── TripsPage.jsx
            └── TripDetailsPage.jsx
```

## Getting Started

### Backend setup

```bash
cd server
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `server/` with:
```
JWT_SECRET_KEY=your-secret-key-here
```

Run migrations and start the server:
```bash
flask db upgrade
flask run --debug
```

The API runs at `http://127.0.0.1:5000` by default.

**Optional: seed the database with sample data**
```bash
python seed.py
```
This clears existing data and generates fake users, trips, checklists, checklist items, and itinerary items using Faker — useful for testing without manually creating records.

### Frontend setup

```bash
npm install
npm run dev
```

The app runs at `http://localhost:5173` by default (Vite's default port).

## API Overview

All routes except `/signup` and `/login` require a `Authorization: Bearer <token>` header.

| Method | Route | Description |
|---|---|---|
| POST | `/signup` | Create a new user, returns token |
| POST | `/login` | Authenticate, returns token |
| GET | `/whoami` | Returns the currently logged-in user |
| GET, POST | `/trips` | List / create trips |
| GET, PATCH, DELETE | `/trips/<id>` | Read / update / delete a trip |
| GET, POST | `/trips/<trip_id>/checklists` | List / create checklists for a trip |
| GET, PATCH, DELETE | `/trips/<trip_id>/checklists/<id>` | Read / update / delete a checklist |
| POST | `/trips/<trip_id>/checklists/<checklist_id>/checklist-items` | Add an item to a checklist |
| PATCH, DELETE | `/trips/<trip_id>/checklists/<checklist_id>/checklist-items/<id>` | Update / delete a checklist item |
| GET, POST | `/trips/<trip_id>/itinerary-items` | List / create itinerary items for a trip |
| GET, PATCH, DELETE | `/trips/<trip_id>/itinerary-items/<id>` | Read / update / delete an itinerary item |

### Notable formatting conventions

- **Dates** are sent/received as ISO 8601 strings: `YYYY-MM-DD`
- **Times** are sent/received as `HH:MM:SS`
- The frontend converts these to locale-friendly display formats (e.g. "July 31, 2026," "2:30 PM") only at render time — all state and API calls stay in ISO format
- **Checklist item status** values are `packed`, `not packed`, `planned` (matches the `Status` enum's *value*, not its Python name)

## Authentication Flow

1. User submits signup or login form
2. Backend returns a JWT (`token`) and the user object
3. Frontend stores both in `AuthContext` (React state, not persisted across reloads by default)
4. Every subsequent authenticated request attaches `Authorization: Bearer <token>` via the shared `apiFetch` wrapper
5. `ProtectedRoute` redirects unauthenticated users to `/login` before they can reach trip pages

## Known Limitations / Future Improvements

- Token is stored in memory only — refreshing the page currently logs the user out (a candidate for persisting to `localStorage` or adding refresh tokens)
- No image/photo support for trips yet
- No collaborative/shared trips between multiple users
- No timezone handling for itinerary times (assumes local time)

## License

This project was built as a capstone project and is not currently licensed for reuse.