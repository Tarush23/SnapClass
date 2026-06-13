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

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


def create_student(name,face_embedding,voice_embedding):
    data = {
        "name":name,
        "face_embedding":face_embedding,
        "voice_embedding":voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_subject(sub_code,sub_name,sub_section,teacher_id):
    data = {
        "subject_code":sub_code,
        "name":sub_name,
        "section":sub_section,
        "teacher_id":teacher_id
    }

    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):

    response = (
        supabase
        .table("subjects")
        .select(
            "*, subject_students(count), attendance_logs(timestamp)"
        )
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for subject in subjects:

        # ---------- Count students ----------

        students = subject.get(
            "subject_students",
            []
        )

        if students:
            subject["total_students"] = (
                students[0]["count"]
            )

        else:
            subject["total_students"] = 0


        # ---------- Count classes ----------

        attendance = subject.get(
            "attendance_logs",
            []
        )

        timestamps = []

        for log in attendance:
            timestamps.append(
                log["timestamp"]
            )

        subject["total_classes"] = (
            len(
                set(timestamps)
            )
        )
        # ---------- Remove extra data ----------
        subject.pop(
            "subject_students",
            None
        )

        subject.pop(
            "attendance_logs",
            None
        )
    return subjects

    