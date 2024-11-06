import tkinter as tk
from tkinter import ttk
import math
import re

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("I MADE THIS F*CK YEAH")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        self.calculation = ""
        self.history = []
        self.memory = 0

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 12))

        self.result = tk.Text(self.master, height=2, width=25, font=("Arial", 20), bg="light green")
        self.result.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        self.history_listbox = tk.Listbox(self.master, height=3, font=("Arial", 12))
        self.history_listbox.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        buttons = [
            'sin', 'cos', 'tan', 'log', '(',
            'π', 'e', '^', '√', ')',
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', '←',
            '1', '2', '3', '-', 'M+',
            '0', '.', '%', '+', 'M-',
            'MR', 'MC', 'Ans', '=', 'MS'
        ]

        row = 2
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ttk.Button(self.master, text=button, command=cmd).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            col += 1
            if col > 4:
                col = 0
                row += 1

        for i in range(8):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)

    def bind_keys(self):
        self.master.bind('<Return>', lambda event: self.click('='))
        self.master.bind('<BackSpace>', lambda event: self.click('←'))
        for key in '0123456789./*-+()':
            self.master.bind(key, lambda event, key=key: self.click(key))

    def click(self, key):
        if key == '=':
            self.evaluate()
        elif key == 'C':
            self.clear()
        elif key == '←':
            self.backspace()
        elif key in ['sin', 'cos', 'tan', 'log', '√']:
            self.add_to_calculation(f"{key}(")
        elif key == 'π':
            self.add_to_calculation('math.pi')
        elif key == 'e':
            self.add_to_calculation('math.e')
        elif key == '^':
            self.add_to_calculation('**')
        elif key == 'M+':
            self.memory_add()
        elif key == 'M-':
            self.memory_subtract()
        elif key == 'MR':
            self.memory_recall()
        elif key == 'MC':
            self.memory_clear()
        elif key == 'MS':
            self.memory_store()
        elif key == 'Ans':
            self.use_last_answer()
        else:
            self.add_to_calculation(key)

    def add_to_calculation(self, symbol):
        self.calculation += str(symbol)
        self.update_display()

    def clear(self):
        self.calculation = ""
        self.update_display()

    def backspace(self):
        self.calculation = self.calculation[:-1]
        self.update_display()

    def update_display(self):
        self.result.delete(1.0, "end")
        self.result.insert(1.0, self.calculation)

    def evaluate(self):
        try:
            # Replace √ with math.sqrt
            expression = re.sub(r'√\(([^)]+)\)', r'math.sqrt(\1)', self.calculation)
            # Replace other function names
            expression = expression.replace('sin', 'math.sin')
            expression = expression.replace('cos', 'math.cos')
            expression = expression.replace('tan', 'math.tan')
            expression = expression.replace('log', 'math.log10')
            
            result = eval(expression)
            self.calculation = str(result)
            self.update_display()
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            self.result.delete(1.0, "end")
            self.result.insert(1.0, f"Error: {str(e)}")
            self.calculation = ""

    def add_to_history(self, result):
        self.history.append(result)
        if len(self.history) > 3:
            self.history.pop(0)
        self.update_history_display()

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for item in reversed(self.history):
            self.history_listbox.insert(0, item)

    def memory_add(self):
        try:
            self.memory += float(self.calculation)
            self.clear()
        except ValueError:
            self.result.delete(1.0, "end")
            self.result.insert(1.0, "Error: Invalid input for M+")

    def memory_subtract(self):
        try:
            self.memory -= float(self.calculation)
            self.clear()
        except ValueError:
            self.result.delete(1.0, "end")
            self.result.insert(1.0, "Error: Invalid input for M-")

    def memory_recall(self):
        self.calculation = str(self.memory)
        self.update_display()

    def memory_clear(self):
        self.memory = 0

    def memory_store(self):
        try:
            self.memory = float(self.calculation)
            self.clear()
        except ValueError:
            self.result.delete(1.0, "end")
            self.result.insert(1.0, "Error: Invalid input for MS")

    def use_last_answer(self):
        if self.history:
            last_result = self.history[-1].split('=')[-1].strip()
            self.add_to_calculation(last_result)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()