import tkinter as tk
from tkinter import messagebox
from password_manager import PasswordManager

class PasswordManagerUI:
    """
       Graphical User Interface (GUI) for the Password Manager.
       Allows users to log in, generate, save, and search passwords.
    """

    def __init__(self):
        """
            Initializes the PasswordManagerUI class.
            Sets up the main window and displays the login screen.
        """
        self.manager = PasswordManager()
        self.window = tk.Tk()
        self.window.title("Password Manager")
        self.window.geometry("400x400")

        # Start with login screen
        self.show_login_screen()

    def show_login_screen(self):
        """
            Displays the login screen for the user to input their username and password.
        """

        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Login title
        tk.Label(self.window, text="Login", font=("Arial", 16)).pack(pady=10)

        # Username field
        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window, font=("Arial", 16))
        self.username_entry.pack()

        # Password field
        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, font=("Arial", 16), show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(self.window, text="Login", command=self.validate_login).pack(pady=10)

    def validate_login(self):
        """
            Validates the login credentials entered by the user.
            Grants access to the main screen if the credentials are correct.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Temporary hardcoded credentials
        if username == "admin" and password == "password123":
            self.show_main_screen()
        else:
            # Display error if credentials are invalid
            messagebox.showerror("Error", "Incorrect username or password.")

    def show_main_screen(self):
        """
            Displays the main screen of the Password Manager with options to generate, save,
            and search for passwords.
        """
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Main screen title
        tk.Label(self.window, text="Password Manager", font=("Arial", 16)).pack(pady=10)

        # Website input
        tk.Label(self.window, text="Website").pack()
        self.website_entry = tk.Entry(self.window, font=("Arial", 16))
        self.website_entry.pack(pady=5)

        # Email input
        tk.Label(self.window, text="Email").pack()
        self.email_entry = tk.Entry(self.window, font=("Arial", 16))
        self.email_entry.pack(pady=5)

        # Password input
        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, font=("Arial", 16))
        self.password_entry.pack(pady=5)

        # Buttons for generating, saving, and searching passwords
        tk.Button(self.window, text="Generate Strong Password", command=self.generate_password).pack(pady=5)
        tk.Button(self.window, text="Save Password", command=self.save_password).pack(pady=5)
        tk.Button(self.window, text="Search Password", command=self.search_password).pack(pady=5)

        # Label to display search result
        self.result_label = tk.Label(self.window, text="", font=("Arial", 16), fg="red")
        self.result_label.pack(pady=10)

    def generate_password(self):
        """
            Generates a strong password and displays it in the password field.
        """
        password = self.manager.generate_strong_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save_password(self):
        """
            Saves the entered website, email, and password to the database.
            Validates that all fields are filled before saving.
        """
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if all fields are filled
        if not website or not email or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        # Save password using PasswordManager
        result = self.manager.save_password(website, email, password)

        # Display result to the user
        tk.messagebox.showinfo("Save Password", result)

        # Clear input fields if the password was saved successfully
        if "successfully" in result.lower():
            self.clear_input_fields()


    def search_password(self):
            """
                Searches for a password by the entered website.
                Displays the result in the result_label.
            """
            website = self.website_entry.get()

            # Check if the website field is filled
            if not website:
                messagebox.showerror("Error", "Please enter a website to search!")
                return

            # Search for the password using PasswordManager and display result
            result = self.manager.search_password(website)
            self.result_label.config(text=result)

    def clear_input_fields(self):
        """
        Clears the input fields for website, email, and password after an action.
        """
        self.website_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def run(self):
        """
            Starts the Tkinter event loop to run the application.
        """
        self.window.mainloop()

if __name__ == "__main__":
    ui = PasswordManagerUI()
    ui.run()

