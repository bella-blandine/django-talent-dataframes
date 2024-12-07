import csv
import random
from faker import Faker
from datetime import datetime
fake = Faker()
num_records = 500000
output_file = "members_dataset.csv"
data = [
    {
        "title": fake.catch_phrase(),
        "name": fake.name(),
        "date": fake.date_between(start_date='-2y', end_date='today'),
        "location": fake.city(),
        "description": fake.text(max_nb_chars=200),
        "created_at": fake.date_time_this_year(),
    }
    for _ in range(num_records)
]
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "name", "date", "location", "description", "created_at"])
    writer.writeheader()
    writer.writerows(data)
print(f"Dataset with {num_records} records saved to {output_file}.")




