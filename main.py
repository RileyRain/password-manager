from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

color_themes = {
    "light": {
        "text": "black",
        "bg": "white"
    },
    "dark": {
        "text": "red",
        "bg": "black"
    }
}

theme = "light"


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(END, password)
    pyperclip.copy(password)


def dark_mode():
    global theme
    theme = "dark"
    update_theme()
    return theme


def light_mode():
    global theme
    theme = "light"
    update_theme()
    return theme


def update_theme():
    window.config(bg=color_themes[theme]["bg"])
    canvas.config(bg=color_themes[theme]["bg"])
    search_button.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    add_button.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    generate_password_button.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    password_label.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    website_label.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    username_label.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    blank_1.config(bg=color_themes[theme]["bg"])
    website_input.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    username_input.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])
    password_input.config(bg=color_themes[theme]["bg"], fg=color_themes[theme]["text"])


def save():
    website_value = website_input.get()
    username_value = username_input.get()
    password_value = password_input.get()
    new_data = {
        website_value: {
            "email": username_value,
            "password": password_value
        }
    }
    # Check if user filled all entries
    if website_value and username_value and password_value:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)
    # Error if entries not filled out
    else:
        messagebox.showinfo(title="Error", message="Please fill out all values and try again")


def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            website_value = website_input.get()
            website_value = website_value.lower()
            if website_value:
                if website_value in data:
                    email = data[website_value]["email"]
                    password = data[website_value]["password"]
                    pyperclip.copy(password)
                    messagebox.showinfo(title="Website found", message=f"The email is: {email}.\n"
                                                                       f"The password is: {password}.\n"
                                                                       f"Password has been copied to clipboard.")
                else:
                    messagebox.showinfo(title="Error", message="Website not found in passwords.\n "
                                                               "make sure the spelling "
                                                               "is correct, or use the 'add' button "
                                                               "to save a new password.")
            else:
                messagebox.showinfo(title="Error", message="Website box must be filled to search")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No passwords found.\n"
                                                   "Please save a new password using the 'add' button.")


window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

# Graphic
logo = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200, highlightthickness=0)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
blank_1 = Label(text="")
blank_1.grid(column=0, row=5)

# Entries
website_input = Entry(width=20)
website_input.grid(column=1, row=1)
website_input.focus()
username_input = Entry(width=38)
username_input.grid(column=1, row=2, columnspan=2)
password_input = Entry(width=20)
password_input.grid(column=1, row=3)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=32, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", command=find_password, width=13)
search_button.grid(column=2, row=1)
dark_mode_button = Button(text="Dark mode", command=dark_mode, bg="black", fg="red")
dark_mode_button.grid(column=0, row=6)
light_mode_button = Button(text="Light mode", command=light_mode)
light_mode_button.grid(column=2, row=6)

update_theme()

window.mainloop()
