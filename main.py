import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import date
from database import DB_NAME

# Create main window
root = tk.Tk()

root.title("CampusFix - Maintenance Control System")
root.geometry("900x600")
root.configure(bg="#0b1f33")


# ---------- Functions ----------

def register_complaint():

    window = tk.Toplevel(root)
    window.title("Register Complaint")
    window.geometry("700x650")
    window.configure(bg="#0b1f33")

    tk.Label(
        window,
        text="REGISTER A COMPLAINT",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#0b1f33"
    ).pack(pady=20)

    form = tk.Frame(window, bg="#0b1f33")
    form.pack(pady=10)

    # Student Name
    tk.Label(form, text="Student Name",
             fg="white", bg="#0b1f33").grid(row=0, column=0, padx=10, pady=10)

    student_entry = tk.Entry(form, width=35)
    student_entry.grid(row=0, column=1, padx=10, pady=10)

    # Department
    tk.Label(form, text="Department",
             fg="white", bg="#0b1f33").grid(row=1, column=0, padx=10, pady=10)

    department_entry = tk.Entry(form, width=35)
    department_entry.grid(row=1, column=1, padx=10, pady=10)

    # Building
    tk.Label(form, text="Building",
             fg="white", bg="#0b1f33").grid(row=2, column=0, padx=10, pady=10)

    building_entry = tk.Entry(form, width=35)
    building_entry.grid(row=2, column=1, padx=10, pady=10)

    # Room
    tk.Label(form, text="Room No.",
             fg="white", bg="#0b1f33").grid(row=3, column=0, padx=10, pady=10)

    room_entry = tk.Entry(form, width=35)
    room_entry.grid(row=3, column=1, padx=10, pady=10)

    # Category
    tk.Label(form, text="Category",
             fg="white", bg="#0b1f33").grid(row=4, column=0, padx=10, pady=10)

    category_box = ttk.Combobox(
        form,
        values=[
            "Electrical",
            "Furniture",
            "Plumbing",
            "IT",
            "Internet",
            "Cleaning",
            "AC/Cooling",
            "Other"
        ],
        width=32,
        state="readonly"
    )
    category_box.grid(row=4, column=1, padx=10, pady=10)

    # Priority
    tk.Label(form, text="Priority",
             fg="white", bg="#0b1f33").grid(row=5, column=0, padx=10, pady=10)

    priority_box = ttk.Combobox(
        form,
        values=["Low", "Medium", "High"],
        width=32,
        state="readonly"
    )
    priority_box.grid(row=5, column=1, padx=10, pady=10)

    # Problem
    tk.Label(form, text="Problem Description",
             fg="white", bg="#0b1f33").grid(row=6, column=0, padx=10, pady=10)

    problem_entry = tk.Entry(form, width=35)
    problem_entry.grid(row=6, column=1, padx=10, pady=10)

    # Submit function
    def save_complaint():

        student = student_entry.get()
        department = department_entry.get()
        building = building_entry.get()
        room = room_entry.get()
        category = category_box.get()
        priority = priority_box.get()
        problem = problem_entry.get()

        if not student or not problem:
            messagebox.showerror(
                "Error",
                "Student Name and Problem are required."
            )
            return

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        # Generate Complaint ID
        cursor.execute("SELECT COUNT(*) FROM complaints")
        count = cursor.fetchone()[0] + 1

        complaint_id = f"CMP{count:03d}"

        cursor.execute("""
            INSERT INTO complaints
            (complaint_id, student_name, department, building,
             room_no, category, problem, priority, status, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            complaint_id,
            student,
            department,
            building,
            room,
            category,
            problem,
            priority,
            "Pending",
            date.today().isoformat()
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            f"Complaint Registered Successfully!\n\nComplaint ID: {complaint_id}"
        )

        window.destroy()

    # Submit button
    tk.Button(
        window,
        text="Register Complaint",
        command=save_complaint,
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#173b5c",
        fg="white"
    ).pack(pady=25)


def view_complaints():

    window = tk.Toplevel(root)
    window.title("All Complaints")
    window.geometry("1000x500")

    tk.Label(
        window,
        text="ALL COMPLAINTS",
        font=("Arial", 22, "bold")
    ).pack(pady=15)

    # Table columns
    columns = (
        "Complaint ID",
        "Student",
        "Category",
        "Building",
        "Priority",
        "Status",
        "Date"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=130)

    table.pack(fill="both", expand=True, padx=20, pady=10)

    # Get complaints from database
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT complaint_id, student_name, category,
               building, priority, status, date
        FROM complaints
    """)

    complaints = cursor.fetchall()

    connection.close()

    # Put data into table
    for complaint in complaints:
        table.insert("", tk.END, values=complaint)


