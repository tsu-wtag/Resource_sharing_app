from fastapi import FastAPI
from fastapi import HTTPException
from config import conn 
import psycopg2
from schema import User, Resources
from models import users, resources
from routes.login import log 
from routes.resources import res


cursor = conn.cursor()
app = FastAPI()

#app.include_router(res)
app.include_router(log)


@app.get("/")
def posts():
    cursor.execute(users)
    conn.commit()
    return {"message": "this is working"}


#CRUD operation

# Create user
@app.post("/users/")
def create_user(user: User):

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", 
                       (user.username, user.email, user.password))
        conn.commit()
        return {"message": "User created successfully"}
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {e}")
    # finally:
    #     cursor.close()
    #     conn.close()

####################################################################################################################################

# Get user by ID
@app.get("/users/{user_id}/")
def read_user(user_id: int):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, email FROM users WHERE id = %s;", (user_id,))
        user = cursor.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "email": user[2]}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {e}")
    # finally:
    #     cursor.close()
    #     conn.close()

# Update user by ID
# @app.put("/users/{user_id}/")
# def update_user(user_id: int, username: str, email: str):
#     cursor = None
#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE users SET username = %s, email = %s WHERE id = %s;",(username, email, user_id)
#         )
#         conn.commit()
#         return {"message": "User updated successfully"}
#     except psycopg2.Error as e:
#         conn.rollback()  # Rollback changes if there's an error
#         print("\n\ncheckin\n\n")
#         raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         conn.close()  # Close the connection in the finally block

# Delete user by ID
# @app.delete("/users/{user_id}/")
# def delete_user(user_id: int):
   
#     cursor = conn.cursor()
#     try:
#         cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
#         conn.commit()
#         return {"message": "User deleted successfully"}
#     except psycopg2.Error as e:
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")
#     # finally:
#     #     cursor.close()
#     #     conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



