
import tkinter as tk
import random
import colors as c
import time

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))
        self.make_GUI()
        self.start_game()
        while True:
            cont = 0
            for i in range(4):
                for j in range(4):
                    if self.matrix[i][j] == 0:
                        cont = cont+1
            if cont <= 1 and self.score >=20000:
                jugada = self.mirar(4,1)
            elif cont <= 2 and self.score >=2000:
                jugada = self.mirar(3,1)
            elif cont >= 4 and cont <= 8 and self.score>=1000:
                jugada = self.mirar(2,1)
            else:
                jugada = self.mirar(1,1)
            anterior=0
            if jugada == 1 and jugada != anterior:
                anterior = jugada
                self.left()
                self.add_new_tile()
            elif jugada == 2 and jugada != anterior:
                anterior = jugada
                self.right()
                self.add_new_tile()
            elif jugada == 3 and jugada != anterior:
                anterior = jugada
                self.up()
                self.add_new_tile()
            elif jugada == 4 and jugada != anterior:
                anterior = jugada
                self.down()
                self.add_new_tile()
            else:
                jugada += 1
            self.update_GUI()
            if self.game_over():
                self.update()
                break
            self.update()
            #time.sleep(0.5)
        time.sleep(5000)
    def make_GUI(self):
        # make grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=100,
                    height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        # make score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT).grid(
            row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)
    def start_game(self):
        # create matrix of zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")

        self.score = 0
    # Matrix Manipulation Functions
    def imprimir(self):
        j=0
        matrix1 = self.matrix
        for i in range(4):
            print("[" + str(matrix1[i][j])+" "+ str(matrix1[i][j+1])+" "+ str(matrix1[i][j+2])+" "+ str(matrix1[i][j+3])+"] " )
        print(self.score)
    def heuristica(self, matrix):
        heuris =self.score*3
        vaciosv=0
        vaciosn=1
        max=0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] > max:
                    max = self.matrix[i][j]
                if matrix[i][j]==0:
                    vaciosv=vaciosv+1
                if self.matrix[i][j]==0:
                    vaciosn=vaciosn+1
                if i > 0:#arriba
                    if self.matrix[i][j] == self.matrix[i-1][j]:
                        heuris = heuris+(self.matrix[i][j] * 1)
                    elif self.matrix[i][j] == ((self.matrix[i-1][j])/2):
                        heuris = heuris + (self.matrix[i][j] * 1)
                if i < 3:#abajo
                    if self.matrix[i][j] == self.matrix[i + 1][j]:
                        heuris = heuris + (self.matrix[i][j] * 1)
                    elif self.matrix[i][j] == ((self.matrix[i + 1][j]) / 2):
                        heuris = heuris + (self.matrix[i][j] * 1)
                if j > 0:  # derecha
                    if self.matrix[i][j] == self.matrix[i][j-1]:
                        heuris = heuris + (self.matrix[i][j] * 1)
                    elif self.matrix[i][j] == ((self.matrix[i][j-1]) / 2):
                        heuris = heuris + (self.matrix[i][j] * 1)
                if j < 3:  # izquierda
                    if self.matrix[i][j] == self.matrix[i][j + 1]:
                        heuris = heuris + (self.matrix[i][j] * 1)
                    elif self.matrix[i][j] == ((self.matrix[i][j + 1]) / 2):
                        heuris = heuris + (self.matrix[i][j] * 1)
        if max == self.matrix[0][0]:
            heuris = heuris + self.matrix[0][0] * 5
            heuris = heuris + self.matrix[0][1] * 1.5
            heuris = heuris + self.matrix[0][2] * 1.2
            heuris = heuris + self.matrix[0][3] * 0.9
            heuris = heuris + self.matrix[1][0] * 1.5
            heuris = heuris + self.matrix[2][0] * 1.2
            heuris = heuris + self.matrix[3][0] * 0.9
            heuris = heuris + self.matrix[1][1] * 1
            heuris = heuris + self.matrix[1][2] * 0.4
            heuris = heuris + self.matrix[2][1] * 0.4
        elif max == self.matrix[0][3]:
            heuris = heuris + self.matrix[0][3] * 5
            heuris = heuris + self.matrix[0][2] * 1.5
            heuris = heuris + self.matrix[0][1] * 1.2
            heuris = heuris + self.matrix[0][0] * 0.9
            heuris = heuris + self.matrix[1][3] * 1.5
            heuris = heuris + self.matrix[2][3] * 1.2
            heuris = heuris + self.matrix[3][3] * 0.9
            heuris = heuris + self.matrix[1][2] * 1
            heuris = heuris + self.matrix[1][1] * 0.4
            heuris = heuris + self.matrix[2][2] * 0.4
        elif max == self.matrix[3][0]:
            heuris = heuris + self.matrix[3][0] * 5
            heuris = heuris + self.matrix[2][0] * 1.5
            heuris = heuris + self.matrix[1][0] * 1.2
            heuris = heuris + self.matrix[0][0] * 0.9
            heuris = heuris + self.matrix[3][1] * 1.5
            heuris = heuris + self.matrix[3][2] * 1.2
            heuris = heuris + self.matrix[3][3] * 0.9
            heuris = heuris + self.matrix[2][1] * 1
            heuris = heuris + self.matrix[1][1] * 0.4
            heuris = heuris + self.matrix[2][2] * 0.4
        elif max == self.matrix[3][3]:
            heuris = heuris + self.matrix[3][3] * 5
            heuris = heuris + self.matrix[2][3] * 1.5
            heuris = heuris + self.matrix[1][3] * 1.2
            heuris = heuris + self.matrix[0][3] * 0.9
            heuris = heuris + self.matrix[3][2] * 1.5
            heuris = heuris + self.matrix[3][1] * 1.2
            heuris = heuris + self.matrix[3][0] * 0.9
            heuris = heuris + self.matrix[2][2] * 1
            heuris = heuris + self.matrix[1][2] * 0.4
            heuris = heuris + self.matrix[2][1] * 0.4
        heuris = heuris + self.score*0.009*vaciosn
        return heuris
  
    def mirar(self,profundidad,og):
        matrix1 = self.matrix
        original = self.score
        self.left()
        aux1 = -1
        aux11 = -1
        cant0 = 0

        if matrix1 == self.matrix:
            aux1 = 0
        else:

            if matrix1 == self.matrix:
                aux1 = 0
            else:
                for (i) in range(4):
                    for j in range(4):
                        if self.matrix[i][j] == 0:
                            cant0 = cant0 + 1
                            # evaluamos con el 2
                            self.matrix[i][j] = 2
                            if profundidad == 1:
                                aux11 = self.evaluar() * 0.9
                            else:
                                aux11 = self.mirar(profundidad - 1,0) * 0.9

                            self.matrix[i][j] = 0

                            aux1 = aux1 + aux11

                aux1 = aux1 / cant0


        self.matrix = matrix1
        self.score = original

        matrix1 = self.matrix
        self.right()
        aux2 = 0
        aux22 = 0
        cant0 = 0
        if matrix1 == self.matrix:
            aux2 = 0
        else:

            if matrix1 == self.matrix:
                aux2 = 0
            else:
                for (i) in range(4):
                    for j in range(4):
                        if self.matrix[i][j] == 0:
                            cant0 = cant0 + 1
                            # evaluamos con el 2
                            self.matrix[i][j] = 2
                            if profundidad == 1:
                                aux22 = self.evaluar() * 0.9
                            else:
                                aux22 = self.mirar(profundidad - 1,0) * 0.9

                            self.matrix[i][j] = 0

                            aux2 = aux2 + aux22

                aux2 = aux2 / cant0



        self.matrix = matrix1
        self.score = original

        matrix1 = self.matrix
        self.up()
        aux3 = 0
        aux31 = 0
        cant0 = 0
        if matrix1 == self.matrix:
            aux3 = 0
        else:

            if matrix1 == self.matrix:
                aux3 = 0
            else:
                for (i) in range(4):
                    for j in range(4):
                        if self.matrix[i][j] == 0:
                            cant0 = cant0 + 1
                            # evaluamos con el 2
                            self.matrix[i][j] = 2
                            if profundidad == 1:
                                aux31 = self.evaluar() * 0.9
                            else:
                                aux31 = self.mirar(profundidad - 1,0) * 0.9


                            self.matrix[i][j] = 0

                            aux3 = aux3 + aux31

                aux3 = aux3 / cant0



        self.matrix = matrix1
        self.score = original

        matrix1 = self.matrix
        self.down()
        aux4 = 0
        aux41 = 0
        cant0 = 0
        if matrix1 == self.matrix:
            aux4 = 0
        else:

            if matrix1 == self.matrix:
                aux4 = 0
            else:
                for (i) in range(4):
                    for j in range(4):
                        if self.matrix[i][j] == 0:
                            cant0 = cant0 + 1
                            # evaluamos con el 2
                            self.matrix[i][j] = 2
                            if profundidad == 1:
                                aux41 = self.evaluar() * 0.9
                            else:
                                aux41 = self.mirar(profundidad - 1,0) * 0.9

                            self.matrix[i][j] = 0

                            aux4 = aux4 + aux41

                aux4 = aux4 / cant0

        self.matrix = matrix1
        self.score = original

        mejorvalor = max(aux2, aux3, aux1, aux4)

        if aux2 == mejorvalor:
            if og == 1:
                return 2
            else:
                return aux2

        if aux4 == mejorvalor:
            if og == 1:
                return 4
            else:
                return aux4

        if aux1 == mejorvalor:
            if og == 1:
                return 1
            else:
                return aux1

        if aux3 == mejorvalor:
            if og == 1:
                return 3
            else:
                return aux3
        else:
            ran = random.choice([1, 2, 3, 4])
            return ran
    def evaluar(self):
        matrix1 = self.matrix
        original = self.score
        self.left()
        aux1 = -1
        aux11 = -1
        cant0 = 0

        if matrix1 == self.matrix:
            aux1 = 0
        else:
            aux1 = self.heuristica(matrix1)

        self.matrix = matrix1
        self.score = original

        matrix1 = self.matrix
        self.right()
        aux2 = 0
        aux21 = 0
        cant0 = 0
        if matrix1 == self.matrix:
            aux2 = 0
        else:
            aux2 = self.heuristica(matrix1)
        self.matrix = matrix1
        self.score = original

        matrix1 = self.matrix
        self.up()
        aux3 = 0
        aux31 = 0
        cant0 = 0
        if matrix1 == self.matrix:
            aux3 = 0
        else:
            aux3 = self.heuristica(matrix1)
        self.matrix = matrix1
        self.score = original

        matrix1 = self.matrix
        self.down()
        aux4 = 0
        aux41 = 0
        cant0 = 0
        if matrix1 == self.matrix:
            aux4 = 0
        else:
            aux4 = self.heuristica(matrix1)

        self.matrix = matrix1
        self.score = original

        mejorvalor = max(aux2, aux3, aux1, aux4)

        if aux2 == mejorvalor:
            return aux2

        if aux4 == mejorvalor:
            return aux4

        if aux1 == mejorvalor:
            return aux1

        if aux3 == mejorvalor:

            return aux3
        else:
            ran = random.choice([1, 2, 3, 4])
            return ran
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
                    if (self.matrix == new_matrix):
                        return False
        self.matrix = new_matrix
        return True
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix
    # Add a new 2 or 4 tile randomly to an empty cell
    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while(self.matrix[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)

            self.matrix[row][col] = random.choice([2,2,2,2,2,2,2,2,2, 4])
    # Update the GUI to match the matrix
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()
    # Arrow-Press Functions
    def left(self):
        if self.stack():
            self.combine()
            self.stack()


        elif self.horizontal_move_exists():
            self.combine()
            self.stack()
    def right(self):
        self.reverse()
        if self.stack():
            self.combine()
            self.stack()


        elif self.horizontal_move_exists():
            self.combine()
            self.stack()


        self.reverse()
    def up(self):
        self.transpose()
        if self.stack():
            self.combine()
            self.stack()


        elif self.horizontal_move_exists():
            self.combine()
            self.stack()


        self.transpose()
    def down(self):
        self.transpose()
        self.reverse()
        if self.stack():
            self.combine()
            self.stack()


        elif  self.horizontal_move_exists():
            self.combine()
            self.stack()


        self.reverse()
        self.transpose()
    # Check if any moves are possible
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1] and self.matrix[i][j] !=0:
                    return True
        return False
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False
    # Check if Game is Over (Win/Lose)
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()
        if not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game over!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()
            return True
        return False
def main():
    Game()
if __name__ == "__main__":
    main()