import os

import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
import pyperclip
from PIL import Image
from customtkinter import CTkImage


from password_manager import PasswordManager
from utils.password_validation import PasswordValidator


class PasswordManagerUI:
    """
       Graphical User Interface (GUI) for the Password Manager.
       Allows users to log in, generate, save, search, and edit passwords.
    """

    def __init__(self):
        """
            Initializes the PasswordManagerUI class.
            Sets up the main window and displays the login screen.
        """
        self.manager = PasswordManager()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.window = ctk.CTk()
        self.window.title("Password Manager")
        self.window.geometry("862x640")

        # Load the logo image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'data', 'Password Manager (2).png')
        try:
            self.logo_image = CTkImage(Image.open(image_path), size=(200, 200))
        except Exception as e:
            print(f"Error loading image: {e}")
            self.logo_image = None

        # Language selection variable
        self.language = "English"
        self.texts = self.load_language_texts(self.language)

        # Check if it's the first run and display the appropriate screen
        if not self.manager.is_configured():
            self.show_first_run_screen()
        else:
            self.current_screen = "login"
            self.show_login_screen()

    def show_first_run_screen(self):
        """
        Displays the first-time setup screen to set a master password.
        Allows the user to input a master password, confirm it, and optionally generate a strong password.
        Includes options for changing the language.
        """
        self.current_screen = "first_run"
        self.clear_window()

        frame = ctk.CTkFrame(self.window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Language selection dropdown
        language_menu = ctk.CTkOptionMenu(
            frame,
            values=["English", "Polish"],
            command=self.change_language,
            variable=ctk.StringVar(value=self.language),
        )
        language_menu.pack(pady=10, anchor="ne", padx=10)

        # Display the logo image
        if self.logo_image:
            logo_label = ctk.CTkLabel(frame, image=self.logo_image, text="")
            logo_label.pack(pady=10)

        # Title for first run setup
        ctk.CTkLabel(
            frame,
            text=self.texts["first_run_title"],
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=20)

        # Note about the importance of remembering the password
        ctk.CTkLabel(
            frame,
            text=self.texts["password_note"],
            font=ctk.CTkFont(size=14),
            wraplength=600,
            justify="center",
        ).pack(pady=10)

        # Master password input field with toggle visibility
        master_password_entry = ctk.CTkEntry(
            frame, placeholder_text=self.texts["master_password"], show="*", width=300
        )
        master_password_entry.pack(pady=10)

        # State variable for visibility
        master_password_state = {"visible": False}

        # Button to toggle visibility
        master_password_toggle = ctk.CTkButton(
            frame,
            text="👁️",
            width=40,
            command=lambda: self.toggle_password_visibility(master_password_entry, master_password_toggle,
                                                            master_password_state),
        )
        master_password_toggle.place(relx=0.69, rely=0.658)  # Adjust position relative to the entry

        # Confirm master password input field with toggle visibility
        confirm_password_entry = ctk.CTkEntry(
            frame, placeholder_text=self.texts["confirm_password"], show="*", width=300
        )
        confirm_password_entry.pack(pady=10)

        # State variable for visibility
        confirm_password_state = {"visible": False}

        # Button to toggle visibility
        confirm_password_toggle = ctk.CTkButton(
            frame,
            text="👁️",
            width=40,
            command=lambda: self.toggle_password_visibility(confirm_password_entry, confirm_password_toggle,
                                                            confirm_password_state),
        )
        confirm_password_toggle.place(relx=0.69, rely=0.738)

        # Button to generate a strong password
        ctk.CTkButton(
            frame,
            text=self.texts["generate_password"],
            command=lambda: self.generate_password(master_password_entry, confirm_password_entry),
            width=200,
        ).pack(pady=10)

        # Button to save the master password
        ctk.CTkButton(
            frame,
            text=self.texts["save_password"],
            command=lambda: self.save_master_password(master_password_entry, confirm_password_entry),
            width=200,
        ).pack(pady=20)

    def load_language_texts(self, language):
        """
        Loads the texts for the specified language.
        """
        texts = {}
        if language == "English":
            texts = {
                "first_run_title": "Welcome to Password Manager",
                "master_password": "Enter Master Password",
                "confirm_password": "Confirm Master Password",
                "password_mismatch": "Passwords do not match. Please try again.",
                "weak_password": "Password is too weak:\n",
                "password_note": "Please remember or write down your master password. It cannot be recovered!",
                "login": "Login",
                "username": "Username",
                "password": "Password",
                "change_password": "Change Admin/User Password",
                "login_button": "Login",
                "current_password": "Current Password",
                "new_password": "New Password",
                "confirm_new_password": "Confirm New Password",
                "generate_strong_password": "Generate Strong Password",
                "save_password": "Save Password",
                "back": "Back",
                "password_manager": "Password Manager",
                "website": "Website",
                "email": "Email",
                "generate_password": "Generate Strong Password",
                "save_password_button": "Save Password",
                "view_all_passwords": "View All Passwords",
                "logout": "Logout",
                "error": "Error",
                "success": "Success",
                "invalid_credentials": "Invalid username or password.",
                "fill_all_fields": "Please fill all fields.",
                "password_saved": "Password saved successfully!",
                "copied": "Copied",
                "password_copied": "Password copied to clipboard.",
                "close": "Close",
                "update_password": "Update Password",
                "passwords_do_not_match": "Passwords do not match!",
                "password_updated": "Password updated successfully!",
                "current_password_incorrect": "Current password is incorrect!",
                "password_too_weak": "Password is too weak:\n",
                "delete_password": "Delete Password",
                "confirm_delete": "Are you sure you want to delete the password for ",
                "password_deleted": "Password deleted successfully!",
                "saved_passwords": "Saved Passwords",
                "copy_password": "Copy Password",
                "edit_password": "Edit Password",
                "delete_password_button": "Delete Password",
                "update_password_for": "Update Password for ",
                "back_to_parent": "Back",
                "language": "Language",
            }
        elif language == "Polish":
            texts = {
                "first_run_title": "Witamy w Menedżerze Haseł",
                "master_password": "Wprowadź hasło główne",
                "confirm_password": "Potwierdź hasło główne",
                "password_mismatch": "Hasła nie są takie same. Spróbuj ponownie.",
                "weak_password": "Hasło jest za słabe:\n",
                "password_note": "Zapamiętaj lub zapisz swoje hasło główne. Nie można go odzyskać!",
                "login": "Logowanie",
                "username": "Nazwa użytkownika",
                "password": "Hasło",
                "change_password": "Zmień hasło admin/użytkownika",
                "login_button": "Zaloguj się",
                "current_password": "Obecne hasło",
                "new_password": "Nowe hasło",
                "confirm_new_password": "Potwierdź nowe hasło",
                "generate_strong_password": "Generuj silne hasło",
                "save_password": "Zapisz hasło",
                "back": "Powrót",
                "password_manager": "Menadżer Haseł",
                "website": "Strona internetowa",
                "email": "Email",
                "generate_password": "Generuj silne hasło",
                "save_password_button": "Zapisz hasło",
                "view_all_passwords": "Wyświetl wszystkie hasła",
                "logout": "Wyloguj",
                "error": "Błąd",
                "success": "Sukces",
                "invalid_credentials": "Nieprawidłowa nazwa użytkownika lub hasło.",
                "fill_all_fields": "Proszę wypełnić wszystkie pola.",
                "password_saved": "Hasło zostało pomyślnie zapisane!",
                "copied": "Skopiowano",
                "password_copied": "Hasło skopiowane do schowka.",
                "close": "Zamknij",
                "update_password": "Zaktualizuj hasło",
                "passwords_do_not_match": "Hasła nie są takie same!",
                "password_updated": "Hasło zostało pomyślnie zaktualizowane!",
                "current_password_incorrect": "Obecne hasło jest niepoprawne!",
                "password_too_weak": "Hasło jest zbyt słabe:\n",
                "delete_password": "Usuń hasło",
                "confirm_delete": "Czy na pewno chcesz usunąć hasło dla ",
                "password_deleted": "Hasło zostało pomyślnie usunięte!",
                "saved_passwords": "Zapisane Hasła",
                "copy_password": "Skopiuj hasło",
                "edit_password": "Edytuj hasło",
                "delete_password_button": "Usuń hasło",
                "update_password_for": "Zaktualizuj hasło dla ",
                "back_to_parent": "Powrót",
                "language": "Język",
            }
        return texts

    def show_login_screen(self):
        """
            Displays the login screen for the user to input their username and password.
        """
        self.current_screen = "login"
        self.clear_window()

        frame = ctk.CTkFrame(self.window)
        frame.pack(fill="both", expand=True)

        # Language selection dropdown
        language_options = ["English", "Polish"]
        self.language_var = ctk.StringVar(value=self.language)
        language_menu = ctk.CTkOptionMenu(frame, values=language_options, command=self.change_language, variable=self.language_var)
        language_menu.pack(pady=10, anchor="ne", padx=10)

        # Display the logo image
        if self.logo_image:
            logo_label = ctk.CTkLabel(frame, image=self.logo_image, text="")
            logo_label.pack(pady=10)
        else:
            print("Logo image not loaded.")

            # State variable for visibility
        password_state = {"visible": False}

        # Button to toggle visibility
        password_toggle = ctk.CTkButton(
            frame,
            text="👁️",
            width=40,
            command=lambda: self.toggle_password_visibility(self.password_entry, password_toggle, password_state),
        )
        password_toggle.place(relx=0.69, rely=0.635)

        # Login Title
        ctk.CTkLabel(frame, text=self.texts["login"], font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 20))

        # Username field
        self.username_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["username"], width=300)
        self.username_entry.pack(pady=10)

        # Password field
        self.password_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["password"], show="*", width=300)
        self.password_entry.pack(pady=10)

        # Login button
        ctk.CTkButton(frame, text=self.texts["login_button"], command=self.validate_login, width=200).pack(pady=20)

        # Button for changing user password
        ctk.CTkButton(frame, text=self.texts["change_password"], command=self.show_change_user_password_screen, width=200).pack()

    def change_language(self, choice):
        """
        Changes the language of the interface.
        """
        self.language = choice
        self.texts = self.load_language_texts(self.language)

        # Refresh the current screen
        if hasattr(self, "current_screen"):
            if self.current_screen == "first_run":
                self.show_first_run_screen()
            elif self.current_screen == "login":
                self.show_login_screen()
            else:
                self.show_main_screen()

    def show_change_user_password_screen(self):
        """
        Displays the screen for changing the admin or user password.
        """
        self.clear_window()

        frame = ctk.CTkFrame(self.window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(frame, text=self.texts["change_password"], font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        # Current password field
        current_password_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["current_password"], show="*", width=300)
        current_password_entry.pack(pady=10)

        # New password field
        new_password_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["new_password"], width=300)
        new_password_entry.pack(pady=10)

        # Confirm new password field
        confirm_password_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["confirm_new_password"], width=300)
        confirm_password_entry.pack(pady=10)

        # Generate a strong password and populate both fields
        def generate_new_password():
            """
            Generates a strong password and populates both new password and confirm password fields.
            """
            new_password = self.manager.generate_strong_password()
            new_password_entry.delete(0, ctk.END)
            new_password_entry.insert(0, new_password)
            confirm_password_entry.delete(0, ctk.END)
            confirm_password_entry.insert(0, new_password)

        # Button for generating a strong password
        ctk.CTkButton(frame, text=self.texts["generate_strong_password"], command=generate_new_password, width=200).pack(pady=10)

        # Save the new admin password
        def save_new_password():
            """
            Validates and saves the new admin password if all conditions are met.
            """
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            # Validate current password
            if not self.manager.validate_current_password(current_password):
                messagebox.showerror(title=self.texts["error"], message=self.texts["current_password_incorrect"])
                return

            # Ensure new passwords match
            if new_password != confirm_password:
                messagebox.showerror(title=self.texts["error"], message=self.texts["passwords_do_not_match"])
                return

            # Validate new password strength using PasswordValidator
            is_valid, messages = PasswordValidator.validate_password_strength(new_password)
            if not is_valid:
                messagebox.showerror(title=self.texts["error"], message=self.texts["password_too_weak"] + "\n".join(messages))
                return

            # Update password logic
            result = self.manager.update_admin_password(new_password)
            if "successfully" in result.lower() or "pomyślnie" in result.lower():
                messagebox.showinfo(title=self.texts["success"], message=self.texts["password_updated"])
                self.show_login_screen()  # Redirect to log in screen after updating password
            else:
                messagebox.showerror(title=self.texts["error"], message=result)

        # Save button
        ctk.CTkButton(frame, text=self.texts["save_password"], command=save_new_password, width=150).pack(pady=10)

        # Back button
        ctk.CTkButton(frame, text=self.texts["back"], command=self.show_login_screen, width=150).pack(pady=5)

    def validate_login(self):
        """
        Validates the login credentials entered by the user.
        Grants access to the main screen if the credentials are correct.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Use PasswordManager to validate credentials
        if self.manager.validate_user_credentials(username, password):
            self.show_main_screen()
        else:
            messagebox.showerror(title=self.texts["error"], message=self.texts["invalid_credentials"])

    def show_main_screen(self):
        """
            Displays the main screen of the Password Manager with options to generate, save,
            search, and edit passwords.
        """
        self.clear_window()

        frame = ctk.CTkFrame(self.window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Main screen title
        ctk.CTkLabel(frame, text=self.texts["password_manager"], font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

        # Display the logo image
        if self.logo_image:
            logo_label = ctk.CTkLabel(frame, image=self.logo_image, text="")
            logo_label.pack(pady=10)
        else:
            print("Logo image not loaded.")

        # Website input
        self.website_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["website"], width=300)
        self.website_entry.pack(pady=10)

        # Email input
        self.email_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["email"], width=300)
        self.email_entry.pack(pady=10)

        # Password input
        self.password_entry = ctk.CTkEntry(frame, placeholder_text=self.texts["password"], width=300)
        self.password_entry.pack(pady=10)

        # Buttons for generating, saving, and viewing passwords
        ctk.CTkButton(frame, text=self.texts["generate_password"], command=lambda: self.generate_password(self.password_entry), width=200).pack(pady=10)
        ctk.CTkButton(frame, text=self.texts["save_password_button"], command=self.save_password, width=200).pack(pady=10)
        ctk.CTkButton(frame, text=self.texts["view_all_passwords"], command=self.show_password_list_screen, width=200).pack(pady=10)
        ctk.CTkButton(frame, text=self.texts["logout"], command=self.logout_user, width=200).pack(pady=10)

    def generate_password(self, *fields):
        """
        Generates a strong password and populates the provided input fields.

        Args:
            *fields: CTkEntry input fields to populate with the generated password.
        """
        try:
            password = self.manager.generate_strong_password()
            for field in fields:
                if field:  # Ensure the field is valid
                    field.delete(0, ctk.END)  # Clear the field
                    field.insert(0, password)  # Insert the generated password
        except Exception as e:
            print(f"Error generating password: {e}")

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
            messagebox.showerror(title=self.texts["error"], message=self.texts["fill_all_fields"])
            return

        # Save password using PasswordManager
        result = self.manager.save_password(website, email, password)

        # Display result to the user
        if "successfully" in result.lower() or "pomyślnie" in result.lower():
            messagebox.showinfo(title=self.texts["success"], message=self.texts["password_saved"])
            self.clear_input_fields()
        else:
            messagebox.showerror(title=self.texts["error"], message=result)

    def clear_input_fields(self):
        """
        Clears the input fields for website, email, and password after an action.
        """
        self.website_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)

    def logout_user(self):
        """
        Logs out the user from the database.
        """
        self.clear_window()
        self.show_login_screen()

    def clear_window(self):
        """
            Clears all widgets from the main application window.
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def show_password_list_screen(self):
        """
        Displays a new window with a list of all saved passwords.
        Provides options to copy, update, and delete passwords.
        """
        # New window
        password_window = ctk.CTkToplevel(self.window)
        password_window.title(self.texts["saved_passwords"])
        password_window.geometry("800x600")

        # Bring the window to the front
        password_window.lift()
        password_window.attributes('-topmost', True)
        password_window.after_idle(password_window.attributes, '-topmost', False)

        ctk.CTkLabel(password_window, text=self.texts["saved_passwords"], font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Frame for Treeview and buttons
        frame = ctk.CTkFrame(password_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Style for Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=30, font=('Arial', 20))
        style.configure("Treeview.Heading", font=('Arial', 20, 'bold'))
        style.map('Treeview', background=[('selected', '#1E90FF')])

        # Create Treeview
        columns = (self.texts["website"], self.texts["email"], self.texts["password"])
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.heading(self.texts["website"], text=self.texts["website"])
        tree.heading(self.texts["email"], text=self.texts["email"])
        tree.heading(self.texts["password"], text=self.texts["password"])
        tree.column(self.texts["website"], width=200)
        tree.column(self.texts["email"], width=200)
        tree.column(self.texts["password"], width=200)

        # Fetch passwords
        passwords = self.manager.get_passwords()
        for password_data in passwords:
            website, email, password = password_data
            tree.insert('', 'end', values=(website, email, password))

        tree.pack(fill="both", expand=True)

        # Function to copy password
        def copy_password():
            selected_item = tree.selection()
            if selected_item:
                password = tree.item(selected_item)['values'][2]
                pyperclip.copy(password)
                messagebox.showinfo(self.texts["copied"], self.texts["password_copied"])
            else:
                messagebox.showerror(self.texts["error"], self.texts["fill_all_fields"])

        # Function to edit password
        def edit_password():
            selected_item = tree.selection()
            if selected_item:
                item = tree.item(selected_item)
                website = item['values'][0]
                email = item['values'][1]
                self.show_update_password_screen(website, email, password_window)
            else:
                messagebox.showerror(self.texts["error"], self.texts["fill_all_fields"])

        # Function to delete password
        def delete_password():
            selected_item = tree.selection()
            if selected_item:
                website = tree.item(selected_item)['values'][0]
                confirm = messagebox.askyesno(self.texts["delete_password"], f"{self.texts['confirm_delete']}{website}?")
                if confirm:
                    result = self.manager.delete_password(website)
                    if "successfully" in result.lower() or "pomyślnie" in result.lower():
                        messagebox.showinfo(self.texts["success"], self.texts["password_deleted"])
                        password_window.destroy()
                        self.show_password_list_screen()  # Refresh the list after deletion
                    else:
                        messagebox.showerror(self.texts["error"], result)
            else:
                messagebox.showerror(self.texts["error"], self.texts["fill_all_fields"])

        # Buttons for actions
        button_frame = ctk.CTkFrame(password_window)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text=self.texts["copy_password"], command=copy_password, width=150).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text=self.texts["edit_password"], command=edit_password, width=150).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text=self.texts["delete_password_button"], command=delete_password, width=150).pack(side="left", padx=10)
        ctk.CTkButton(password_window, text=self.texts["close"], command=password_window.destroy, width=150).pack(pady=10)

    def show_update_password_screen(self, website, email, parent_window):
        """
        Displays a screen for updating the password for the given website and email.
        """
        # Create a new window for updating the password
        update_window = ctk.CTkToplevel(self.window)
        update_window.title(f"{self.texts['update_password_for']}{website}")
        update_window.geometry("400x300")

        # Header
        ctk.CTkLabel(update_window, text=f"{self.texts['update_password_for']}{website}", font=ctk.CTkFont(size=16)).pack(pady=10)

        # Input field for the new password
        new_password_entry = ctk.CTkEntry(update_window, placeholder_text=self.texts["new_password"], width=300)
        new_password_entry.pack(pady=5)

        # Input field for confirming the new password
        confirm_password_entry = ctk.CTkEntry(update_window, placeholder_text=self.texts["confirm_new_password"], width=300)
        confirm_password_entry.pack(pady=5)

        # Function to generate a strong password and populate the fields
        def generate_new_password():
            """
            Generates a strong password and populates both new password and confirm password fields.
            """
            new_password = self.manager.generate_strong_password()
            new_password_entry.delete(0, ctk.END)
            new_password_entry.insert(0, new_password)
            confirm_password_entry.delete(0, ctk.END)
            confirm_password_entry.insert(0, new_password)

        # Button for generating a strong password
        ctk.CTkButton(update_window, text=self.texts["generate_password"], command=generate_new_password).pack(pady=5)

        # Function to handle the password update process
        def update_password():
            """
            Validates the new password and updates it in the database if valid.
            Closes the current window and returns to the parent window.
            """
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            # Ensure passwords match
            if new_password != confirm_password:
                messagebox.showerror(self.texts["error"], self.texts["passwords_do_not_match"])
                return

            # Validate new password strength using PasswordValidator
            is_valid, messages = PasswordValidator.validate_password_strength(new_password)
            if not is_valid:
                messagebox.showerror(self.texts["error"], self.texts["password_too_weak"] + "\n".join(messages))
                return

            # Update the password using the manager
            result = self.manager.update_password(website, new_password)
            if "successfully" in result.lower() or "pomyślnie" in result.lower():
                messagebox.showinfo(self.texts["success"], self.texts["password_updated"])
                update_window.destroy()  # Close the update password window
                parent_window.deiconify()  # Restore the parent window
                parent_window.destroy()
                self.show_password_list_screen()  # Refresh the list
            else:
                messagebox.showerror(self.texts["error"], result)

        # Button to update the password
        ctk.CTkButton(update_window, text=self.texts["update_password"], command=update_password).pack(pady=10)

        # Button to cancel the operation and go back
        def cancel_update():
            """
            Closes the update password window and restores the parent window.
            """
            update_window.destroy()
            parent_window.deiconify()

        # Back button
        ctk.CTkButton(update_window, text=self.texts["back_to_parent"], command=cancel_update).pack(pady=5)

        # Hide the parent window while editing
        parent_window.withdraw()

    def save_master_password(self, master_password_entry, confirm_password_entry):
        """
        Saves the master password after validating it.

        Args:
            master_password_entry (CTkEntry): The field for entering the master password.
            confirm_password_entry (CTkEntry): The field for confirming the master password.
        """
        master_password = master_password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Validate that the passwords match
        if master_password != confirm_password:
            messagebox.showerror(title=self.texts["error"], message=self.texts["password_mismatch"])
            return

        # Validate the strength of the password
        is_valid, messages = PasswordValidator.validate_password_strength(master_password)
        if not is_valid:
            messagebox.showerror(title=self.texts["error"], message=self.texts["weak_password"] + "\n".join(messages))
            return

        # Save the master password
        self.manager.save_master_password(master_password)
        self.manager.mark_as_configured()

        messagebox.showinfo(title=self.texts["success"], message=self.texts["password_saved"])

        # Redirect to login screen after setting the password
        self.show_login_screen()

    def run(self):
        """
            Starts the Tkinter event loop to run the application.
        """
        self.window.mainloop()

    def toggle_password_visibility(self, entry, button, state):
        """
        Toggles the visibility of the password in the entry field.

        Args:
            entry: The CTkEntry field containing the password.
            button: The button used to toggle the visibility.
            state: A mutable variable (list or dictionary) tracking the visibility state.
        """
        if state["visible"]:
            entry.configure(show="*")  # Hide password
            button.configure(text="👁️")
            state["visible"] = False
        else:
            entry.configure(show="")  # Show password
            button.configure(text="👁️‍🗨️")
            state["visible"] = True


if __name__ == "__main__":
    ui = PasswordManagerUI()
    ui.run()
