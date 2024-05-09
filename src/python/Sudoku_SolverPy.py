import tkinter as tk
from tkinter import messagebox
import time
import numpy as np

N = 9
class SudokuGUI:
    def __init__(self, master, sudoku=None, timelaps = 0):
        self.master = master
        master.title("Sudoku Solver")
        self.last_update_time = 0 
        
        if sudoku is None:
            sudoku = [[0]*9 for _ in range(9)]  # Default to an empty grid if none provided
        
        self.sudoku = sudoku
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.locked = [[False for _ in range(9)] for _ in range(9)]

        self.create_grid()
        self.lock_button = tk.Button(master, text="Lock Initial Numbers", command=self.lock_entries)
        self.lock_button.pack()
        self.solve_button = tk.Button(master, text="Solve Sudoku", command=self.solve, state='disabled')
        self.solve_button.pack()
        self.backtracking_visu = False
        self.timelaps = timelaps


    def update_gui(self, row, column, number):
        if not self.locked[row][column]:
            self.entries[row][column].delete(0, tk.END)
            self.entries[row][column].insert(0, number)
            self.entries[row][column].config(fg='purple')  
            self.master.update()
            


    def create_grid(self):
        self.canvas = tk.Canvas(self.master, width=300, height=300)
        self.canvas.pack()

        entry_width = 33
        entry_height = 33
        for i in range(9):
            for j in range(9):
                x = j * entry_width
                y = i * entry_height
                entry = tk.Entry(self.master, width=2, font=('Arial', 14), borderwidth=0, highlightthickness=0)
                entry.place(x=x+2, y=y+2, width=entry_width-2, height=entry_height-2)
                if self.sudoku[i][j] != 0:
                    entry.insert(0, self.sudoku[i][j])
                    entry.config(fg='blue')  
                else:
                    entry.insert(0, '0')
                    entry.config(fg='red')  
                self.entries[i][j] = entry

        for n in range(1, 3):
            self.canvas.create_line(n * 3 * entry_width, 0, n * 3 * entry_width, 300, width=2, fill='black')
            self.canvas.create_line(0, n * 3 * entry_height, 300, n * 3 * entry_height, width=2, fill='black')

    def lock_entries(self):
        for i in range(9):
            for j in range(9):
                entry_value = self.entries[i][j].get()
                if entry_value.isdigit() and int(entry_value) in range(1, 10):
                    self.entries[i][j].config(fg='blue', state='readonly')
                    self.locked[i][j] = True
                else:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].config(fg='red')
        self.lock_button.config(state='disabled')
        self.solve_button.config(state='normal')


    def is_safe(self, row, col, num):
        if num in self.sudoku[row, :]:
            return False
        if num in self.sudoku[:, col]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.sudoku[start_row:start_row+3, start_col:start_col+3]:
            return False
        return True


    def solve(self):
        grid = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry_value = self.entries[i][j].get()
                grid[i][j] = int(entry_value) if entry_value.isdigit() else 0

        self.sudoku = np.array(grid)
        success = self.solve_sudoku(0, 0)
        if success:
            self.update_entries()
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists for the given Sudoku.")
        self.master.update()

    def update_entries(self):
        # Update GUI entries from the sudoku matrix
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(self.sudoku[i][j]) if self.sudoku[i][j] != 0 else '')
                self.entries[i][j].config(fg='black')

    def solve_sudoku(self, row, col):
        if col == N:
            col = 0
            row += 1
        if row == N:
            return True

        if self.sudoku[row][col] == 0:
            for num in range(1, 10):
                if self.is_safe(row, col, num):
                    self.sudoku[row][col] = num
                    self.update_entry(row, col, num)
                    time.sleep(self.timelaps) # Introduce a slight delay to visualize the algorithm
                    if self.solve_sudoku(row + 1 if col == 8 else row, (col + 1) % 9):
                        return True
                    self.sudoku[row][col] = 0
                    self.update_entry(row, col, '')  # Remove the number on backtrack
        else:
            return self.solve_sudoku(row + 1 if col == 8 else row, (col + 1) % 9)

        return False

    def update_entry(self, row, col, value):
        self.entries[row][col].delete(0, tk.END)
        if value:
            self.entries[row][col].insert(0, str(value))
        self.master.update_idletasks()



def main():
    sudoku = [
    [0, 0, 1, 0, 5, 4, 0, 0, 0],
    [3, 4, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 1, 9, 0, 7, 0],
    [4, 0, 7, 9, 3, 1, 0, 6, 0],
    [9, 1, 0, 0, 7, 0, 3, 4, 2],
    [0, 0, 0, 2, 0, 5, 0, 0, 7],
    [1, 3, 2, 0, 9, 7, 0, 0, 5],
    [0, 6, 4, 5, 0, 0, 0, 1, 0],
    [0, 0, 8, 1, 0, 6, 0, 0, 4]
]


    root = tk.Tk()
    app = SudokuGUI(root, sudoku = None, timelaps= 0)
    root.mainloop()

if __name__ == "__main__":
    main()




