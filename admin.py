import streamlit as st
import sqlite3
import csv
import io


st.title("College Complaint System")

# ---------------- ADMIN LOGIN ----------------

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False


if not st.session_state["admin_logged_in"]:

    st.header("Admin Login")

    username = st.text_input("Admin Username")

    password = st.text_input(
        "Admin Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state["admin_logged_in"] = True

            st.success("Admin Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Username or Password.")

# ---------------- ADMIN DASHBOARD ----------------

else:

    st.header("Admin Dashboard")

    # ---------------- LOGOUT ----------------

    if st.button("Logout"):

        st.session_state["admin_logged_in"] = False

        st.rerun()

    # ---------------- DATABASE CONNECTION ----------------

    connection = sqlite3.connect(
        "college_complaints.db"
    )

    cursor = connection.cursor()

    # ---------------- COMPLAINT COUNTS ----------------

    cursor.execute(
        "SELECT COUNT(*) FROM complaints"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints "
        "WHERE status = 'Pending'"
    )

    pending = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints "
        "WHERE status = 'In Progress'"
    )
    in_progress = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints "
        "WHERE status = 'Resolved'"
    )

    resolved = cursor.fetchone()[0]

    # ---------------- DASHBOARD COUNTERS ----------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total)

    col2.metric("Pending", pending)

    col3.metric("In Progress", in_progress)

    col4.metric("Resolved", resolved)

    # ---------------- PRIORITY SUMMARY ----------------

    st.divider()
    st.subheader("Priority Summary")
    cursor.execute(
        "SELECT COUNT(*) FROM complaints "
        "WHERE priority = 'High'"
    )

    high_priority = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints "
        "WHERE priority = 'Medium'"
    )

    medium_priority = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints "
        "WHERE priority = 'Low'"
    )

    low_priority = cursor.fetchone()[0]

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "High Priority",
        high_priority
    )

    p2.metric(
        "Medium Priority",
        medium_priority
    )

    p3.metric(
        "Low Priority",
        low_priority
    )

    # ---------------- CATEGORY SUMMARY ----------------

    st.divider()
    st.subheader("Category Summary")
    cursor.execute(
        """
        SELECT
        COALESCE(NULLIF(TRIM(category), ''), 'Uncategorized'),
        COUNT(*)
        FROM complaints
        GROUP BY
        COALESCE(NULLIF(TRIM(category), ''), 'Uncategorized')
        ORDER BY 1
       """)

    category_summary = cursor.fetchall()
    if len(category_summary) == 0:

        st.info(
            "No category data available."
        )
    else:
        c1, c2, c3 = st.columns(3)
        for i, item in enumerate(category_summary):

            category_name = item[0]

            category_count = item[1]
            if i % 3 == 0:

                c1.metric(
                    category_name,
                    category_count
                )

            elif i % 3 == 1:

                c2.metric(
                    category_name,
                    category_count
                )
            else:

                c3.metric(
                    category_name,
                    category_count
                )

    # ---------------- SEARCH ----------------

    st.divider()
    st.subheader("Search Complaint")
    search_roll_no = st.text_input(
        "Enter Student Roll Number"
    )

    search_complaint_id = st.text_input(
        "Enter Complaint ID"
    )

    # ---------------- FILTERS ----------------

    st.subheader("Filter Complaints")

    filter_priority = st.selectbox(
        "Select Priority",
        [
            "All",
            "High",
            "Medium",
            "Low"
        ]
    )

    filter_category = st.selectbox(
        "Select Category",
        [
            "All",
            "Electrical",
            "Network",
            "Classroom",
            "Library",
            "Other"
        ]
    )

    # ---------------- GET COMPLAINTS ----------------

    if search_complaint_id.strip() != "":

        cursor.execute(
            """
            SELECT * FROM complaints
            WHERE id = ?
            """,
            (
                search_complaint_id.strip(),
            )
        )

    elif search_roll_no.strip() != "":

        cursor.execute(
            """
            SELECT * FROM complaints
            WHERE roll_no = ?
            """,
            (
                search_roll_no.strip(),
            )
        )

    elif (
        filter_priority == "All"
        and
        filter_category == "All"
    ):

        cursor.execute(
            """
            SELECT * FROM complaints
            ORDER BY
                CASE priority
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                END
            """
        )

    elif (
        filter_priority != "All"
        and
        filter_category == "All"
    ):

        cursor.execute(
            """
            SELECT * FROM complaints
            WHERE priority = ?
            ORDER BY id DESC
            """,
            (
                filter_priority,
            )
        )

    elif (
        filter_priority == "All"
        and
        filter_category != "All"
    ):
        cursor.execute(
            """
            SELECT * FROM complaints
            WHERE category = ?
            ORDER BY id DESC
            """,
            (
                filter_category,
            )
        )
    else:

        cursor.execute(
            """
            SELECT * FROM complaints
            WHERE priority = ?
            AND category = ?
            ORDER BY id DESC
            """,
            (
                filter_priority,
                filter_category
            )
        )
    complaints = cursor.fetchall()

    # =====================================================
    # DOWNLOAD COMPLAINT REPORT
    # =====================================================

    st.divider()
    st.subheader(
        "Download Complaint Report"
    )
    if len(complaints) > 0:

        output = io.StringIO()

        writer = csv.writer(output)

        # CSV headings

        writer.writerow([
            "Complaint ID",
            "Student Name",
            "Roll Number",
            "Complaint",
            "Category",
            "Priority",
            "Status",
            "Date & Time"
        ])
        # Complaint data

        for complaint in complaints:

            writer.writerow([
                complaint[0],
                complaint[1],
                complaint[2],
                complaint[3],
                complaint[4],
                complaint[5],
                complaint[6],
                complaint[7]
            ])
        csv_data = output.getvalue()
        st.download_button(
            "📥 Download Complaint Report",
            csv_data,
            "college_complaints_report.csv",
            "text/csv",
            key="admin_report_download"
        )
    else:

        st.info(
            "No complaints available for download."
        )

    # ---------------- SHOW COMPLAINTS ----------------

    st.divider()

    st.subheader("Complaints")
    if len(complaints) == 0:

        st.info(
            "No complaints found."
        )
    else:

        for complaint in complaints:

            with st.expander(
                "Complaint #"
                + str(complaint[0])
                + " - "
                + complaint[3]
            ):

                st.write(
                    "Student Name:",
                    complaint[1]
                )
                st.write(
                    "Roll Number:",
                    complaint[2]
                )
                st.write(
                    "Complaint:",
                    complaint[3]
                )
                st.write(
                    "Category:",
                    complaint[4]
                )
                st.write(
                    "Priority:",
                    complaint[5]
                )
                st.write(
                    "Date & Time:",
                    complaint[7]
                )
                current_status = complaint[6]

                # ---------------- STATUS MESSAGE ----------------

                if current_status == "Pending":

                    st.warning(
                        "🟡 Complaint is waiting for action."
                    )

                elif current_status == "In Progress":

                    st.info(
                        "🔵 Complaint is being processed."
                    )

                elif current_status == "Resolved":

                    st.success(
                        "🟢 Complaint has been resolved."
                    )
                st.write(
                    "Current Status:",
                    current_status
                )
                # ---------------- CHANGE STATUS ----------------
                new_status = st.selectbox(
                    "Change Status",
                    [
                        "Pending",
                        "In Progress",
                        "Resolved"
                    ],
                    index=[
                        "Pending",
                        "In Progress",
                        "Resolved"
                    ].index(current_status),
                    key="status_" + str(complaint[0])
                )
                if st.button(
                    "Update Status",
                    key="update_" + str(complaint[0])
                ):

                    cursor.execute(
                        """
                        UPDATE complaints
                        SET status = ?
                        WHERE id = ?
                        """,
                        (
                            new_status,
                            complaint[0]
                        )
                    )
                    connection.commit()
                    st.success(
                        "Status updated successfully!"
                    )
                    st.rerun()
    # ---------------- CLOSE DATABASE ----------------
    connection.close()