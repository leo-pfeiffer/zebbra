# test object factory
from core.dao.database import db


def create_user_data():
    return db.users.insert_many(
        [
            {
                "username": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspaces": ["ACME Inc."],
                "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
                "disabled": False,
            },
            {
                "username": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Wonderson",
                "workspaces": ["Boring Co."],
                "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
                "disabled": False,
            },
        ]
    )


def create_workspace_data():
    return db.workspaces.insert_many(
        [
            {
                "name": "ACME Inc.",
                "admin": "johndoe@example.com",
                "users": ["johndoe@example.com"],
            },
            {
                "name": "Boring Co.",
                "admin": "alice@example.com",
                "users": ["alice@example.com"],
            },
        ]
    )


def teardown_users():
    return db.users.delete_many({})


def teardown_workspaces():
    return db.workspaces.delete_many({})


def teardown_token_blacklist():
    return db.token_blacklist.delete_many({})
