import tkinter
import math


class Conway():
    def __init__(self):
        self.UNIVERSE_SQUARE_SIZE = 800
        self.CELL_SIDE_LENGTH = 10
        self.SLOW_SPEED = 500
        self.NORMAL_SPEED = 75
        self.FAST_SPEED = 1
        self.DEAD_COLOR = "white"
        self.ALIVE_COLOR = "black"

        self.cell_list_size = int(self.UNIVERSE_SQUARE_SIZE / self.CELL_SIDE_LENGTH)
        self.cells = [[0 for i in range(self.cell_list_size)] for j in range(self.cell_list_size)]
        self.animate = False
        self.outline = "black"
        self.update_speed = self.NORMAL_SPEED

        self.root = tkinter.Tk()
        self.root.title('conway')
        self.iterations = tkinter.IntVar()
        self.iterations.set(0)
        self.controls = tkinter.Frame(self.root)
        self.display = tkinter.Frame(self.root)

        self.canvas_widget = tkinter.Canvas(self.display, bg="white", height=self.UNIVERSE_SQUARE_SIZE, width=self.UNIVERSE_SQUARE_SIZE)
        self.canvas_widget.bind("<Button-1>", self.handle_canvas_click)
        self.canvas_items = []
        for i, cells_value in enumerate(self.cells):
            self.canvas_items.append([])
            for j, _ in enumerate(cells_value):
                self.canvas_items[i].append(self.canvas_widget.create_rectangle(
                    i * self.CELL_SIDE_LENGTH,
                    j * self.CELL_SIDE_LENGTH,
                    i * self.CELL_SIDE_LENGTH + self.CELL_SIDE_LENGTH,
                    j * self.CELL_SIDE_LENGTH + self.CELL_SIDE_LENGTH,
                    fill=self.DEAD_COLOR,
                    outline=self.outline))

        self.title_label = tkinter.Label(self.controls, text="Conway's Game of Life", font="bold")
        self.info_label = tkinter.Label(self.controls, text="Click cells to turn on/off")
        self.output_str_label = tkinter.Label(self.controls, text="Iterations:")
        self.output_int_label = tkinter.Label(self.controls, textvariable=self.iterations)
        self.start_stop_button = tkinter.Button(self.controls, text="START / STOP", command=self.start_stop)
        self.update_button = tkinter.Button(self.controls, text="UPDATE", command=self.update)
        self.reset_button = tkinter.Button(self.controls, text="RESET", command=self.reset)
        self.slow_speed_button = tkinter.Button(self.controls, text="SLOW", command=lambda: self.set_speed(self.SLOW_SPEED))
        self.normal_speed_button = tkinter.Button(self.controls, text="NORMAL", command=lambda: self.set_speed(self.NORMAL_SPEED))
        self.fast_speed_button = tkinter.Button(self.controls, text="FAST", command=lambda: self.set_speed(self.FAST_SPEED))

        self.display.grid(row=0, column=0, sticky="nw")
        self.controls.grid(row=0, column=1, sticky="nw")

        self.canvas_widget.grid(row=0, column=0, sticky="nw")
        self.title_label.grid(row=0, column=0, sticky="nw", padx=10, pady=(0, 10))
        self.info_label.grid(row=1, column=0, sticky="nw", padx=10, pady=(0, 10))
        self.output_str_label.grid(row=2, column=0, sticky="nw", padx=(10, 0), pady=(0, 10))
        self.output_int_label.grid(row=2, column=1, sticky="new", padx=(1, 1), pady=(0, 10))
        self.start_stop_button.grid(row=3, column=0, sticky="new", padx=10, pady=(0, 10))
        self.update_button.grid(row=4, column=0, sticky="new", padx=10, pady=(0, 10))
        self.reset_button.grid(row=5, column=0, sticky="new", padx=10, pady=(0, 10))
        self.slow_speed_button.grid(row=3, column=1, sticky="new", padx=10, pady=(0, 10))
        self.normal_speed_button.grid(row=4, column=1, sticky="new", padx=10, pady=(0, 10))
        self.fast_speed_button.grid(row=5, column=1, sticky="new", padx=10, pady=(0, 10))

        self.root.mainloop()

    def handle_canvas_click(self, event):
        click_column = math.floor(event.x / self.CELL_SIDE_LENGTH)
        click_row = math.floor(event.y / self.CELL_SIDE_LENGTH)
        self.cells[click_column][click_row] = not self.cells[click_column][click_row]
        self.draw()

    def start_stop(self):
        self.animate = not self.animate
        if self.animate:
            self.update_button["state"] = "disabled"
            self.outline = ""
            self.update_after = self.root.after(self.update_speed, self.update)
        else:
            self.root.after_cancel(self.update_after)
            self.update_button["state"] = "normal"
            self.outline = "black"
            self.draw()

    def update(self):
        updated_cells = []
        for i, cells_value in enumerate(self.cells):
            updated_cells.append([])
            for j, cell_value in enumerate(cells_value):
                living_neighbors = 0
                if i == 0:
                    if j > 0:
                        living_neighbors = living_neighbors + self.cells[i][j-1]
                    if j < self.cell_list_size - 1:
                        living_neighbors = living_neighbors + self.cells[i][j+1]
                if i > 0:
                    living_neighbors = living_neighbors + self.cells[i-1][j]
                    if j > 0:
                        living_neighbors = living_neighbors + self.cells[i][j-1]
                        living_neighbors = living_neighbors + self.cells[i-1][j-1]
                    if j < self.cell_list_size - 1:
                        living_neighbors = living_neighbors + self.cells[i][j+1]
                        living_neighbors = living_neighbors + self.cells[i-1][j+1]
                if i < self.cell_list_size - 1:
                    living_neighbors = living_neighbors + self.cells[i+1][j]
                    if j > 0:
                        living_neighbors = living_neighbors + self.cells[i+1][j-1]
                    if j < self.cell_list_size - 1:
                        living_neighbors = living_neighbors + self.cells[i+1][j+1]
                if cell_value == 1:
                    if living_neighbors > 1 and living_neighbors < 4:
                        updated_cells[i].append(1)
                    else:
                        updated_cells[i].append(0)
                else:
                    if living_neighbors == 3:
                        updated_cells[i].append(1)
                    else:
                        updated_cells[i].append(0)
        self.cells = updated_cells
        self.iterations.set(self.iterations.get() + 1)
        self.draw()
        if self.animate:
            self.update_after = self.root.after(self.update_speed, self.update)

    def reset(self):
        if self.animate:
            self.start_stop()
        updated_cells = []
        for i, cells_value in enumerate(self.cells):
            updated_cells.append([])
            for _ in cells_value:
                updated_cells[i].append(0)
        self.cells = updated_cells
        self.iterations.set(0)
        self.draw()

    def set_speed(self, speed):
        self.update_speed = speed

    def draw(self):
        for i, cells_value in enumerate(self.cells):
            for j, cell_value in enumerate(cells_value):
                if cell_value == 1:
                    fill_color = self.ALIVE_COLOR
                else:
                    fill_color = self.DEAD_COLOR
                self.canvas_widget.itemconfig(self.canvas_items[i][j], fill=fill_color, outline=self.outline)


if __name__ == "__main__":
    Conway()
