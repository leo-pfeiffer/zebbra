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
            {
                "username": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Babish",
                "workspaces": ["Boring Co."],
                "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
                "disabled": False,
            },
            {
                "username": "charlie@example.com",
                "first_name": "Charlie",
                "last_name": "Carlson",
                "workspaces": ["ACME Inc."],
                "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
                "disabled": False,
            },
            {
                "username": "darwin@example.com",
                "first_name": "Darwin",
                "last_name": "Dobson",
                "workspaces": ["ACME Inc."],
                "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
                "disabled": False,
            },
            {
                "username": "zeus@example.com",
                "first_name": "Zeus",
                "last_name": "Olympus",
                "workspaces": ["ACME Inc."],
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


def create_model_data():
    return db.models.insert_many(
        [
            {
                "_id": "62b488ba433720870b60ec0a",
                "meta": {
                    "name": "model1",
                    "admin": "johndoe@example.com",
                    "editors": ["darwin@example.com"],
                    "viewers": ["charlie@example.com"],
                    "workspace": "ACME Inc.",
                },
                "data": [
                    {
                        "meta": {"name": "sheet1"},
                        "data": [
                            {
                                "assumptions": [
                                    {
                                        "name": "Initial Customers",
                                        "valType": "number",
                                        "editable": True,
                                        "data": {
                                            "varType": "manual",
                                            "data": {
                                                "column1": 100,
                                            },
                                        },
                                    }
                                ],
                                "model": {
                                    "category": "Growth",
                                    "rows": [
                                        {
                                            "name": "New customers",
                                            "valType": "number",
                                            "editable": True,
                                            "data": {
                                                "varType": "manual",
                                                "data": {
                                                    "column1": 10,
                                                    "column2": 20,
                                                    "column3": 25,
                                                },
                                            },
                                        }
                                    ],
                                    "end_row": {
                                        "name": "Total customers",
                                        "valType": "number",
                                        "editable": True,
                                        "data": {
                                            "varType": "manual",
                                            "data": {
                                                "column1": 110,
                                                "column2": 130,
                                                "column3": 155,
                                            },
                                        },
                                    },
                                },
                            }
                        ],
                    }
                ],
            },
            {
                "_id": "62b488ba433720870b60ec0b",
                "meta": {
                    "name": "model1",
                    "admin": "alice@example.com",
                    "editors": ["alice@example.com"],
                    "viewers": ["bob@example.com"],
                    "workspace": "Boring Co.",
                },
                "data": [
                    {
                        "meta": {"name": "sheet1"},
                        "data": [
                            {
                                "assumptions": [
                                    {
                                        "name": "Initial Customers",
                                        "valType": "number",
                                        "editable": True,
                                        "data": {
                                            "varType": "manual",
                                            "data": {
                                                "column1": 100,
                                            },
                                        },
                                    }
                                ],
                                "model": {
                                    "category": "Growth",
                                    "rows": [
                                        {
                                            "name": "New customers",
                                            "valType": "number",
                                            "editable": True,
                                            "data": {
                                                "varType": "manual",
                                                "data": {
                                                    "column1": 10,
                                                    "column2": 20,
                                                    "column3": 25,
                                                },
                                            },
                                        }
                                    ],
                                    "end_row": {
                                        "name": "Total customers",
                                        "valType": "number",
                                        "editable": True,
                                        "data": {
                                            "varType": "manual",
                                            "data": {
                                                "column1": 110,
                                                "column2": 130,
                                                "column3": 155,
                                            },
                                        },
                                    },
                                },
                            }
                        ],
                    }
                ],
            },
        ]
    )


def teardown_users():
    return db.users.delete_many({})


def teardown_workspaces():
    return db.workspaces.delete_many({})


def teardown_token_blacklist():
    return db.token_blacklist.delete_many({})


def teardown_models():
    return db.models.delete_many({})
