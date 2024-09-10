import sys
sys.path.append('c:/Users/HP/Desktop/Password-Generator')

from datetime import datetime
import psycopg2
from fastapi import FastAPI, HTTPException
import hashlib
from ValidPass import is_strong_password
from PydanticFile import UserCreate
from db import connect_db , create_users_table

app = FastAPI()

create_users_table()


@app.post("/signup")
async def create_account(user: UserCreate):
    username = user.username
    password = user.password

    if not is_strong_password(password):
        raise HTTPException(
            status_code = 400,
            detail = "Password must be atleast 8 characters long, contain an uppercase letter, a lower case letter , a digit and a special character"
        )
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    created_at = datetime.now()

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users(username, password, created_at) VALUES(%s,%s,%s)",(username,hashed_password,created_at))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Usernae alraedy exists.Please Choose another one.")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Account Created Successfully!"}