"""
Daniel Rostin
Tetris

"""

#~~~~~~~~~~~~SET UP~~~~~~~~~~
import pygame, sys, random
pygame.init()

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Daniel's Super Original and Awesome Tetris")

clock = pygame.time.Clock()

#Sound Set up
pygame.mixer.init()
pygame.mixer.music.load("MainTheme.mp3")
pygame.mixer.music.play(-1)


#~~~~~~~COLOURS~~~~~~~~~~~~~~
class Colours:
    DarkGrey = (26, 31, 40)
    Green = (47, 230, 23)
    Red = (232, 18, 18)
    Orange = (226, 116, 17)
    Yellow = (237, 234, 4)
    Purple = (166, 0, 247)
    Cyan = (21, 204, 209)
    Blue = (13, 64, 216)
    White = (255, 255, 255)
    DarkBlue = (44, 44, 127)
    LightBlue = (59, 85, 162)


    @classmethod 
    def fnGetCellColours(cls):
        #Pre: Colours class must be defined. 
        #Post: Returns list of colour values in RGB in tuples
        return [cls.DarkGrey, cls.Green, cls.Red, cls.Orange, cls.Yellow, cls.Purple, cls.Cyan, cls.Blue]
    

#~~~~~USER INTERFACE~~~~~~~
#Text fonts + sizes
TitleFont = pygame.font.Font(None, 40)
BasicFont = pygame.font.Font(None, 36) 

#Score 
strScore = TitleFont.render("Score", True, Colours.White)
ScoreRectangle = pygame.Rect(320, 55, 170, 60)

#Next block
strNext = TitleFont.render("Next", True, Colours.White)
NextRectangle = pygame.Rect(320, 215, 170, 180)

#Game over text
strGameOver = TitleFont.render("GAME OVER", True, Colours.White)



#~~~~~INTRO SCREEN~~~~~~~~~~~~
def fnShowIntroScreen(screen):
    #Pre: Screen is a valid pygame surface.
    #Post: Displays the intro screen
    screen.fill(Colours.DarkBlue)

    # Title Text
    strTitle = TitleFont.render("Daniel's Super Cool Tetris", True, Colours.White)
    TitleRect = strTitle.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    screen.blit(strTitle, TitleRect)

    # Instruction Text
    instructions = [
        "Arrow Keys to Move",
        "Up Arrow to Rotate",
        "Down Arrow to Move Down Faster",
        "Press Any Key to Start and Good Luck!"
    ]

    InstructionYPosition = screen.get_height() // 2
    for line in instructions:
        InstructionSurface = BasicFont.render(line, True, Colours.LightBlue)
        InstructionRectangle = InstructionSurface.get_rect(center=(screen.get_width() // 2, InstructionYPosition))
        screen.blit(InstructionSurface, InstructionRectangle)
        InstructionYPosition += 40

    pygame.display.update()




#~~~~~~POSITIONS~~~~~~~~~~~
class Position:
    def __init__(self, iRow, iColumn):
        #Pre: iRow and iColumn are integers
        #Post: Initializes the Position object
        self.iRow = iRow
        self.iColumn = iColumn


#~~~~~~~~BLOCK~~~~~~~~~~
class Block:
    def __init__(self, iIdentifier):
        #Pre: iIdentifier is a valid integer.
        #Post: Initializes Block object with specified iIdentifier to set up cell positions, colours, etc.
        self.iIdentifier = iIdentifier
        self.Cells = {}
        self.iCellSize = 30
        self.iRowOffset = 0
        self.iColumnOffset = 0
        self.iRotationState = 0
        self.Colours = Colours.fnGetCellColours()

    def fnMove(self, iRows, iColumns):
        #Pre: iRows and iColumns are valid integers.
        #Post: Updates the iRowOffSet and iColumnOffSet to show movement.
        self.iRowOffset += iRows
        self.iColumnOffset += iColumns

    def fnGetCellPositions(self):
        #Pre: Block's cells attribute and iRotationState are initialized.
        #Post: Returns list of position objects showing the new locations of the block's cells after offsets.
        tiles = self.Cells[self.iRotationState]
        MovedTiles = []
        for position in tiles:
            position = Position(position.iRow + self.iRowOffset, position.iColumn + self.iColumnOffset) 
            MovedTiles.append(position)
        return MovedTiles
    
    def fnRotate(self):
        # Pre: iRotationState is initialized.
        # Post: Rotates the block by updating iRotationState.
        self.iRotationState = (self.iRotationState + 1) % len(self.Cells)

    def fnUndoRotation(self):
        # Pre: iRotationState is initialized.
        # Post: Undoes the block's rotation
        self.iRotationState = (self.iRotationState - 1) % len(self.Cells)

    def fnDraw(self, screen, iOffsetX, iOffsetY):
        #Pre: Screen is a valid pygame surface and offsets are integers
        #Post:Draws the block's cells on the screen.
        tiles = self.fnGetCellPositions()
        for tile in tiles:
            TileRect = pygame.Rect(iOffsetX + tile.iColumn * self.iCellSize, iOffsetY + tile.iRow * self.iCellSize, self.iCellSize -1, self.iCellSize -1)
            pygame.draw.rect(screen, self.Colours[self.iIdentifier], TileRect)


#~~~~~~~~~~~~Block Shapes~~~~~~~~~~~~
class LBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 1)
        self.Cells = {
            0: [Position(0, 2), Position(1, 0), Position(1,1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2,1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1,2), Position(2, 0)], 
            3: [Position(0, 0), Position(0, 1), Position(1,1), Position(2, 1)]
        }
        self.fnMove(0, 3)

class JBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 2)
        self.Cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.fnMove(0, 3)

class IBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 3)
        self.Cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],  # Horizontal
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)]   # Vertical
        }
        self.fnMove(-1, 3)

class OBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 4)
        self.Cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.fnMove(0, 4)

class SBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 5)
        self.Cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.fnMove(0, 3)

class TBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 6)
        self.Cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.fnMove(0, 3)

class ZBlock(Block):
    def __init__(self):
        #Pre: Calls Block class with iIdentifier and sets up cell positions for shape.
        #Post: Initializes block's unique shape and sets the starting position.
        super().__init__(iIdentifier = 7)
        self.Cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.fnMove(0, 3)


#~~~~~~~GRID~~~~~~~~~~~
class Grid:
    def __init__(self):
        #Pre: None.
        #Post: Initializes the grid and sets grid cells to 0.
        self.iNumRows = 20
        self.iNumCols = 10
        self.iCellSize = 30
        self.grid = [[0 for j in range(self.iNumCols)] for i in range(self.iNumRows)]
        self.colours = Colours.fnGetCellColours()

    def fnPrintGrid(self):
        #Pre: iNumRows and iNumCols are initialized.
        #Post: Prtins grid's current state.
        for iRow in range(self.iNumRows):
            for iColumn in range(self.iNumCols):
                print(self.grid[iRow][iColumn], end = " ")
            print()

    def fnInside(self, iRow, iColumn):
        #Pre: iRow and iColumn are valid integers
        #Post: Returns True if the row and column are within the grid and false otherwise.
        if iRow >= 0 and iRow < self.iNumRows and iColumn >= 0 and iColumn < self.iNumCols:
            return True
        return False
    
    def fnEmpty(self, iRow, iColumn):
        #Pre: iRow and iColumn are valid integers.
        #Post: Returns True if the cell is empty otherwise False.
        if self.grid[iRow][iColumn] == 0:
            return True
        return False 
    
    def fnRowFull(self, iRow):
        #Pre: iRow is a valid integer.
        #Post: Returns True if the row is full otherwise False.
        for iColumn in range(self.iNumCols):
            if self.grid[iRow][iColumn] == 0:
                return False 
        return True 
    
    def fnClearRow(self, iRow):
        #Pre: iRow is a valid integer.
        #Post: Clears the row.
        for iColumn in range(self.iNumCols):
            self.grid[iRow][iColumn] = 0

    def fnMoveRowDown(self, iRow, iNumRows):
        #Pre: iRow and iNumRows are valid integers.
        #Post: Moves the row down by iNumRows and clears originl row.
        for iColumn in range(self.iNumCols):
            self.grid[iRow + iNumRows][iColumn] = self.grid[iRow][iColumn]
            self.grid[iRow][iColumn] = 0

    def fnClearFullRows(self):
        #Pre: None.
        #Post: Clears all full rows and moves remaining rows down.
        completed = 0
        for iRow in range(self.iNumRows - 1, 0, -1):
            if self.fnRowFull(iRow):
                self.fnClearRow(iRow)
                completed += 1
            elif completed > 0:
                self.fnMoveRowDown(iRow, completed)
        return completed
    
    def fnReset(self):
        #Pre: None.
        #Post: Resets the entire grid.
        for iRow in range(self.iNumRows):
            for iColumn in range (self.iNumCols):
                self.grid[iRow][iColumn] = 0
    
    def fnDraw(self, screen):
        #Pre: Screen is a valid pygame surface.
        #Post: Draws the entire grid. 
        for iRow in range(self.iNumRows):
            for iColumn in range(self.iNumCols):
                CellValue = self.grid[iRow][iColumn]
                CellRect = pygame.Rect(iColumn * self.iCellSize + 11, iRow * self.iCellSize + 11, self.iCellSize - 1, self.iCellSize - 1)
                pygame.draw.rect(screen, self.colours[CellValue], CellRect)


