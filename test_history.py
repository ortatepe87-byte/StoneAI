from core.database import db

rows = db.get_last_analyses()

for row in rows:
    print(row)