def search_complaint():

    window = tk.Toplevel(root)
    window.title("Search Complaint")
    window.geometry("600x450")

    tk.Label(
        window,
        text="SEARCH COMPLAINT",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter Complaint ID:"
    ).pack(pady=5)

    search_entry = tk.Entry(
        window,
        width=30
    )
    search_entry.pack(pady=10)

    result_label = tk.Label(
        window,
        text="",
        font=("Arial", 11),
        justify="left"
    )
    result_label.pack(pady=20)

    def search():

        complaint_id = search_entry.get().strip()

        if not complaint_id:
            messagebox.showerror(
                "Error",
                "Please enter Complaint ID."
            )
            return

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT complaint_id, student_name, department,
                   building, room_no, category, problem,
                   priority, status, date
            FROM complaints
            WHERE complaint_id = ?
        """, (complaint_id,))

        complaint = cursor.fetchone()

        connection.close()

        if complaint:

            result_label.config(
                text=f"""
Complaint ID: {complaint[0]}
Student Name: {complaint[1]}
Department: {complaint[2]}
Building: {complaint[3]}
Room No.: {complaint[4]}
Category: {complaint[5]}
Problem: {complaint[6]}
Priority: {complaint[7]}
Status: {complaint[8]}
Date: {complaint[9]}
"""
            )

        else:
            result_label.config(
                text="Complaint Not Found",
                fg="red"
            )

    tk.Button(
        window,
        text="Search",
        command=search,
        width=20,
        height=2
    ).pack(pady=10)


def update_status():

    window = tk.Toplevel(root)
    window.title("Update Complaint Status")
    window.geometry("600x450")

    tk.Label(
        window,
        text="UPDATE COMPLAINT STATUS",
        font=("Arial", 22, "bold")
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Complaint ID:"
    ).pack(pady=5)

    complaint_entry = tk.Entry(
        window,
        width=30
    )
    complaint_entry.pack(pady=10)

    tk.Label(
        window,
        text="Select New Status:"
    ).pack(pady=5)

    status_box = ttk.Combobox(
        window,
        values=["Pending", "In Progress", "Resolved"],
        width=27,
        state="readonly"
    )
    status_box.pack(pady=10)

    current_status_label = tk.Label(
        window,
        text=""
    )
    current_status_label.pack(pady=10)

    def find_complaint():

        complaint_id = complaint_entry.get().strip()

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT status FROM complaints WHERE complaint_id = ?",
            (complaint_id,)
        )

        result = cursor.fetchone()
        connection.close()

        if result:
            current_status_label.config(
                text=f"Current Status: {result[0]}"
            )
        else:
            current_status_label.config(
                text="Complaint Not Found",
                fg="red"
            )

    def save_status():

        complaint_id = complaint_entry.get().strip()
        new_status = status_box.get()

        if not complaint_id:
            messagebox.showerror(
                "Error",
                "Please enter Complaint ID."
            )
            return

        if not new_status:
            messagebox.showerror(
                "Error",
                "Please select a status."
            )
            return

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT status FROM complaints WHERE complaint_id = ?",
            (complaint_id,)
        )

        result = cursor.fetchone()

        if not result:
            connection.close()
            messagebox.showerror(
                "Error",
                "Complaint Not Found."
            )
            return

        cursor.execute(
            """
            UPDATE complaints
            SET status = ?
            WHERE complaint_id = ?
            """,
            (new_status, complaint_id)
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            f"{complaint_id} status updated to {new_status}."
        )

        window.destroy()

    tk.Button(
        window,
        text="Check Complaint",
        command=find_complaint,
        width=20
    ).pack(pady=10)

    tk.Button(
        window,
        text="Update Status",
        command=save_status,
        width=20,
        height=2
    ).pack(pady=15)


def add_maintenance():

    window = tk.Toplevel(root)
    window.title("Add Maintenance Details")
    window.geometry("650x550")

    tk.Label(
        window,
        text="ADD MAINTENANCE DETAILS",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack(pady=10)

    # Complaint ID
    tk.Label(form, text="Complaint ID").grid(
        row=0, column=0, padx=10, pady=10
    )

    complaint_entry = tk.Entry(form, width=35)
    complaint_entry.grid(
        row=0, column=1, padx=10, pady=10
    )

    # Staff Name
    tk.Label(form, text="Staff Name").grid(
        row=1, column=0, padx=10, pady=10
    )

    staff_entry = tk.Entry(form, width=35)
    staff_entry.grid(
        row=1, column=1, padx=10, pady=10
    )

    # Repair Date
    tk.Label(form, text="Repair Date").grid(
        row=2, column=0, padx=10, pady=10
    )

    repair_date_entry = tk.Entry(form, width=35)
    repair_date_entry.grid(
        row=2, column=1, padx=10, pady=10
    )
    repair_date_entry.insert(0, date.today().isoformat())

    # Repair Cost
    tk.Label(form, text="Repair Cost").grid(
        row=3, column=0, padx=10, pady=10
    )

    cost_entry = tk.Entry(form, width=35)
    cost_entry.grid(
        row=3, column=1, padx=10, pady=10
    )

    # Remarks
    tk.Label(form, text="Remarks").grid(
        row=4, column=0, padx=10, pady=10
    )

    remarks_entry = tk.Entry(form, width=35)
    remarks_entry.grid(
        row=4, column=1, padx=10, pady=10
    )

    def save_maintenance():

        complaint_id = complaint_entry.get().strip()
        staff_name = staff_entry.get().strip()
        repair_date = repair_date_entry.get().strip()
        cost = cost_entry.get().strip()
        remarks = remarks_entry.get().strip()

        if not complaint_id or not staff_name or not repair_date or not cost:
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return

        try:
            cost = float(cost)

            if cost < 0:
                messagebox.showerror(
                    "Error",
                    "Repair cost cannot be negative."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Repair cost must be a number."
            )
            return

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        # Check whether complaint exists
        cursor.execute(
            "SELECT complaint_id FROM complaints WHERE complaint_id = ?",
            (complaint_id,)
        )

        complaint = cursor.fetchone()

        if not complaint:
            connection.close()
            messagebox.showerror(
                "Error",
                "Complaint Not Found."
            )
            return

        # Save maintenance details
        cursor.execute(
            """
            INSERT INTO maintenance
            (complaint_id, staff_name, repair_date, cost, remarks)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                complaint_id,
                staff_name,
                repair_date,
                cost,
                remarks
            )
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Maintenance details saved successfully!"
        )

        window.destroy()

    tk.Button(
        window,
        text="Save Maintenance",
        command=save_maintenance,
        width=25,
        height=2,
        font=("Arial", 12, "bold")
    ).pack(pady=25)


def reports_analysis():
    from analysis import show_analysis
    show_analysis()


def exit_application():
    root.destroy()


# ---------- Heading ----------

title = tk.Label(
    root,
    text="CampusFix",
    font=("Arial", 32, "bold"),
    fg="white",
    bg="#0b1f33"
)

title.pack(pady=(50, 5))


subtitle = tk.Label(
    root,
    text="MAINTENANCE CONTROL SYSTEM",
    font=("Arial", 12),
    fg="#7dd3fc",
    bg="#0b1f33"
)

subtitle.pack(pady=(0, 40))


# ---------- Buttons ----------

button_frame = tk.Frame(root, bg="#0b1f33")
button_frame.pack()


buttons = [
    ("Register Complaint", register_complaint),
    ("View Complaints", view_complaints),
    ("Search Complaint", search_complaint),
    ("Update Status", update_status),
    ("Add Maintenance", add_maintenance),
    ("Reports & Analysis", reports_analysis),
    ("Exit", exit_application)
]


for text, command in buttons:
    button = tk.Button(
        button_frame,
        text=text,
        command=command,
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#173b5c",
        fg="white"
    )
    button.pack(pady=7)


# Start application
root.mainloop()