#~~~~~~~~~GAME~~~~~~~~~~~~~~~~
class Game:
    def __init__(self):
        #Pre: None.
        #Post:Initializes the game, creates a grid, block list, score, speed and sets current and next blocks.
        self.Grid = Grid()
        self.Blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.CurrentBlock = self.fnGetRandomBlocks()
        self.NextBlock = self.fnGetRandomBlocks()
        self.boolGameOver = False
        self.iScore = 0
        self.Speed = 250

    def fnUpdateScore(self, iLinesCleared, iMoveDownPoints):
        #Pre: iLinesCleared is an integer between 0-3 and iMoveDownPoints is non-negative integer.
        #Post: Score is updated based on how many lines have been cleared or from moving down.
        if iLinesCleared == 1:
            self.iScore += 100
        elif iLinesCleared == 2:
            self.iScore += 300
        elif iLinesCleared == 3:
            self.iScore += 500
        self.iScore += iMoveDownPoints

    def fnGetRandomBlocks(self):
        #Pre: self.Blocks has at least one block in the list.
        #Post: Returns a random block from the list and removes it from avaliable list of blocks. If the list is empty, it will reset the list. 
        if len(self.Blocks) == 0:
            self.Blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        Block = random.choice(self.Blocks)
        self.Blocks.remove(Block)
        return Block 
    
    def fnMoveLeft(self):
        #Pre: The current block is inside the grid.
        #Post: Moves current block one column left. Will revert to original position if it results in the block leaving the grid.
        self.CurrentBlock.fnMove(0, -1)
        if self.fnBlockInside() == False or self.fnBlockFits() == False:
            self.CurrentBlock.fnMove(0, 1)

    def fnMoveRight(self):
        #Pre: The current block is inside the grid.
        #Post: Moves the current block one column right. Will revert to original position if it results in the block leaving the grid. 
        self.CurrentBlock.fnMove(0, 1)
        if self.fnBlockInside() == False or self.fnBlockFits() == False:
            self.CurrentBlock.fnMove(0, -1)

    def fnMoveDown(self):
        #Pre: The current block is inside the grid.
        #Post: Moves the current block one row down. The block is locked and a new one is spawned if it can't go further down. 
        self.CurrentBlock.fnMove(1, 0)
        if self.fnBlockInside() == False or self.fnBlockFits() == False:
            self.CurrentBlock.fnMove(-1, 0)
            self.fnLockBlock()

    def fnLockBlock(self):
        #Pre: The current block is inside the grid.
        #Post: Places the current block on the grid, clears any full rows, updates, the score, and sets the next block. Will end the game if next block doesn't fit.
        tiles = self.CurrentBlock.fnGetCellPositions()
        for position in tiles:
            self.Grid.grid[position.iRow][position.iColumn] = self.CurrentBlock.iIdentifier
        self.CurrentBlock = self.NextBlock
        self.NextBlock = self.fnGetRandomBlocks()
        RowsCleared = self.Grid.fnClearFullRows()
        self.fnUpdateScore(RowsCleared, 0)
        if self.fnBlockFits() == False:
            self.boolGameOver = True
    
    def fnReset(self):
        #Pre: None.
        #Post: Resets the game (the grid, blocks, and score).
        self.Grid.fnReset()
        self.Blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.CurrentBlock = self.fnGetRandomBlocks()
        self.NextBlock = self.fnGetRandomBlocks()
        self.iScore = 0

    def fnBlockFits(self):
        #Pre: None.
        #Post: Returns True if current block fits in current position, otherwise false.
        tiles = self.CurrentBlock.fnGetCellPositions()
        for tile in tiles:
            if self.Grid.fnEmpty(tile.iRow, tile.iColumn) == False:
                return False
        return True

    def fnRotate(self):
        # Pre: The current block is inside the grid.
        # Post: Rotates the current block. Reverts to original position if the new position is out of the grid or merged into other block.
        self.CurrentBlock.fnRotate()
        if not self.fnBlockInside() or not self.fnBlockFits():
            self.CurrentBlock.fnUndoRotation()


    def fnBlockInside(self):
        #Pre: None.
        #Post: Returns True if the current block is completel inside the grid and false if it isn't.
        tiles = self.CurrentBlock.fnGetCellPositions()
        for tile in tiles:
            if self.Grid.fnInside(tile.iRow, tile.iColumn) == False:
                return False
        return True
    

    def fnDraw(self, screen):
        #Pre: Screen is a valid pygame surface.
        #Post: Draws the grid, current block, and next block on the screen
        self.Grid.fnDraw(screen)
        self.CurrentBlock.fnDraw(screen, 11, 11)
        self.NextBlock.fnDraw(screen, 270, 270)
    

