# from app import app
from config import db
from faker import Faker
from models import User, Trip, CheckList, CheckListItem, ItineraryList, ItineraryItem


with app.app_context():

  print("Clearing database...")
  User.query.delete()
  Trip.query.delete()
  CheckList.query.delete()
  CheckListItem.query.delete()
  ItineraryList.query.delete()
  ItineraryItem.query.delete()

  print("Seeding database...")

  # create and initialize faker generator
  fake = Faker()

  users = []

  for n in range(12):
    user = User(
      username=fake.name(), 
      email=fake.email()
      )
    users.append(user)

  db.session.add_all(users)
  db.session.commit()