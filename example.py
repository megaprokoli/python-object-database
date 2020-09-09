from PyObjDB.python_object_database import PyObjDatabase

import time
import random

# Create database
db = PyObjDatabase(db_dir="db", name="obj_db")
db.create()

# Clear database
# db.clear_table("test")
# db.commit()

# Add table
db.add_table("test")

# Add elements to table
start = time.time()

for i in range(10):
    db.add("test", list(range(random.randint(1, 10))))

db.commit()
print("Added in", time.time() - start)

# Print the table with filter
start = time.time()

print(db.get("test", filter_func=lambda o: len(o) > 3))
print("Get in", time.time() - start)
