import streamlit as st

from src.database.db import get_teacher_subjects
from src.database.config import supabase

enrolled_res = supabase.table("subject_students").select("*,students(*)").eq("subject_id",2).execute()

    
print(enrolled_res)