import customtkinter as ct

def read_work_data():
    """Reads work_data.txt and returns a dictionary of activities and their budgets."""
    try:
        with open("work_data.txt", "r") as file:
            lines = file.readlines()
            print("work_data.txt contents:")
            for line in lines:
                print(line.strip())
            work_data = {}
            for line in reversed(lines):
                line = line.strip()
                if line:
                    activity, budget = line.split(":")
                    work_data[activity] = float(budget)
                    break
            print("work_data:", work_data)
            return work_data
    except FileNotFoundError:
        print("Error: work_data.txt not found")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def find_activities():
    """Reads activity.txt, compares activities to budgets in work_data.txt, and displays matching activities."""
    work_data = read_work_data()
    if not work_data:
        result_label.configure(text="No data found in work_data.txt")
        return

    activity_all_caps = {k.upper(): v for k, v in work_data.items()}
    print("activity_all_caps:", activity_all_caps)

    result_text = ""
    found_match = False
    try:
        with open("activity.txt", "r") as file:
            current_activity = None
            for line in file:
                line = line.strip()
                print("activity.txt line:", line)
                if line.isupper():
                    current_activity = line
                elif line.startswith(current_activity.lower() + ":"):
                    details = line.split(":")[1:]
                    # Extract price, handling potential ranges like "10-15"
                    price = float(details[0].split("-")[0]) if "-" in details[0] else float(details[0])
                    print("Matching activity:", current_activity, "with price", price)
                    if current_activity in activity_all_caps and price <= activity_all_caps[current_activity]:
                        result_text += line + "\n"
                        found_match = True
    except FileNotFoundError:
        print("Error: activity.txt not found")
        result_label.configure(text="Error: activity.txt not found")
    except Exception as e:
        print(f"Error: {e}")
        result_label.configure(text=f"Error: {e}")

    if found_match:
        result_label.configure(text=result_text)
    else:
        result_label.configure(text="No activity found within budget")

# Create the main window
root = ct.CTk()
root.title("Activity Finder")

# Label to display results
result_label = ct.CTkLabel(master=root, text="", wraplength=400)
result_label.pack(pady=20)

# Button to trigger the activity search
search_button = ct.CTkButton(master=root, text="Find Activities", command=find_activities)
search_button.pack(pady=20)

# Run the GUI
root.mainloop()