from src.database.config import supabase
import bcrypt  # for hashing the passwords during registration



def check_teacher_exists(username):
    # for checking if the username is unique or not 
    # returns false when username is already taken

    response = supabase.table("teachers").select("username").eq("username",username).execute()
    # this line will return the row where the username matches the passed username

    return len(response.data) > 0


def hash_pass(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()


def check_pass(password,hashed_password):
    return bcrypt.checkpw(password.encode(),hashed_password.encode())

def create_teacher(username,password,name):
    data = {
        "username":username,
        "password":hash_pass(password),
        "name":name
    }

    response = supabase.table("teachers").insert(data).execute()

    return response.data

def teacher_login(username,password):
    reponse=supabase.table("teachers").select("*").eq("username",username).execute()

    if reponse.data:
        teacher = reponse.data[0]
        if check_pass(password,teacher["password"]):
            print(teacher)
            return teacher
        
    return None

