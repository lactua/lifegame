from random import random
from time import sleep
from os import get_terminal_size, system, name as osname
from argparse import ArgumentParser

def clear():
    if osname.lower() == 'nt': system('cls')
    else: system('clear')

class Cell:
    def __init__(self, x: int, y: int, state: int=0) -> None:
        self.x, self.y = x, y
        self.state = state

class Table:
    def __init__(self, width: int=None, height: int=None, table: list[list[int]]=None) -> None:
        if table:
            self.table = [[Cell(x, y, state) for x, state in enumerate(row)] for y, row in enumerate(table)]
            self.width, self.height = len(table[0]), len(table)
        else:
            self.width, self.height = width, height
            self.table = [[Cell(x, y) for x in range(width)] for y in range(height)]
    
    def getCell(self, x: int, y: int) -> Cell:
        if y >= self.height or y < 0 or x >= self.width or x < 0: return Cell(x, y)
        return self.table[y][x]
    
    def getCells(self) -> list[Cell]:
        cells = []

        for row in self.table: cells.extend(row)

        return cells
 
    def randomize(self, prob: int):
        for cell in self.getCells():
            if random() <= prob: cell.state = 1

class Game:
    def __init__(self, table: Table) -> None:
        self.table = table

    def play(self):
        new_table = Table(width=self.table.width, height=self.table.height)

        for cell in self.table.getCells():

            near_cells = []
            for y in range(cell.y - 1, cell.y + 2):
                for x in range(cell.x - 1, cell.x + 2):
                    near_cells.append(self.table.getCell(x, y))
                
            near_cells.pop(4)

            new_cell = new_table.getCell(cell.x, cell.y)

            if cell.state == 0:
                if len(list(filter(lambda cell: cell.state == 1, near_cells))) == 3:
                    new_cell.state = 1
                else:
                    new_cell.state = 0
            
            if cell.state == 1:
                if len(list(filter(lambda cell: cell.state == 1, near_cells))) not in [2, 3]:
                    new_cell.state = 0
                else:
                    new_cell.state = 1

        self.table = new_table

def displayTable(table: Table):
    string = str.join('\n', [str.join('', ['%' if cell.state else ' ' for cell in row]) for row in table.table])
    print(string)

def parseArgs(*args: tuple[tuple, dict]):
    argument_parser = ArgumentParser()
    for arg in args: argument_parser.add_argument(*arg[0], **arg[1])
    return argument_parser.parse_args().__dict__

def importSystem(table:Table, system:str):
    system_table = Table(table=[[0 if cell == " " else 1 for cell in row] for row in system.split('\n')])

    table_middle = table.width // 2, table.height // 2
    system_table_middle = system_table.width // 2, system_table.height // 2

    for cell in system_table.getCells():
        table_cell = table.getCell(table_middle[0]-system_table_middle[0]+cell.x, table_middle[1]-system_table_middle[1]+cell.y)
        table_cell.state = cell.state

def main(delay: int, alive_cell_percentage: int, width: int, height: int, system_path: int):
    prob = alive_cell_percentage / 100

    table = Table(width, height)

    if system_path:
        with open(system_path, 'r') as file:
            importSystem(table, file.read())
    else:
        table.randomize(prob)

    game = Game(table)

    clear()

    while True:
        print('\033[H')
        displayTable(game.table)
        game.play()
        sleep(delay)

if __name__ == '__main__':

    args = parseArgs(
        (
            ('-d', '--delay'),
            {'default': 0, 'type': float, 'help': 'Delay between two frames'}
        ),
        (
            ('-a', '--alive-cell-percentage'),
            {'default': 10, 'type': float, 'help': 'Percentage of alive cell'}
        ),
        (
            ('-W', '--width'),
            {'default': get_terminal_size().columns-1, 'type': int, 'help': 'Width of the playground'}
        ),
        (
            ('-H', '--height'),
            {'default': get_terminal_size().lines-2, 'type': int, 'help': 'Height of the playground'}
        ),
        (
            ('-s', '--system-path'),
            {'required': False, 'type': str, 'help': 'Path to the cell system file to start with. Cancel the alive-cell-percentage arg'}
        )
    )

    main(**args)