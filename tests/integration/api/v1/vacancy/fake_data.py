import random

from faker import Faker

faker = Faker()
sectors = [
    "RH",
    "IT",
    "Commercial",
    "Logistics",
    "Finance",
    "Marketing",
    "Operations",
    "Legal",
]
periods = ["ANNUAL", "MONTHLY"]


def generate_fake_vacancy_data():
    payload = {
        "description": faker.text(10),
        "sector": random.choice(sectors),
        "manager": faker.name(),
        "salary_expectation": faker.pyfloat(
            left_digits=5, right_digits=2, positive=True
        ),
        "urgency": random.randint(0, 2),
        "status": random.choice(["IN_PROGRESS", "FINISHED", "CANCELED"]),
        "start_date": faker.iso8601(),
        "end_date": None,
        "notes": faker.text(10),
    }

    return payload


def generate_fake_data_simulation_input():
    payload = {"sector": random.choice(sectors), "period": random.choice(periods)}

    return payload