#~~~~SANDBOX~~~~~
game = Game()

GameUpdate = pygame.USEREVENT
pygame.time.set_timer(GameUpdate, 250)


#~~~~GAME LOOP~~~~~~
IntroScreen = True 
GameOverTime = None  
FlashInterval = 500 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if IntroScreen:
            if event.type == pygame.KEYDOWN:
                IntroScreen = False 
        else:
            if game.boolGameOver:
                if GameOverTime is None: 
                    GameOverTime = pygame.time.get_ticks()
                
                if pygame.time.get_ticks() - GameOverTime > 2000: 
                    if event.type == pygame.KEYDOWN:
                        game.boolGameOver = False
                        game.fnReset()
                        GameOverTime = None  
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.fnMoveLeft()
                    if event.key == pygame.K_RIGHT:
                        game.fnMoveRight()
                    if event.key == pygame.K_DOWN:
                        game.fnMoveDown()
                        game.fnUpdateScore(0, 1)
                    if event.key == pygame.K_UP:
                        game.fnRotate()
                if event.type == GameUpdate:
                    game.fnMoveDown()

    # Draw
    if IntroScreen:
        fnShowIntroScreen(screen) 
    else:
        screen.fill(Colours.DarkBlue)

        screen.blit(strScore, (365, 20, 50, 50))
        screen.blit(strNext, (375, 180, 50, 50))
        pygame.draw.rect(screen, Colours.LightBlue, ScoreRectangle, 0, 10)
        ScoreValueSurface = TitleFont.render(str(game.iScore), True, Colours.White)
        screen.blit(ScoreValueSurface, ScoreValueSurface.get_rect(centerx = ScoreRectangle.centerx, centery = ScoreRectangle.centery))
        pygame.draw.rect(screen, Colours.LightBlue, NextRectangle, 0, 10)

        game.fnDraw(screen)

        if game.boolGameOver:
            CurrentTime = pygame.time.get_ticks()
            if (CurrentTime // FlashInterval) % 2 == 0: 
                screen.blit(strGameOver, (320, 450, 50, 50))

    pygame.display.update()
    clock.tick(60)