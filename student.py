import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
from priority import detect_priority

st.title("🏫 College Complaint Priority System")

st.write(
    "A simple system to submit, track and manage college complaints."
)
# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "student_name" not in st.session_state:
    st.session_state["student_name"] = ""

if "roll_no" not in st.session_state:
    st.session_state["roll_no"] = ""


# =========================================================
# LOGIN / REGISTRATION
# =========================================================

if not st.session_state["logged_in"]:

    st.header("Student Portal")


    # ---------------- STUDENT REGISTRATION ----------------

    register_tab, login_tab = st.tabs(
        ["Student Registration", "Student Login"]
    )
    with register_tab:

        st.subheader("Create Student Account")
        st.caption(
           "Register once to submit and track your college complaints."
        )

        name = st.text_input("Full Name")

        roll_no = st.text_input("Roll Number")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        department = st.text_input("Department")

        semester = st.selectbox(
            "Semester",
            [
                "1st Semester",
                "2nd Semester",
                "3rd Semester",
                "4th Semester",
                "5th Semester",
                "6th Semester",
                "7th Semester",
                "8th Semester"
            ]
        )
        if st.button("Register"):

            if name.strip() == "":

                st.error(
                    "Please enter your name."
                )

            elif roll_no.strip() == "":

                st.error(
                    "Please enter your roll number."
                )

            elif email.strip() == "":

                st.error(
                    "Please enter your email."
                )

            elif password.strip() == "":

                st.error(
                    "Please enter your password."
                )

            elif department.strip() == "":

                st.error(
                    "Please enter your department."
                )

            else:

                connection = sqlite3.connect(
                    "college_complaints.db"
                )

                cursor = connection.cursor()
                try:

                    password_hash = hashlib.sha256(
                        password.encode()
                    ).hexdigest()
                    cursor.execute(
                        """
                        INSERT INTO students
                        (name, roll_no, email, password,
                        department, semester)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            name.strip(),
                            roll_no.strip(),
                            email.strip(),
                            password_hash,
                            department.strip(),
                            semester
                        )
                    )
                    connection.commit()

                    st.success(
                        "Registration successful! "
                        "You can now login."
                    )

                except sqlite3.IntegrityError:

                    st.error(
                        "This Roll Number is already registered."
                    )
                finally:

                    connection.close()

    # ---------------- STUDENT LOGIN ----------------

    with login_tab:

        st.subheader("Student Login")

        st.caption(
            "Login using your registered Roll Number and Password."
        )

        login_roll_no = st.text_input(
            "Roll Number",
            key="login_roll"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            if login_roll_no.strip() == "":

                st.error(
                    "Please enter your Roll Number."
                )

            elif login_password.strip() == "":

                st.error(
                    "Please enter your Password."
                )

            else:

                connection = sqlite3.connect(
                    "college_complaints.db"
                )

                cursor = connection.cursor()
                password_hash = hashlib.sha256(
                    login_password.encode()
                ).hexdigest()
                cursor.execute(
                    """
                    SELECT name, roll_no
                    FROM students
                    WHERE roll_no = ? AND password = ?
                    """,
                    (
                        login_roll_no.strip(),
                        password_hash
                    )
                )
                student = cursor.fetchone()

                connection.close()
                if student:

                    st.session_state["logged_in"] = True

                    st.session_state["student_name"] = student[0]

                    st.session_state["roll_no"] = student[1]

                    st.rerun()

                else:

                    st.error(
                        "Invalid Roll Number or Password."
                    )
# =========================================================
# STUDENT DASHBOARD
# =========================================================

else:

    st.header(
        "Welcome, " +
        st.session_state["student_name"]
    )
    st.write(
        "Roll Number:",
        st.session_state["roll_no"]
    )
    # ---------------- LOGOUT ----------------

    if st.button("Logout"):

        st.session_state["logged_in"] = False

        st.session_state["student_name"] = ""

        st.session_state["roll_no"] = ""

        st.rerun()
    st.divider()

    # =====================================================
    # STUDENT PROFILE
    # =====================================================

    st.subheader("My Profile")
    connection = sqlite3.connect(
        "college_complaints.db"
    )

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT name, roll_no, email, department, semester
        FROM students
        WHERE roll_no = ?
        """,
        (st.session_state["roll_no"],)
    )

    profile = cursor.fetchone()
    connection.close()
    if profile:

        col1, col2 = st.columns(2)
        with col1:

            st.write(
                "**Name:**",
                profile[0]
            )

            st.write(
                "**Roll Number:**",
                profile[1]
            )

            st.write(
                "**Email:**",
                profile[2]
            )
        with col2:

            st.write(
                "**Department:**",
                profile[3]
            )

            st.write(
                "**Semester:**",
                profile[4]
            )
    st.divider()


    # =====================================================
    # MY COMPLAINTS
    # =====================================================

    st.subheader("My Complaints")
    connection = sqlite3.connect(
        "college_complaints.db"
    )

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, complaint, category,
        priority, status, created_at
        FROM complaints
        WHERE roll_no = ?
        ORDER BY id DESC
        """,
        (st.session_state["roll_no"],)
    )
    complaints = cursor.fetchall()

    connection.close()
    if len(complaints) == 0:

        st.info(
            "You have not submitted any complaints yet."
        )

    else:

        for complaint in complaints:

            with st.container(border=True):

             st.subheader(
              "📌 Complaint #" + str(complaint[0])
             )

            st.write(
            "**Complaint ID:**",
            complaint[0]
            )

            st.write(
                    "**Complaint:**",
                    complaint[1]
                )

            st.write(
                    "**Category:**",
                    complaint[2]
                )

            st.write(
                    "**Priority:**",
                    complaint[3]
                )

            st.write(
                    "**Status:**",
                    complaint[4]
                )

                # ---------------- STATUS MESSAGE ----------------

            if complaint[4] == "Pending":

                    st.warning(
                        "🟡 Complaint is waiting for action."
                    )

            elif complaint[4] == "In Progress":

                    st.info(
                        "🔵 Complaint is being processed."
                    )

            elif complaint[4] == "Resolved":

                    st.success(
                        "🟢 Complaint has been resolved."
                    )
            st.write(
                    "**Date & Time:**",
                    complaint[5]
                )
    st.divider()


   # =====================================================
    # SUBMIT NEW COMPLAINT
    # =====================================================

    st.subheader("Submit New Complaint")

    # Complaint Form

    with st.form("complaint_form"):

        complaint_text = st.text_area(
            "Enter your complaint"
        )
        category = st.selectbox(
            "Select Category",
            [
                "Select Category",
                "Electrical",
                "Network",
                "Classroom",
                "Library",
                "Other"
            ]
        )
        submit_complaint = st.form_submit_button(
            "Submit Complaint"
        )
        # ---------------- VALIDATION ----------------

        if submit_complaint:

            if complaint_text.strip() == "":

                st.error(
                    "Please enter your complaint."
                )

            elif len(complaint_text.strip()) < 10:

                st.error(
                    "Complaint must contain at least 10 characters."
                )

            elif category == "Select Category":

                st.error(
                    "Please select a category."
                )
            else:
                try:
                    connection = sqlite3.connect(
                        "college_complaints.db"
                    )
                    cursor = connection.cursor()
                    # Current date and time
                    current_time = datetime.now().strftime(
                        "%d-%m-%Y %I:%M %p"
                    )
                    # Automatic priority
                    priority = detect_priority(
                        complaint_text
                    )
                    # Save complaint

                    cursor.execute(
                        """
                        INSERT INTO complaints
                        (student_name, roll_no, complaint,
                        category, priority, status, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            st.session_state["student_name"],
                            st.session_state["roll_no"],
                            complaint_text.strip(),
                            category,
                            priority,
                            "Pending",
                            current_time
                        )
                    )
                    connection.commit()
                    connection.close()
                    st.success(
                        "Complaint submitted successfully!"
                    )
                    st.info(
                        "Automatically assigned priority: "
                        + priority
                    )
                except Exception as error:
                    st.error(
                        "Unable to submit complaint."
                    )
                    st.write(
                        "Error:",
                        error
                    )