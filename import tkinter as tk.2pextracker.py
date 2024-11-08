import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry('550x1000')
        self.root.title("PE'X")
        self.root.configure(bg='#5E9387')

        self.salary = 0
        self.total_expenses = 0
        self.expenses = []
        self.category_limits = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Other": 0}
        self.recurring_expenses = []

        self.create_main_screen()

    def create_main_screen(self):
        self.clear_screen()

        # Optional Salary Input Section
        self.var_include_salary = tk.BooleanVar()
        self.check_include_salary = tk.Checkbutton(
            self.root, text="Include Salary Input", variable=self.var_include_salary, 
            bg='#5E9387', fg='#CEE9B6', command=self.toggle_salary_input
        )
        self.check_include_salary.pack(pady=5)

        self.salary_frame = tk.Frame(self.root, bg='#5E9387')
        self.label_salary = tk.Label(self.salary_frame, text="Enter Your Salary:", bg='#5E9387', fg='#CEE9B6')
        self.label_salary.pack(pady=5)

        self.entry_salary = tk.Entry(self.salary_frame)
        self.entry_salary.pack(pady=5)

        self.button_done_salary = tk.Button(self.salary_frame, text="Done", command=self.set_salary)
        self.button_done_salary.pack(pady=5)

        self.salary_frame.pack_forget()  # Hide salary input initially

        # Display the Salary
        self.label_display_salary = tk.Label(self.root, text="Salary: ₱0.00", bg='#5E9387', fg='#CEE9B6')
        self.label_display_salary.pack(pady=5)

        # Category Limits Input Section
        self.label_category_limits = tk.Label(self.root, text="Set Expense Category Limits:", bg='#5E9387', fg='#CEE9B6')
        self.label_category_limits.pack(pady=5)

        self.label_food_limit = tk.Label(self.root, text="Food Limit:", bg='#5E9387', fg='#CEE9B6')
        self.label_food_limit.pack(pady=5)
        self.entry_food_limit = tk.Entry(self.root)
        self.entry_food_limit.pack(pady=5)

        self.label_transportation_limit = tk.Label(self.root, text="Transportation Limit:", bg='#5E9387', fg='#CEE9B6')
        self.label_transportation_limit.pack(pady=5)
        self.entry_transportation_limit = tk.Entry(self.root)
        self.entry_transportation_limit.pack(pady=5)

        self.label_entertainment_limit = tk.Label(self.root, text="Entertainment Limit:", bg='#5E9387', fg='#CEE9B6')
        self.label_entertainment_limit.pack(pady=5)
        self.entry_entertainment_limit = tk.Entry(self.root)
        self.entry_entertainment_limit.pack(pady=5)

        self.label_other_limit = tk.Label(self.root, text="Other Limit:", bg='#5E9387', fg='#CEE9B6')
        self.label_other_limit.pack(pady=5)
        self.entry_other_limit = tk.Entry(self.root)
        self.entry_other_limit.pack(pady=5)

        self.button_set_limits = tk.Button(self.root, text="Set Category Limits", command=self.set_category_limits)
        self.button_set_limits.pack(pady=5)

        # Expense Input Section
        self.label_category = tk.Label(self.root, text="Expense Category:", bg='#5E9387', fg='#CEE9B6')
        self.label_category.pack(pady=5)

        self.category_var = tk.StringVar(value="Food")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, "Food", "Transportation", "Entertainment", "Other")
        self.category_menu.pack(pady=5)

        self.label_expense = tk.Label(self.root, text="Enter Expense Amount:", bg='#5E9387', fg='#CEE9B6')
        self.label_expense.pack(pady=5)
        self.entry_expense = tk.Entry(self.root)
        self.entry_expense.pack(pady=5)

        self.button_add_expense = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.button_add_expense.pack(pady=5)

        self.listbox = tk.Listbox(self.root, width=50, height=10)
        self.listbox.pack(pady=5)

        self.total_label = tk.Label(self.root, text=f"Total Expenses: ₱0.00", bg='#5E9387', fg='#CEE9B6')
        self.total_label.pack(pady=5)

        self.remaining_label = tk.Label(self.root, text=f"Remaining Salary: ₱0.00", bg='#5E9387', fg='#CEE9B6')
        self.remaining_label.pack(pady=5)

        self.button_analyze = tk.Button(self.root, text="Analyze Expenses", command=self.analyze_expenses)
        self.button_analyze.pack(pady=5)

        self.button_exit = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.button_exit.pack(pady=5)

    def toggle_salary_input(self):
        if self.var_include_salary.get():
            self.salary_frame.pack(pady=5)
        else:
            self.salary_frame.pack_forget()
            self.salary = 0
            self.update_totals()

    def set_salary(self):
        try:
            self.salary = float(self.entry_salary.get())
            self.label_display_salary.config(text=f"Salary: ₱{self.salary:.2f}")
            self.update_totals()
            self.salary_frame.pack_forget()  # Hide salary input after "Done" is clicked
        except ValueError:
            messagebox.showerror("Error", "Invalid salary input.")

    def set_category_limits(self):
        try:
            self.category_limits["Food"] = float(self.entry_food_limit.get())
            self.category_limits["Transportation"] = float(self.entry_transportation_limit.get())
            self.category_limits["Entertainment"] = float(self.entry_entertainment_limit.get())
            self.category_limits["Other"] = float(self.entry_other_limit.get())
            messagebox.showinfo("Category Limits", "Category limits set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid category limit input. Please enter numeric values.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def add_expense(self):
        try:
            expense = float(self.entry_expense.get())
            if expense <= 0:
                raise ValueError("Expense must be positive.")

            category = self.category_var.get()

            # Check if the expense exceeds the category limit
            if expense + self.get_category_total(category) > self.category_limits[category]:
                messagebox.showerror("Error", f"{category} expense exceeds the limit of ₱{self.category_limits[category]}")
                return

            self.expenses.append((category, expense))
            self.listbox.insert(tk.END, f"{category}: ₱{expense:.2f}")
            self.total_expenses += expense
            self.entry_expense.delete(0, tk.END)
            self.update_totals()

        except ValueError:
            messagebox.showerror("Error", "Invalid expense input.")

    def get_category_total(self, category):
        # Calculate total for a specific category
        total = sum(expense for cat, expense in self.expenses if cat == category)
        return total

    def update_totals(self):
        remaining_salary = self.salary - self.total_expenses
        self.total_label.config(text=f"Total Expenses: ₱{self.total_expenses:.2f}")
        self.remaining_label.config(text=f"Remaining Salary: ₱{remaining_salary:.2f}")

            # Calculate total of recurring expenses and check limits
        total_recurring = 0
        for name, amount, limit in self.recurring_expenses:
            total_recurring += amount
            if total_recurring > limit:
                messagebox.showwarning("Warning", f"You are exceeding the limit for {name}!")

        self.total_expenses += total_recurring  # Include recurring in total expenses

    def analyze_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Analysis", "No expenses recorded yet.")
            return

        categories = {}
        for category, amount in self.expenses:
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        labels = list(categories.keys())
        sizes = list(categories.values())

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution')
        plt.axis('equal')
        plt.show()

    def open_recurring_expenses_window(self):
        self.recurring_window = tk.Toplevel(self.root)
        self.recurring_window.geometry("450x800")
        self.recurring_window.title("Recurring Expenses")
        self.recurring_window.configure(bg='#5E9387')

        self.label_recurring = tk.Label(self.recurring_window, text="Recurring Expense:", bg='#5E9387', fg='#CEE9B6')
        self.label_recurring.pack(pady=5)
        self.entry_recurring_expense = tk.Entry(self.recurring_window)
        self.entry_recurring_expense.pack(pady=5)

        self.label_recurring_amount = tk.Label(self.recurring_window, text="Amount:", bg='#5E9387', fg='#CEE9B6')
        self.label_recurring_amount.pack(pady=5)
        self.entry_recurring_amount = tk.Entry(self.recurring_window)
        self.entry_recurring_amount.pack(pady=5)

        self.label_limit = tk.Label(self.recurring_window, text="Set Limit:", bg='#5E9387', fg='#CEE9B6')
        self.label_limit.pack(pady=5)
        self.entry_limit = tk.Entry(self.recurring_window)
        self.entry_limit.pack(pady=5)

        self.button_add_recurring = tk.Button(self.recurring_window, text="Add Recurring Expense", command=self.add_recurring_expense)
        self.button_add_recurring.pack(pady=5)

        self.button_done_recurring = tk.Button(self.recurring_window, text="Done", command=self.exit_recurring_expenses)
        self.button_done_recurring.pack(pady=5)

    def exit_recurring_expenses(self):
        self.recurring_window.destroy()
        self.root.deiconify()

    def add_recurring_expense(self):
        try:
            expense_name = self.entry_recurring_expense.get()
            expense_amount = float(self.entry_recurring_amount.get())
            limit = float(self.entry_limit.get())
            self.recurring_expenses.append((expense_name, expense_amount, limit))
            messagebox.showinfo("Recurring Expense Added", f"Added recurring expense: {expense_name} - Amount: ₱{expense_amount:.2f}, Limit: ${limit:.2f}")
            self.entry_recurring_expense.delete(0, tk.END)
            self.entry_recurring_amount.delete(0, tk.END)
            self.entry_limit.delete(0, tk.END)


            # Close the recurring expenses window, login window and return to expenses window
            self.exit_recurring_expenses.login_window()

        except ValueError:
            messagebox.showerror("Error", "Invalid input for recurring expense.")
        
    def exit_recurring_expenses(self):
        self.recurring_window.destroy()
        self.expenses_window.deiconify()  # Show the expenses window again 

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()