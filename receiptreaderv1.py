#reciept reader v1
#this is a simple reciept reader that allows the user to enter the seller's name, amount, and date of purchase
#the data is then saved to a csv file
#the user can then view the data in the csv file
#The inputs are processed via a tkinter GUI
#Quazi Heider
#March 24, 2025

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
class ReceiptReaderMainScreen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Receipt Reader")
        self.window.geometry("600x600")

        # Create main frame to center everything
        main_frame = tk.Frame(self.window)
        # Add top padding to push content to middle
        main_frame.pack(expand=True)

        #create title and version labels
        self.title_label = tk.Label(main_frame, text="Finance Tracker", font=("Arial", 24))
        self.title_label.pack(pady=10)
        self.version_label = tk.Label(main_frame, text="v1.0", font=("Arial", 12))
        self.version_label.pack(pady=(0, 20))  # More padding below version

        # Button frame for all buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)

        #create a button to add an entry
        self.add_entry_button = tk.Button(button_frame, text="Add Entry", command=lambda: AddEntry())
        self.add_entry_button.pack(pady=10)

        #create a button to view entries
        self.view_entries_button = tk.Button(button_frame, text="View Entries", command=lambda: ViewEntries())
        self.view_entries_button.pack(pady=10)

        #create a button to exit, move this to the top left corner of the window
        
        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.quit)
        self.exit_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
        
class AddEntry:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Receipt Reader")
        self.window.geometry("600x600")

        # Create main frame to center everything
        main_frame = tk.Frame(self.window)
        main_frame.pack(expand=True)

        #input field
        #seller info:   
        tk.Label(main_frame, text="Seller Name:").pack(pady=5)
        self.seller_entry = tk.Entry(main_frame)
        self.seller_entry.pack(pady=5)

        #amount info
        tk.Label(main_frame, text="Amount Paid:").pack(pady=5)
        self.amount_entry = tk.Entry(main_frame)
        self.amount_entry.pack(pady=5)

        #date info
        tk.Label(main_frame, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = tk.Entry(main_frame)
        self.date_entry.pack(pady=5)

        #submit button
        submit = tk.Button(main_frame, text="Submit", command=self.submit)
        submit.pack(pady=15)

    def submit(self):
        self.verify()
        self.clear_fields()

    def verify(self):
        #seller
        self.seller = self.seller_entry.get()
        if not self.seller:
            messagebox.showerror("Error", "Seller name cannot be empty")
            return
        #amount
        try: 
            self.amount = float(self.amount_entry.get())
            if self.amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        #date
        try:
            self.date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format")
            return
        
        #send to file if all validations pass
        self.toCSVFile()
        messagebox.showinfo("Success", "Receipt data saved successfully")
        self.window.destroy()
    
    def clear_fields(self):
        #clear fields for next entry
        self.seller_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def toCSVFile(self):
        with open("recieptEntries.txt", "a") as file:
            # Only write header if file is empty
            if file.tell() == 0:
                file.write('seller,amount,date\n')
            file.write(f'{self.seller},{self.amount},{self.date}\n')

class ViewEntries:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Edit Entry")
        self.window.geometry("600x600")
        
        main_frame = tk.Frame(self.window)
        main_frame.pack(expand=True)

        #Create a back button in the top left corner
        back_button = tk.Button(main_frame, text="Back", command=self.window.destroy)
        back_button.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Create a frame to hold the scrollable list
        list_frame = tk.Frame(self.window)
        list_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Create scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create listbox
        self.entries_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.entries_list.pack(side=tk.LEFT, fill='both', expand=True)

        # Configure scrollbar
        scrollbar.config(command=self.entries_list.yview)

        # Read and display entries from file
        try:
            with open("recieptEntries.txt", "r") as file:
                entries = file.readlines()
                if len(entries) > 0:
                    # Format and display header
                    header = "Seller                          Amount         Date"
                    self.entries_list.insert(tk.END, header)
                    self.entries_list.insert(tk.END, "-" * 54)  # Separator line
                    
                    # Display data rows (skip header row from file)
            
                    for entry in entries[1:]:
                    
                        parts = entry.strip().split(',')
                        if len(parts) == 3:
                            seller, amount, date = parts
                            formatted_entry = f"{seller:<30} ${amount:>10} {date:>12}"
                            self.entries_list.insert(tk.END, formatted_entry)
        except FileNotFoundError:
            messagebox.showerror("Error", "No entries found")

class storeDataValues:
    def __init__(self):
        self.sellers = []
        self.amounts = []
        self.dates = []

   

        
        
if __name__ == "__main__":
    app = ReceiptReaderMainScreen()
    app.window.mainloop()
