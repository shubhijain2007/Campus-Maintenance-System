import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from database import DB_NAME


def load_data():

    connection = sqlite3.connect(DB_NAME)

    complaints = pd.read_sql_query(
        "SELECT * FROM complaints",
        connection
    )

    maintenance = pd.read_sql_query(
        "SELECT * FROM maintenance",
        connection
    )

    connection.close()

    return complaints, maintenance


def show_analysis():

    complaints, maintenance = load_data()

    if complaints.empty:
        print("No complaints found.")
        return

    print("\n===== CAMPUS MAINTENANCE ANALYSIS =====")

    # Total complaints
    total_complaints = len(complaints)
    print("Total Complaints:", total_complaints)

    # Complaints by status
    status_counts = complaints["status"].value_counts()
    print("\nComplaints by Status:")
    print(status_counts)

    # Most common category
    common_category = complaints["category"].value_counts().idxmax()
    print("\nMost Common Category:", common_category)

    # Building with highest complaints
    common_building = complaints["building"].value_counts().idxmax()
    print("Building with Highest Complaints:", common_building)

    # Maintenance cost
    if not maintenance.empty:

        total_cost = maintenance["cost"].sum()
        average_cost = maintenance["cost"].mean()

        print("\nTotal Maintenance Cost:", total_cost)
        print("Average Maintenance Cost:", round(average_cost, 2))

    else:
        print("\nNo maintenance records found.")

    # Chart 1 - Complaints by Status
    status_counts.plot(
        kind="bar",
        title="Complaints by Status"
    )

    plt.xlabel("Status")
    plt.ylabel("Number of Complaints")
    plt.tight_layout()
    plt.show()

    # Chart 2 - Complaints by Category
    category_counts = complaints["category"].value_counts()

    category_counts.plot(
        kind="bar",
        title="Complaints by Category"
    )

    plt.xlabel("Category")
    plt.ylabel("Number of Complaints")
    plt.tight_layout()
    plt.show()

    # Chart 3 - Complaints by Building
    building_counts = complaints["building"].value_counts()

    building_counts.plot(
        kind="bar",
        title="Complaints by Building"
    )

    plt.xlabel("Building")
    plt.ylabel("Number of Complaints")
    plt.tight_layout()
    plt.show()

    # Chart 4 - Maintenance Cost
    if not maintenance.empty:

        maintenance.plot(
            x="complaint_id",
            y="cost",
            kind="bar",
            title="Maintenance Cost by Complaint"
        )

        plt.xlabel("Complaint ID")
        plt.ylabel("Cost")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    show_analysis()