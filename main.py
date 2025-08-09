from tkinter import *
from tkinter import messagebox
from random import choice,randint,shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password_gen = "".join(password_list)
    password_input.insert(END, password_gen)
    pyperclip.copy(password_gen)

    def check_password():
        if len(password_input.get()) > 0:
            generate_password_button.config(state=DISABLED)

        else:
            generate_password_button.config(state=NORMAL)

        window.after(100, check_password)
    check_password()

# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_password():
    website = website_input.get()
    password = password_input.get()
    email = email_username_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Fill in all the lines")
    else:

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except(FileNotFoundError, json.decoder.JSONDecodeError):
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

#-----------------------------Find password-----------------------------#

def find_password():
    website = website_input.get().strip()
    if not website:
        messagebox.showinfo(title="Oops", message="Please enter a website name")
        return
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No data file found")
        return

    if website in data:
        email = data[website]['email']
        password = data[website]['password']
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)

    else:
        messagebox.showinfo(title="Error", message=f"No details found for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1, columnspan=2)

# -------------- Labels ------------------------------- #
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

email_username = Label(text="Email/Username:")
email_username.grid(row=2, column=0, sticky="e", padx=5, pady=5)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

# ---------------- Entries ---------------------- #
website_input = Entry(width=21)
website_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")
website_input.focus()

email_username_input = Entry(width=43)
email_username_input.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
email_username_input.insert(0, "aka@gmail.com")

password_input = Entry(width=21)
password_input.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# --------------- Buttons ---------------------- #
generate_password_button = Button(text="Generate", width=16, command=create_password)
generate_password_button.grid(row=3, column=2, padx=5, pady=5)

add_button = Button(text="Add", width=36, command=add_password)
add_button.grid(row=4, column=1, columnspan=2, pady=5)

search_button = Button(text="Search", width=16, command=find_password)
search_button.grid(row=1, column=2, padx=5, pady=5)

window.mainloop()
