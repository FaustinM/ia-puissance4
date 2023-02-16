from random import randint


def segmentEquation(coords1, coords2):
    xIncrease = coords2[0] - coords1[0]
    yIncrease = coords2[1] - coords1[1]
    if xIncrease == 0:
        return (1, 0, -coords1[0])
    if yIncrease == 0:
        return (0, 1, -coords1[1])

    increaseRate = yIncrease / xIncrease
    originValue = coords1[1] - coords1[0] * increaseRate

    return (-increaseRate, 1, -originValue)


class JeuPuissance4:

    """
    our main game class to implement the whole game in python, with all necessary functions :

    __init__ : intializes our game object with the game variables
    play : function placing a pawn for the current player in the indicated column unless the column is full
    win : function detecting whether one of the players won, called by play function each turn to end the game
    """

    def __init__(self):
        """
        definition of our class variables

        grid : list of list - our grid where 0 will mean no pawn on the tile,1 red pawn and 2 yellow pawn
        currentPlayer : int - always one (human plays first)
        turn : int - number of turns from the beginning of the game
        """

        self.grid = [[0 for i in range(6)] for i in range(7)]
        # self.currentPlayer = randint(1,2)        # Function to randomly choose the first player - not used yet
        self.currentPlayer = 1
        self.turns = 0

    def __str__(self):
        """
        overwriting built-in function __str__ for better display when called using print(gameInstance)
        """
        lineDisplay = [
            [column[lineNumber] for column in self.grid] for lineNumber in range(6)
        ]
        lineDisplay = "\n".join([str(line) for line in lineDisplay])
        return lineDisplay

    def possiblePlays(self, grid=None):
        if grid == None:
            return [i[0] for i in enumerate(self.grid) if 0 in i[1]]
        else:
            return [i[0] for i in enumerate(grid) if 0 in i[1]]

    def getNearby(self, coords):
        nearbyList = {}
        for x in [
            coords[0] + increment
            for increment in (-1, 0, 1)
            if coords[0] + increment >= 0 and coords[0] + increment < 7
        ]:
            for y in [
                coords[1] + increment
                for increment in (-1, 0, 1)
                if coords[1] + increment >= 0 and coords[1] + increment < 6
            ]:
                if not (x == coords[0] and y == coords[1]):
                    nearbyList[(x, y)] = self.grid[x][y]
        return nearbyList

    def win(self, coords, player):
        """
        a function called each time a player places a pawn, detects whether one of both players has aligned 4 pawns or whether all columns are full - no winner

        return : 1/2 for the winning player, 0 if there is no winner and 3 if all columns are full - game over with no winner
        """
        cols = len(self.grid)
        rows = len(self.grid[0])
        row = coords[1]
        col = coords[0]

        for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            consecutive_items = 1
            for delta in (1, -1):
                delta_row *= delta
                delta_col *= delta
                next_row = row + delta_row
                next_col = col + delta_col
                while 0 <= next_row < rows and 0 <= next_col < cols:
                    if self.grid[next_col][next_row] == player:
                        consecutive_items += 1
                    else:
                        break
                    if consecutive_items == 4:
                        return player
                    next_row += delta_row
                    next_col += delta_col
        if self.turns == 42:
            return 3

        #         nearby = self.getNearby(coords)
        #         nearbySameColor = {i:nearby[i] for i in nearby if nearby[i] == player}

        #         for point in nearbySameColor :
        #             align = -1
        #             lineLength = 0
        #             equation = segmentEquation(coords,point)
        #             for i in (-1,1):
        #                 x = coords[0]
        #                 y = coords[1]
        #                 while x >=0 and x <=6 and y >= 0 and y <= 5 and self.grid[x][y] == player :
        #                     align+=1
        #                     x += equation[1]*i
        #                     if equation[1]*equation[0] == 0 :
        #                         y += equation[0]*i
        #                     else :
        #                         y -= equation[0]*i
        #                     align+=1
        #                     x += equation[1]*i
        #                     y += equation[0]*i
        #                     y = int(y)
        #                     x = int(x)

        #             if align >= 4:
        #                 return player

        return 0

    def play(self, column):
        """
        a function placing a pawn for the current player in the indicated column and detecting errors

        param column : int - between 0 and 6, the column which you want to place your pawn in
        return : int - 0 if the column is full, 1/2 if no problem to indicate the next player
        """

        currentColumn = self.grid[column]

        if not 0 in currentColumn:
            return 0

        currentColumn = currentColumn[::-1]
        indexFirstBlank = currentColumn.index(0)
        indexPawn = 5 - indexFirstBlank

        self.grid[column][indexPawn] = self.currentPlayer

        self.currentPlayer = (
            -self.currentPlayer + 3
        )  # function to invert currentPlayer : 1 => 2 and 2 => 1
        self.turns += 1

        return (
            self.currentPlayer,
            self.win((column, indexPawn), -self.currentPlayer + 3),
        )


if __name__ == "__main__":
    game = JeuPuissance4()
    game.grid = [
        [0, 0, 0, 1, 2, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 1, 2],
        [0, 0, 0, 0, 1, 1],
    ]
    assert game.win((5, 0), 2) == 2
    print(game, "\n")

    game.grid = [
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 1, 1, 1],
        [2, 1, 1, 2, 1, 2],
        [0, 0, 0, 1, 2, 2],
        [2, 1, 2, 2, 1, 2],
        [0, 0, 0, 1, 2, 1],
    ]
    assert game.win((0, 5), 1) == 1
    print(game, "\n")

    game.grid = [
        [0, 2, 1, 2, 1, 2],
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 2],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 2, 2],
    ]
    assert game.win((4, 4), 1) == 1
    print(game, "\n")

    game.grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 1, 1, 1],
        [2, 1, 1, 2, 1, 2],
        [0, 0, 0, 1, 2, 2],
        [2, 1, 2, 2, 1, 2],
        [0, 0, 0, 1, 2, 1],
    ]
    assert game.win((1, 4), 1) == 0
    print(game, "\n")

    game.turns = 42
    game.grid = [
        [2, 2, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 2],
        [1, 1, 1, 2, 2, 1],
        [1, 2, 2, 1, 1, 2],
        [2, 2, 1, 1, 2, 1],
        [2, 1, 2, 1, 2, 1],
        [2, 1, 1, 2, 2, 1],
    ]
    assert game.win((0, 0), 2) == 3
    print(game, "\n")
