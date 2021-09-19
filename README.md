# Python-Object-Database
Python-Object-Database is a simple database that can store python objects.
This is meant to be used as local database for small data sets<br>

**Disclaimer:** This is a students project and may or may not be useful. Feedback is welcome.
## Basic usage
### Creating a new database
To create a database you need to create a database object and provide it a 
directory to place the database files in and a name. After that you can run the
create method.
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")
db.create()
```
### Committing and reverting
In order to save changes you made to the filesystem, you need to commit. 
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")

db.add_table(table_name="table1")
db.commit()
```
In case something went wrong, you can revert all changes made since the
last commit.
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")

db.add_table(table_name="table1")
db.revert()
```
### Adding and deleting tables
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")

# Add
db.add_table(table_name="table1")
db.commit()

# Delete
db.delete_table(table_name="table1")
db.commit()
```
### Adding and deleting elements
**Note:** you can't store duplicate objects. They will be overwritten.
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")
obj = [1, 2, 3]

# Add
db.add(table_name="table1", obj=obj)
db.commit()

# Delete
# deleting by id
db.delete(table_name="table1", row_id="77667533ff2d4961a8ad3b35d7d8801f")
db.commit()

# deleting by filter (delete every element with length 3)
db.delete(table_name="table1", filter_func=lambda o: len(o) == 3)
db.commit()
```
### Updating elements
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")
obj = [1, 2]

# Updating by id
db.update(table_name="table1", new_obj=obj, row_id="77667533ff2d4961a8ad3b35d7d8801f")
db.commit()

# Updating by filter
db.update(table_name="table1", new_obj=obj, filter_func=lambda o: len(o) == 3)
db.commit()
```
### Clearing tables
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")

db.clear_table(table_name="table1")
db.commit()
```
### Getting elements
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")

# Getting all elements
elems = db.get(table_name="table1")

# Getting a element by id 
elems = db.get(table_name="table1", row_id="77667533ff2d4961a8ad3b35d7d8801f")

# Getting elements by filter
elems = db.get(table_name="table1", filter_func=lambda o: len(o) == 3)
```
### Object existence
```python
from PyObjDB.python_object_database import PyObjDatabase

db = PyObjDatabase(db_dir="db", name="obj_db")

if db.obj_exists("table1", some_obj):
    do_something()
```
### Encryption
You can encrypt your database by providing a key to the database object.<br>
**Note:** Don't forget to save your key!
```python
from PyObjDB.python_object_database import PyObjDatabase
import PyObjDB.helpers.encryption as crypto

crypt_key = crypto.generate_key()
db = PyObjDatabase(db_dir="db", name="obj_db", crypt_key=crypt_key)
```
## Filter function
Filter functions must have the following signature:
```python
def filter_function(obj: object) -> bool:
    pass
```