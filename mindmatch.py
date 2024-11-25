import tkinter as tk
from tkinter import ttk
import os

# Therapist data with details including images
therapists = [
    {"name": "Dr. John Smith", "specialty": "Anxiety", "gender": "Male", "image": "male_icon.gif", "phone": "555-123-4567"},
    {"name": "Dr. Sarah Lee", "specialty": "Anxiety", "gender": "Female", "image": "female_icon.gif", "phone": "555-987-6543"},
    {"name": "Dr. Mark Green", "specialty": "Depression", "gender": "Male", "image": "male_icon.gif", "phone": "555-456-7890"},
    {"name": "Dr. Emily White", "specialty": "Depression", "gender": "Female", "image": "female_icon.gif", "phone": "555-654-3210"},
    {"name": "Dr. Alex Brown", "specialty": "PTSD", "gender": "Male", "image": "male_icon.gif", "phone": "555-234-5678"},
    {"name": "Dr. Laura Gray", "specialty": "PTSD", "gender": "Female", "image": "female_icon.gif", "phone": "555-876-5432"},
    {"name": "Dr. Michael Johnson", "specialty": "Substance Abuse", "gender": "Male", "image": "male_icon.gif", "phone": "555-345-6789"},
    {"name": "Dr. Lily Adams", "specialty": "Substance Abuse", "gender": "Female", "image": "female_icon.gif", "phone": "555-765-4321"},
]

# Global variables
gender_var = None
specialty_var = None
saved_therapists = []  # List to store saved therapists, persists across screens
therapist_images = {}
bg_color = "#d0f0f8"
previous_screen = None

# Function to load therapist images
def load_images():
    """Loads images for therapists into memory."""
    global therapist_images
    for therapist in therapists:
        image_path = therapist["image"]
        if os.path.exists(image_path):
            try:
                therapist_images[image_path] = tk.PhotoImage(file=image_path)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
        else:
            print(f"Image file not found: {image_path}")

# Function to clear all widgets from the screen
def clear_screen():
    """Removes all widgets currently displayed on the screen."""
    for widget in root.winfo_children():
        widget.destroy()

# Function to create a scrollable frame
def create_scrollable_frame(parent):
    """Creates a scrollable frame to display content."""
    canvas = tk.Canvas(parent, bg=bg_color)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame

# Function to create the hamburger menu
def create_hamburger_menu(parent):
    """Creates a dropdown menu accessible via a hamburger button."""
    menu_button = tk.Button(parent, text="☰", font=("Arial", 16), command=lambda: menu.tk_popup(menu_button.winfo_rootx(), menu_button.winfo_rooty() + 30))
    menu_button.pack(anchor="nw", padx=10, pady=10)

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Home", command=show_main_screen)
    if previous_screen:
        menu.add_command(label="Back", command=previous_screen)
    menu.add_command(label="View Saved Therapists", command=show_saved_therapists_screen)

# Function to display the main screen
def show_main_screen():
    """Displays the main screen with options to find or view saved therapists."""
    global previous_screen
    previous_screen = None
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Welcome to MindMatch", font=("Helvetica", 20), bg=bg_color).pack(pady=50)
    tk.Button(root, text="Find a Therapist", command=show_gender_screen).pack(pady=5)
    tk.Button(root, text="View Saved Therapists", command=show_saved_therapists_screen).pack(pady=5)

# Function to display the gender selection screen
def show_gender_screen():
    """Displays the screen for selecting the gender of the therapist."""
    global previous_screen, gender_var
    previous_screen = show_main_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Choose Gender", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    gender_var = tk.StringVar(value="Any")
    tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", bg=bg_color).pack(pady=5)
    tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", bg=bg_color).pack(pady=5)
    tk.Radiobutton(root, text="Any", variable=gender_var, value="Any", bg=bg_color).pack(pady=5)

    tk.Button(root, text="Submit", command=show_specialty_screen).pack(pady=20)

# Function to display the specialty selection screen
def show_specialty_screen():
    """Displays the screen for selecting the specialty of the therapist."""
    global previous_screen, specialty_var
    previous_screen = show_gender_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Choose Specialty", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    specialties = ["Anxiety", "Depression", "PTSD", "Family Therapy", "Substance Abuse"]
    specialty_var = tk.StringVar(value="Select a Specialty")
    ttk.Combobox(root, textvariable=specialty_var, values=specialties, state="readonly").pack(pady=20)

    tk.Button(root, text="Submit", command=show_results_screen).pack(pady=20)

# Function to display the results screen
def show_results_screen():
    """Displays therapists based on user-selected gender and specialty."""
    global previous_screen
    previous_screen = show_specialty_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Therapist Results", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    scrollable_frame = create_scrollable_frame(root)

    gender = gender_var.get()
    specialty = specialty_var.get()
    results = [
        t for t in therapists
        if (t["gender"] == gender or gender == "Any") and t["specialty"] == specialty
    ]

    if not results:
        tk.Label(scrollable_frame, text="No therapists found.", bg=bg_color).pack(pady=10)
        return

    for i, therapist in enumerate(results):
        frame = tk.Frame(scrollable_frame, bg=bg_color)
        frame.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        img = therapist_images.get(therapist["image"])
        if img:
            tk.Label(frame, image=img, bg=bg_color).pack()

        info = f"{therapist['name']}\n{therapist['phone']}"
        tk.Label(frame, text=info, bg=bg_color).pack()

        tk.Button(frame, text="Save", command=lambda t=therapist: save_therapist(t)).pack()

# Function to save a therapist
def save_therapist(therapist):
    """Adds the selected therapist to the saved therapists list."""
    if therapist not in saved_therapists:
        saved_therapists.append(therapist)
        print(f"Saved: {therapist['name']}")

# Function to display the saved therapists screen
def show_saved_therapists_screen():
    """Displays the list of saved therapists."""
    global previous_screen
    previous_screen = show_results_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Saved Therapists", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    scrollable_frame = create_scrollable_frame(root)

    if not saved_therapists:
        tk.Label(scrollable_frame, text="No therapists saved yet.", bg=bg_color).pack(pady=10)
        return

    for i, therapist in enumerate(saved_therapists):
        frame = tk.Frame(scrollable_frame, bg=bg_color)
        frame.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        img = therapist_images.get(therapist["image"])
        if img:
            tk.Label(frame, image=img, bg=bg_color).pack()

        info = f"{therapist['name']}\n{therapist['phone']}"
        tk.Label(frame, text=info, bg=bg_color).pack()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MindMatch")
    root.geometry("600x400")
    load_images()
    show_main_screen()
    root.mainloop()