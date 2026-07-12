from random import choice, randint
from datetime import timedelta, time

from config import app, db
from faker import Faker
from models import User, Trip, CheckList, CheckListItem, ItineraryItem, Status

with app.app_context():

  print("Clearing database...")
  # delete children before parents since some columns are non-nullable
  # (cascades handle this too, but being explicit keeps order obvious)
  CheckListItem.query.delete()
  CheckList.query.delete()
  ItineraryItem.query.delete()
  Trip.query.delete()
  User.query.delete()
  db.session.commit()

  print("Seeding database...")

  # create and initialize faker generator
  fake = Faker()

  # a small pool of realistic checklist item names to pull from,
  # since fake words wouldn't read like real packing/planning items
  packing_items = [
    "Passport", "Phone charger", "Toothbrush", "Sunglasses", "Swimsuit",
    "Hiking boots", "Rain jacket", "Camera", "Travel adapter", "Medication",
    "Sunscreen", "Reusable water bottle", "Headphones", "Laptop", "Snacks"
  ]

  activities = [
    "Flight departure", "Hotel check-in", "City walking tour", "Museum visit",
    "Beach day", "Dinner reservation", "Hiking excursion", "Local market visit",
    "Boat tour", "Spa afternoon", "Train to next city", "Sightseeing bus tour"
  ]

  users = []

  for n in range(12):
    user = User(
      username=fake.unique.user_name(),
      email=fake.unique.email()
    )
    # password_hash is a setter that hashes whatever plaintext you assign it
    user.password_hash = fake.password(length=10)
    users.append(user)

  db.session.add_all(users)
  db.session.commit()

  trips = []

  for user in users:
    # each user gets 1-3 trips
    for _ in range(randint(1, 3)):
      start_date = fake.date_between(start_date="-1y", end_date="+1y")
      end_date = start_date + timedelta(days=randint(2, 14))

      trip = Trip(
        title=f"Trip to {fake.city()}",
        description=fake.sentence(nb_words=12),
        destination=fake.city(),
        start_date=start_date,
        end_date=end_date,
        notes=fake.paragraph(nb_sentences=2),
        user_id=user.id
      )
      trips.append(trip)

  db.session.add_all(trips)
  db.session.commit()

  checklists = []
  checklist_items = []
  itinerary_items = []

  for trip in trips:
    # each trip gets 1-2 checklists (e.g. "Packing List", "Documents")
    for checklist_title in fake.random_elements(
      elements=("Packing List", "Documents", "Shopping List", "To-Do Before Leaving"),
      length=randint(1, 2),
      unique=True
    ):
      checklist = CheckList(
        title=checklist_title,
        trip_id=trip.id
      )
      checklists.append(checklist)
      db.session.add(checklist)
      db.session.flush()  # assigns checklist.id without a full commit

      # each checklist gets 3-7 items
      for item_name in fake.random_elements(elements=packing_items, length=randint(3, 7), unique=True):
        checklist_items.append(CheckListItem(
          item_name=item_name,
          status=choice(list(Status)),
          checklist_id=checklist.id
        ))

    # each trip gets 3-6 itinerary items spread across its date range
    trip_length = (trip.end_date - trip.start_date).days or 1
    for _ in range(randint(3, 6)):
      day_offset = randint(0, trip_length)
      day = trip.start_date + timedelta(days=day_offset)

      # build start/end times directly so end_time is guaranteed to be after start_time
      start_hour = randint(6, 20)
      duration_hours = randint(1, 3)
      start_time = time(hour=start_hour, minute=choice([0, 15, 30, 45]))
      end_time = time(hour=min(start_hour + duration_hours, 23), minute=start_time.minute)

      itinerary_items.append(ItineraryItem(
        activity=choice(activities),
        start_time=start_time,
        end_time=end_time,
        day=day,
        trip_id=trip.id
      ))

  db.session.add_all(checklist_items)
  db.session.add_all(itinerary_items)
  db.session.commit()

  print(f"Seeded {len(users)} users, {len(trips)} trips, "
        f"{len(checklists)} checklists ({len(checklist_items)} items), "
        f"{len(itinerary_items)} itinerary items.")