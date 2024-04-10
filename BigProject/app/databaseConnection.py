# Connecting my api to a database
# Create a folder called app, rename program into main.py and add an empty file called __init__.py
# download Postgre
# add id and created_at column (timestamp_with_timezone / constraints now()) to the tables and see if they should be deleted from the model
# install and import psycopg https://www.psycopg.org/

import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Keep the CLASSES between the libraries and database connection

while True:

		try:
				# data needs to be consistent with the Postgre configuration
				conn = psycopg2.conn(host='localhost', database='VynilRecordCollectorAPI', user='AndreaCi', password='Forzalazio1!', cursor_factory=RealDictCursor)
				# pass the user and password through variables referring to a config file
				cursor = conn.cursor()
				print("Database connection was successfull!")
				break
		except Exception as error:
				print("Connect to database failed!")
				print("Error: ", error)
				time.sleep(2)
				
				
# To get ALL USERS
cursor.execute("""SELECT * FROM users """)
users = cursor.fetchall()
print(users) # users can be inserted into the return statement and th print statement can be deleted

# To get ALL RECORDS
cursor.execute("""SELECT * FROM records """)
records = cursor.fetchall()
print(records) # records can be inserted into the return statement and th print statement can be deleted

# To get ONE USER by ID
cursor.execute("""SELECT * FROM users WHERE ID =%s """,(str(id),)
user = cursor.fetchone()
if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
return {"data": user}

# To get ONE RECORD by ID
cursor.execute("""SELECT * FROM records WHERE ID =%s """,(str(id))
user = cursor.fetchone()
if not record:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with id: {id} was not found")
return {"data": record}

# To POST a new user
cursor.execute("""INSERT INTO users ("type all columns") VALUES (%s, %s ("variable for each column") RETURNING *)""", 
							(user.name, user.lastname ("for each column name")))
new_user = cursor.fetchone()
conn.commit()
return {"data": new_user)

# To POST a new record
cursor.execute("""INSERT INTO records ("type all columns") VALUES(%s, %s ("variable for each column") RETURNING *)""", 
							(record.title, record.lable ("for each column name")))
new_record = cursor.fetchone()
conn.commit()
return {"data": new_record)

# To UPDATE a user's details
cursor.execute("""UPDATE users SET first_name =%s, last_name=%s, email=%s ("and all the rest") WHERE id =%s RETURNING *""", (user.first_name, user.last_name, user.email), str(id)))
updated_user= cursor.fetchone()
conn.commit()
if updated_user == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
return {"data": updated_user}

# To UPDATE a record's details
cursor.execute("""UPDATE records SET title =%s, lable=%s, condition=%s ("and all the rest") WHERE id =%s RETURNING *""", (record.title, record.lable, record.condition), str(id)))
updated_record= cursor.fetchone()
conn.commit()
if updated_record == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with id: {id} was not found")
return {"data": updated_record}

# To DELETE a user by ID
cursor.execute("""DELETE FROM users WHERE ID =%s RETURNING *""",(str(id),)
deleted_user = cursor.fetchone()
conn.commit()
if deleted_user == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
return {"data": deleted_user}

# To DELETE a record by ID
cursor.execute("""DELETE FROM records WHERE ID =%s RETURNING *""",(str(id),)
deleted_record = cursor.fetchone()
conn.commit()
if deleted_record == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with id: {id} was not found")
return {"data": deleted_record}
