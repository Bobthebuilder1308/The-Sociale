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
    """Save data to a file."""
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
    """Change the theme of the application."""
    global current_theme
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
    """Open a new page with input fields."""
    global new_window, age_entry, group_size_entry, activity_var, budget_var, budget_label
    new_window = customtkinter.CTkToplevel(root)
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

def format_budget(value):
    """Format the budget value."""
    return f"{value}₹"

def submit_form(age_entry, group_size_entry, activity_var, budget_var, budget_label):
    """Submit the form data."""
    budget = budget_var.get()
    budget_label.configure(text=f"Budget: {format_budget(budget)}")
    age = age_entry.get()
    group_size = group_size_entry.get()
    activity = activity_var.get()

    # Save all details to group_activity_data.txt
    data_file = "group_activity_data.txt"
    with open(data_file, "a") as file:
        file.write(f"Age: {age}\n")
        file.write(f"Group Size: {group_size}\n")
        file.write(f"Activity: {activity}\n")
        file.write(f"Budget: {budget}\n\n")
    print(f"Data saved successfully to {data_file}")

    # Save activity and budget to work_data.txt
    work_data = f"{activity}: {budget}\n"
    with open("work_data.txt", "a") as work_file:
        work_file.write(work_data)
    print(f"Data saved successfully to group_activity_data.txt and work_data.txt")

root = customtkinter.CTk()
root.title("The Sociale")
button = customtkinter.CTkButton(master=root, text="Welcome To Sociale (We Are Working on the name)", command=open_new_page)
root.geometry("500x500")
button.place(relx=0.5, rely=0.5, anchor="center")
theme_button = customtkinter.CTkButton(master=root, text="Theme")
theme_button.place(relx=1, rely=0, anchor="ne")
theme_button.bind("<Button-1>", change_theme)
root.configure(fg_color=dark_theme["fg_color"], bg=dark_theme["bg"])

def parse_activity_data(filename, activity_name):
    """Parse activity data from a file."""
    data = {}
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return data
    try:
        with open(filename, "r") as file:
            current_activity = None
            for line in file:
                line = line.strip()
                if line.isupper():
                    current_activity = line
                elif current_activity and current_activity == activity_name:
                    data[current_activity] = []
                    for detail in file:
                        detail = detail.strip()
                        if not detail or detail.isupper():
                            break
                        place, price = detail.split(": ", 1)
                        try:
                            price = float(price.strip("₹"))
                        except ValueError:
                            print(f"Warning: Invalid price format for {place} in {filename}. Skipping.")
                            continue
                        data[current_activity].append((place, price))
                    break
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    return data
root.mainloop()