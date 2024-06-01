import customtkinter as ctk
import os  # For path handling


def read_latest_activity_and_budget():
    """Reads the latest activity and budget from work_data.txt."""
    try:
        with open("work_data.txt", "r") as work_file:
            lines = work_file.readlines()
        # Assuming the latest line has activity and budget
        latest_line = lines[-1].strip()
        activity, budget_text = latest_line.split(": ")
        budget = float(budget_text)
        return activity, budget
    except FileNotFoundError:
        print("work_data.txt not found. No previous activity and budget data.")
        return None, None


def parse_activity_data(filename):
    """Reads activity data from a file and returns a dictionary (simplified)."""
    data = {}
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return data
    try:
        with open(filename, "r") as file:
            current_provider = None
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                if line.isupper():  # Assuming provider names are uppercase
                    current_provider = line
                    data[current_provider] = []
                else:
                    activity_data = line.split(": ", 1)  # Split at most once
                    if len(activity_data) == 2:  # Ensure two elements
                        activity, price = activity_data
                        data[current_provider].append((activity, price))  # Activity and price as tuple
                    else:
                        print(f"Warning: Skipping line with invalid format in {filename}")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    return data


def find_suitable_activities(activities, budget):
    """Finds activities within budget from the provided data."""
    suitable_activities = []
    for provider, activity_prices in activities.items():
        for activity, price in activity_prices:
            if float(price) <= budget:
                suitable_activities.append(f"{provider}: {activity} - ₹{price}")
    return suitable_activities


def display_activities(activity_list, root):
    """Displays a list of activities within a CTkFrame."""

    # Create a frame to hold the activity list
    activity_frame = ctk.CTkFrame(master=root)
    activity_frame.pack(padx=20, pady=10)

    # Add activity labels to the frame
    if not activity_list:
        label = ctk.CTkLabel(master=activity_frame, text="No activities found within your budget.")
        label.pack(padx=10, pady=10)
    else:
        for activity_text in activity_list:
            label = ctk.CTkLabel(master=activity_frame, text=activity_text)
            label.pack(padx=10, pady=5)


def main():
    # Retrieve activity and budget from the last line of work_data.txt
    activity, budget = read_latest_activity_and_budget()

    # Create the main window
    root = ctk.CTk()
    root.geometry("500x400")
    root.title("The Sociale - Activity Search")

    # Display retrieved activity (optional)
    activity_label = ctk.CTkLabel(master=root, text=f"Previous Activity: {activity}")
    activity_label.pack(padx=20, pady=10)

    # If activity and budget are found, proceed with search using the relative path
    if activity and budget:
                # Use the relative path (activity.txt) for the activity data file
        activity_file = "activity.txt"

        # Read activity data from the file
        activities = parse_activity_data(activity_file)

        # Find suitable activities
        suitable_activities = find_suitable_activities(activities, budget)

        # Display search results
        display_activities(suitable_activities, root)
    else:
        label = ctk.CTkLabel(master=root, text="No previous activity and budget data found.")
        label.pack(padx=20, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()