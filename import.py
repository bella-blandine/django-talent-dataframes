import random
import psycopg2
from faker import Faker


fake = Faker()


DB_NAME = 'talentsy'
DB_USER = 'postgres'
DB_PASSWORD = 'jmn11bbl'
DB_HOST = 'localhost'
DB_PORT = '5433'


NUM_AUDITIONS = 500000
NUM_PERFORMANCES = 500000


try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    cursor = conn.cursor()
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()


try:
    cursor.execute("""
        INSERT INTO judge_judge (id, name) 
        VALUES (1, 'Judge 1')
        ON CONFLICT (id) DO NOTHING;
    """)
    print("Judge table populated with required entry.")
except Exception as e:
    print(f"Error populating judges: {e}")


try:
    for _ in range(NUM_AUDITIONS):
        title = fake.catch_phrase()
        description = fake.text(max_nb_chars=200)
        judge_id = 1  
        cursor.execute(
            """
            INSERT INTO judge_audition (title, description, judge_id)
            VALUES (%s, %s, %s)
            """,
            (title, description, judge_id),
        )
    print(f"{NUM_AUDITIONS} dummy auditions inserted successfully.")
except Exception as e:
    print(f"Error inserting auditions: {e}")


try:
   
    cursor.execute("SELECT id FROM judge_audition")
    audition_ids = [row[0] for row in cursor.fetchall()]

    if not audition_ids:
        print("No auditions found in the database. Cannot insert performances.")
    else:
        for _ in range(NUM_PERFORMANCES):
            performer_id = random.choice([1, 2])  
            audition_id = random.choice(audition_ids)  
            score = random.randint(0, 100)  
            cursor.execute(
                """
                INSERT INTO judge_performance (performer_id, audition_id, score)
                VALUES (%s, %s, %s)
                """,
                (performer_id, audition_id, score),
            )
        print(f"{NUM_PERFORMANCES} dummy performances inserted successfully.")
except Exception as e:
    print(f"Error inserting performances: {e}")


try:
    conn.commit()
    print("Changes committed to the database.")
except Exception as e:
    print(f"Error committing changes: {e}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
