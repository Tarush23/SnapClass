import dlib 
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector,sp,facerec


def get_face_embeddings(image_np):
    detector,sp,facerec = load_dlib_models()

    faces = detector(image_np,1)
    st.write("Shape:", image_np.shape)
    st.write("Faces found:", len(faces))
    encodings=[]

    for face in faces:
        shape = sp(image_np,face) # 68 landmarks

        face_descriptor = facerec. compute_face_descriptor(image_np,shape,1) # 128 vectors

        encodings.append(np.array(face_descriptor))

    return encodings


@st.cache_resource
def get_trained_model():
    X=[]
    y=[]

    student_db = get_all_students()
    if not student_db:   # number of students = 0
        return None
    
    for student in student_db:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get("student_id"))


    if len(X)==0:
        return 0
    
    clf = SVC(kernel="linear",probability=True,class_weight="balanced")

    try:
        clf.fit(X,y)
    except ValueError:
        pass

    return {"clf":clf,"X":X,"y":y}


def train_classifier():    # when a new student registered on the application
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np) #create embedding for each face in the photo

    detected_student = {}  

    model_data = get_trained_model()

    if not model_data:
        return {},{},len(encodings)
    
    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))  

    for encoding in encodings:
        if len(all_students)>=2:
            predicted_id = int(clf.predict([encoding])[0]) # clf takes input as 2d arrary so we do [encoding],precition is then made and we take the first item (first id) and then store it
        else:
            predicted_id = int(all_students[0])  # this is when there is only 1 student in the database then no need to make any prediction


        student_embedding = X_train[y_train.index(predicted_id)]  # get the embedding of the id predicted by the model

        best_match_score = np.linalg.norm(student_embedding-encoding) 

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:  # if the difference between predicted id and actual id(their embeddings) is less than 0.6, then only attendance will be marked as true
                detected_student[predicted_id]=True

    return detected_student,all_students,len(encodings)
 # detected student list will look like {101:true,102:true,103:false}


