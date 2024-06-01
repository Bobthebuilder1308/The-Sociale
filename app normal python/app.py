import customtkinter
from tkinter import StringVar, filedialog
import os

dark_theme = {
    "fg_color": "white",
    "text_color": "black",
    "button_bg": "gray",
    "button_fg": "white",
    "bg": "black",
}
light_theme = {
    "fg_color": "black",
    "text_color": "white",
    "button_bg": "lightgray",
    "button_fg": "black",
    "bg": "white",
}
current_theme = "dark"


def save_data(age, group_size, activity, budget):
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save Data",
    )

    if filename == "":
        return
    with open(filename, "w") as file:
        file.write(f"Age: {age}\n")
        file.write(f"Group Size: {group_size}\n")
        file.write(f"Activity: {activity}\n")
        file.write(f"Budget: {budget}\n")

    print("Data saved successfully!")


def change_theme(event):
    global current_theme, theme_clicks
    theme_clicks += 1
    if current_theme == "dark":
        current_theme = "light"
    else:
        current_theme = "dark"
    theme_button.configure(
        fg_color=light_theme["fg_color"] if current_theme == "light" else dark_theme["fg_color"],
        text_color=light_theme["text_color"] if current_theme == "light" else dark_theme["text_color"],
    )
    root.configure(
        fg_color=light_theme["fg_color"] if current_theme == "light" else dark_theme["fg_color"],
        bg=light_theme["bg"] if current_theme == "light" else dark_theme["bg"],
    )


def open_new_page():
    global new_window, age_entry, group_size_entry, activity_var, budget_var, budget_label
    new_window = customtkinter.CTk()
    new_window.geometry("500x500")

    age_label = customtkinter.CTkLabel(master=new_window, text="Age:")
    age_label.pack(padx=20, pady=10)
    age_entry = customtkinter.CTkEntry(master=new_window, width=50)
    age_entry.pack(padx=20, pady=10)
    group_size_label = customtkinter.CTkLabel(master=new_window, text="Group size:")
    group_size_label.pack(padx=20, pady=10)
    group_size_entry = customtkinter.CTkEntry(master=new_window, width=50)
    group_size_entry.pack(padx=20, pady=10)
    activity_label = customtkinter.CTkLabel(master=new_window, text="Activity:")
    activity_label.pack(padx=20, pady=10)
    activity_options = ["Movie", "Bowling", "Amusement Park", "Escape Room", "Hiking"]
    activity_var = StringVar(new_window)
    activity_var.set(activity_options[0])
    activity_menu = customtkinter.CTkOptionMenu(
        master=new_window, values=activity_options, variable=activity_var
    )
    activity_menu.pack(padx=20, pady=10)
    budget_label = customtkinter.CTkLabel(master=new_window, text="Budget:")
    budget_var = StringVar(new_window)
    budget_label.pack(padx=20, pady=10)
    budget_entry = customtkinter.CTkEntry(master=new_window, width=50, textvariable=budget_var)
    budget_entry.pack(padx=40, pady=20)
submit_button = customtkinter.CTkButton(
    master=new_window,
    text="Submit",
    command=lambda: submit_form(age_entry, group_size_entry, activity_var, budget_var, budget_label),
)
submit_button.pack(padx=20, pady=10)

new_window.mainloop()


def format_budget(value):
    return f"{value}₹"


theme_clicks = 0
root = customtkinter.CTk()
root.title("The Sociale")
button = customtkinter.CTkButton(master=root, text="Welcome To Sociale (We Are Working on the name)", command=open_new_page)
root.geometry("500x500")
button.place(relx=0.5, rely=0.5, anchor="center")
theme_button = customtkinter.CTkButton(master=root, text="Theme")
theme_button.place(relx=1, rely=0, anchor="ne")
theme_button.bind("<Button-1>", change_theme)
root.configure(fg_color=dark_theme["fg_color"], bg=dark_theme["bg"])

data_file = "group_activity_data.txt"  # File for all details


def submit_form(age_entry, group_size_entry, activity_var, budget_var, budget_label):
    budget = budget_var.get()
    budget_label.configure(text=f"Budget: {format_budget(budget)}")
    age = age_entry.get()
    group_size = group_size_entry.get()
    activity = activity_var.get()

    # Save all details to group_activity_data.txt (as before)
    with open(data_file, "a") as file:
        file.write(f"Age: {age}\n")
        file.write(f"Group Size: {group_size}\n")
        file.write(f"Activity: {activity}\n")
        file.write(f"Budget: {budget}\n\n")
    print(f"Data saved successfully to {data_file}")

    # Save activity and budget to work_data.txt
    work_data = f"{activity}: {budget}\n"  # Format data for work_data.txt
    with open("work_data.txt", "a") as work_file:
        work_file.write(work_data)
    print(f"Data saved successfully to group_activity_data.txt and work_data.txt")

root.mainloop()

def parse_activity_data(filename, activity_name):
    """
    Reads activity data from a file and returns a dictionary (simplified).
    Focuses on the specified activity based on the activity_name.
    """
    data = {}
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return data
    try:
        with open(filename, "r") as file:
            current_activity = None
            for line in file:
                line = line.strip()
                if line.isupper():  # Assuming activity names are uppercase
                    current_activity = line
                elif current_activity and current_activity == activity_name:
                    # Activity block found, process lines within this block
                    data[current_activity] = []
                    for detail in file:  # Loop through details for this activity
                        detail = detail.strip()
                        if not detail or detail.isupper():  # Break on empty line or new activity
                            break
                        place, price = detail.split(": ", 1)  # Assuming price follows place
                        try:
                            price = float(price.strip("₹"))  # Convert price to float (assuming currency symbol)
                        except ValueError:
                            print(f"Warning: Invalid price format for {place} in {filename}. Skipping.")
                            continue
                        data[current_activity].append((place, price))  # Store place and price as tuple
                    break  # Exit loop after processing this activity block
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    return data


#
