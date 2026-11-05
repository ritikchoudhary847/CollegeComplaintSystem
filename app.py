import streamlit as st
import sqlite3

st.title("College Complaint System")
st.header("Submit a Complaint")

student_name = st.text_input("Student Name")
roll_no = st.text_input("Roll Number")
complaint = st.text_area("Enter your complaint")

category = st.selectbox(
    "Select Category",
    ["Electrical", "Network", "Other"]
)
priority = st.selectbox(
    "Select Priority",
    ["Low", "Medium", "High"]
)
if st.button("Submit Complaint"):

    if student_name.strip() == "":
        st.error("Please enter Student Name.")

    elif roll_no.strip() == "":
        st.error("Please enter Roll Number.")

    elif complaint.strip() == "":
        st.error("Please enter your Complaint.")

    else:
        connection = sqlite3.connect("college_complaints.db")
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO complaints
            (student_name, roll_no, complaint, category, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_name.strip(),
                roll_no.strip(),
                complaint.strip(),
                category,
                priority,
                "Pending"
            )
        )
        connection.commit()
        connection.close()

        st.success("Complaint Submitted Successfully!")