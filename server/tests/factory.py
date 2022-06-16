# test object factory
from core.models.database import db


def create_demo_data():
    return db["users"].insert_many([
        {
            "username": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "workspace": "ACME Inc.",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
            "disabled": False
        },
        {
            "username": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Wonderson",
            "workspace": "Boring Co.",
            "email": "alice@example.com",
            "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
            "disabled": False
        }
    ])


def teardown():
    return db["users"].delete_many({})
