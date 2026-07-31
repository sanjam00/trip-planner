# Trip Planner

A full-stack web app for planning trips, catering to outdoor trips such as camping. Create trips, build packing/to-do checklists, and schedule itinerary items, all scoped to your own account.

## Features

- **User authentication** — signup/login with JWT-based sessions
- **Trips** — create, view, edit, and delete trips (title, destination, dates, description, notes)
- **Checklists** — add multiple checklists per trip (e.g. "Packing List," "Documents"), each with its own items
- **Checklist items** — add items to a checklist and toggle their status (`packed` and `not packed`)
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
├── client/ (or project root, depending on setup) 
    ├── dist/
    ├── node_modules/
    ├── public/
    ├── src/
        ├── api/
            └── api.js            # fetch wrapper, attaches Authorization header
        ├── components/
            ├── checklists/       # ChecklistSection, ChecklistCard, ChecklistForm, ChecklistItemRow, ChecklistItemForm
            ├── itinerary/        # ItinerarySection, ItineraryItemCard, ItineraryItemForm
            ├── layout/           # Navbar, ProtectedRoute
            └── trips/            # TripCard, TripEditForm
        ├── context/
            └── AuthContext.jsx   # holds token/user, exposes login/signup/logout
        ├── fonts/                # custom fonts
        ├── pages/
            ├── LoginPage.jsx
            ├── NotFoundPage.jsx
            ├── SignupPage.jsx
            ├── TripDetailsPage.jsx
            ├── TripFormPage.jsx
            ├── TripsPage.jsx
            └── WhoAmIPage.jsx
        ├── styles/               # styling for all pages and components
        ├── utils/
            └── dateTime.js       # formats ISO dates/times for display vs. API
        ├── App.css
        ├── App.jsx               # holds BrowserRouter
        ├── index.css             # universal styles and variables
        └── main.jsx
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── vite.config.jsx
├── server/
    ├── __pycache__/
    ├── controllers/
        ├── __init__.py
        ├── CheckListIndex.py / CheckListById.py
        ├── CheckListItemIndex.py / CheckListItemById.py
        ├── ItineraryItemIndex.py / ItineraryItemById.py
        ├── Signup.py / Login.py / WhoAmI.py
        └── TripIndex.py / TripById.py
    ├── instance/
        └── app.db                # database
    ├── migrations/               # Alembic migration history
    ├── models/
        ├── schemas/              # Marshmallow schemas
        ├── __init__.py
        ├── CheckList.py
        ├── CheckListItem.py
        ├── ItineraryItem.py
        ├── Trip.py
        ├── User.py
    ├── app.py                    # route registration
    ├── config.py                 # Flask app, db, jwt, bcrypt, api setup
    ├── seed.py                   # populates the db with fake data (Faker)
    └── requirements.txt
├── README.md
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

## Known Limitations

- Token is stored in memory only — refreshing the page currently logs the user out (a candidate for persisting to `localStorage` or adding refresh tokens)
- No image/photo support for trips yet
- No collaborative/shared trips between multiple users
- No timezone handling for itinerary times (assumes local time)
- No navigation buttons to navigate back from a trip to trip board
- Error handling is not user friendly

## Future Improvements

- Social features including collaboration on trips, direct-messaging, following/followers, etc.
- Map features such as displaying location for a trip, searching locations, and popular locations with reviews
- Budget section for a trip
- Weather features that notify user regarding bad weather
- Currency exchange
- Calendar displaying the dates of all trips
- Sorting and search of trips
- Test suites

## License

This project was built as a capstone project for Flatiron School's Software Engineering course and is not currently licensed for reuse.

## Author

Sanaeya James