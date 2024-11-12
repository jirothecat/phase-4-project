#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, BubbleTea

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        BubbleTea.query.delete()

        bubble_tea_1 = BubbleTea(franchise="Molly Tea", image="https://s3-media0.fl.yelpcdn.com/bphoto/pqQdxJYmf2l9hIeEXaHVCQ/348s.jpg", price="$6.79", topping="Tapioca", location="Flushing")

        db.session.add_all([bubble_tea_1])
        db.session.commit()

        print("Seeded database.")