#include <iostream>
#include <vector>
#include <queue>
#include <functional>

#define UNASSIGNED 0
#define N 9

using namespace std;

struct Cell {
    int possibilities;
    int row;
    int col;
    Cell(int p, int r, int c) : possibilities(p), row(r), col(c) {}
};

struct compare {
    bool operator()(const Cell& a, const Cell& b) {
        return a.possibilities > b.possibilities;
    }
};

void printGrid(const vector<vector<int>>& grid) {
    for (int row = 0; row < N; row++) {
        for (int col = 0; col < N; col++)
            cout << grid[row][col] << " ";
        cout << endl;
    }
}

bool isSafe(const vector<vector<int>>& grid, int row, int col, int num) {
    for (int d = 0; d < N; d++) {
        if (grid[row][d] == num || grid[d][col] == num) {
            return false;
        }
    }
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (grid[i + startRow][j + startCol] == num) {
                return false;
            }
    return true;
}

bool findUnassignedLocation(const vector<vector<int>>& grid, int& row, int& col) {
    priority_queue<Cell, vector<Cell>, compare> minHeap;

    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            if (grid[r][c] == UNASSIGNED) {
                int count = 0;
                for (int num = 1; num <= N; num++) {
                    if (isSafe(grid, r, c, num)) {
                        count++;
                    }
                }
                minHeap.push(Cell(count, r, c));
            }
        }
    }

    if (!minHeap.empty()) {
        Cell cell = minHeap.top();
        row = cell.row;
        col = cell.col;
        return true;
    }

    return false;
}

bool solveSudoku(vector<vector<int>>& grid) {
    int row, col;
    if (!findUnassignedLocation(grid, row, col))
        return true; // Puzzle solved

    for (int num = 1; num <= N; num++) {
        if (isSafe(grid, row, col, num)) {
            grid[row][col] = num;
            if (solveSudoku(grid))
                return true;
            grid[row][col] = UNASSIGNED;
        }
    }
    return false;
}

int main() {
    vector<vector<int>> grid = {
        {0, 8, 0, 6, 0, 0, 0, 0, 0},
        {4, 0, 0, 0, 0, 0, 9, 0, 0},
        {0, 9, 0, 5, 0, 1, 0, 8, 0},
        {0, 0, 2, 0, 0, 0, 0, 0, 7},
        {0, 4, 0, 9, 0, 8, 0, 5, 0},
        {0, 0, 0, 0, 3, 0, 0, 0, 0},
        {0, 0, 0, 0, 4, 0, 0, 3, 0},
        {7, 0, 0, 1, 0, 3, 0, 0, 5},
        {0, 1, 0, 0, 6, 0, 0, 0, 0}
    };
    if (solveSudoku(grid))
        printGrid(grid);
    else
        cout << "Pas de solution existe";
    return 0;
}

