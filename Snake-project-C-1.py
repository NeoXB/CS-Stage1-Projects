import turtle
import random

class sSnake:
    def __init__(self, snake):
        self.call = snake
        self.movement = True
        self.call.snakeColors = [('white', '#84089B'),
                                 ('#08219B', '#E94D1B'),
                                 ('', 'white')]
        self.direction = {'right'   : self.call.snakeSize,
                          'left'    : -self.call.snakeSize,
                          'up'      : self.call.snakeSize,
                          'down'    : -self.call.snakeSize}
        self.call.draw()
        self.isInvalidMove = False
        self.isTargetHit = False
        self.testspawns = 0
        self.oppositePlane = {'horizontal':'vertical', 'vertical':'horizontal'}
        self.axis = {'horizontal': ['left', 'right'], 'vertical': ['down', 'up']}

    def new_move(self, direction='up'):
        #move the snake in the direction given by adding a new
        #head position to the list of locations, and removing
        #the end of the snake.  The snake grows automatically every 10
        #moves.  That is, every 10 moves, the tail of the snake is not
        #removed.

        coords = (self.call.moveData[direction][0], self.call.moveData[direction][1])
        
        tail = self.call.playerSnakeSeg[0]
        
        if self.movement:
            
            head = self.shortest_path()
            if not self.isTargetHit:
                self.call.playerSnakeSeg = self.call.playerSnakeSeg[1:]
            else:
                self.isTargetHit = False
                self.call.playerSnakeSize += 1
                
            self.call.playerSnakeSeg.append(head)

    def future_collision(self, plane, coords):
        if plane == 'vertical':
            future_coords = (self.call.playerSnakeSeg[-1][0], self.call.playerSnakeSeg[-1][1]+coords)
        else:
            future_coords = (self.call.playerSnakeSeg[-1][0]+coords, self.call.playerSnakeSeg[-1][1])
        return (future_coords in self.call.playerSnakeSeg)

    def shortest_path_movement(self, plane, value, value2):
        self.is_blocking(self.call.previousMove)
        if not self.isInvalidMove:
            coords = self.direction[self.axis[plane][0]]
            if value < 0 and self.call.previousMove != self.axis[plane][1]:
                self.call.previousMove = self.axis[plane][0]
                if self.future_collision(plane, coords):
                    plane = self.oppositePlane[plane]
                    if not (value < 0 and value2 > 0):
                        self.call.previousMove = self.axis[plane][0]
                        coords = self.direction[self.axis[plane][0]]
                        if self.future_collision(plane, coords):
                            self.call.previousMove = self.axis[plane][1]
                            coords = self.direction[self.axis[plane][1]]
                    else:
                        self.call.previousMove = self.axis[plane][1]
                        coords = self.direction[self.axis[plane][0]]*-1
                if plane == 'horizontal':
                    return (self.call.playerSnakeSeg[-1][0]+coords, self.call.playerSnakeSeg[-1][1])
                else:
                    return (self.call.playerSnakeSeg[-1][0], self.call.playerSnakeSeg[-1][1]+coords)
            self.is_blocking(self.axis[plane][1])
            if value > 0 and not self.isInvalidMove:
                coords = self.direction[self.axis[plane][1]]
                self.call.previousMove = self.axis[plane][1]
                if plane == 'horizontal':
                    return (self.call.playerSnakeSeg[-1][0]+coords, self.call.playerSnakeSeg[-1][1])
                else:
                    return (self.call.playerSnakeSeg[-1][0], self.call.playerSnakeSeg[-1][1]+coords)

                
            # if value one tile greater than the boundary move up/down
            self.isInvalidMove = False
            if plane == 'horizontal' and (self.call.previousMove == 'left' or self.call.previousMove == 'right'):
                if (value2 > 0 and value < 0):
                    coords = self.direction[self.axis[plane][1]]
                    self.call.previousMove = self.axis['vertical'][1]
                elif (value2 < 0 and value < 0):
                    coords = self.direction[self.axis[plane][0]]
                    self.call.previousMove = self.axis['vertical'][0]        
                else:
                    coords = self.direction[self.axis[plane][0]]
                    self.call.previousMove = self.axis['vertical'][0]
                    if self.future_collision(plane, coords):
                        plane = self.oppositePlane[plane]
                        self.call.previousMove = self.axis[plane][1]
                        coords = self.direction[self.axis[plane][1]]
                return (self.call.playerSnakeSeg[-1][0], self.call.playerSnakeSeg[-1][1]+coords)

            if plane == 'vertical' and (self.call.previousMove == 'up' or self.call.previousMove == 'down'):
                coords = self.direction[self.axis[plane][1]]
                self.call.previousMove = self.axis['horizontal'][1]
                return (self.call.playerSnakeSeg[-1][0]+coords, self.call.playerSnakeSeg[-1][1])

    def shortest_path_no_obstruction(self, xLeft, yLeft):
        self.isInvalidMove = False
        if xLeft != 0:
            head = self.shortest_path_movement('horizontal', xLeft, yLeft)
            if not self.isInvalidMove:
                return head

        self.isInvalidMove = False
        if yLeft != 0:
            head = self.shortest_path_movement('vertical', yLeft, xLeft)
            if not self.isInvalidMove:
                return head

        self.isInvalidMove = False
        if xLeft == 0:
            head = self.shortest_path_movement('vertical', yLeft, xLeft)
            if not self.isInvalidMove:
                return head

        self.isInvalidMove = False
        if yLeft == 0:
            head = self.shortest_path_movement('horizontal', xLeft, yLeft)
            if not self.isInvalidMove:
                return head

        
        

    def shortest_path(self, isTargetHit=False):
        xLeft = self.call.targetLocation[0] - self.call.playerSnakeSeg[-1][0]
        yLeft = self.call.targetLocation[1] - self.call.playerSnakeSeg[-1][1]

        if xLeft != 0 or yLeft != 0:
            head = self.shortest_path_no_obstruction(xLeft, yLeft)
        else:
            
            self.call.target.spawn(self.call.playerSnakeSeg, self.snake.playerSnakeSeg)
            self.testspawns += 1
            self.call.targetLocation = (self.call.target.coords.x, self.call.target.coords.y)
            self.snake.targetLocation = (self.call.target.coords.x, self.call.target.coords.y)
            self.isTargetHit = True
            
            head = self.shortest_path(True)

        return head

    def is_blocking(self, direction):
        if (self.call.previousMove == self.call.obstruction[direction]):
            self.isInvalidMove = True      

    def avoid_player(self):
        pass

    def get_player(self, snake):
        self.snake = snake

    def snake_collision(self, snakeSegments):
        return (self.call.playerSnakeSeg[-1] in snakeSegments)

class RandomNumber:
    def __init__(self, snake1, snake2, size, bounds, isSnake = False):
        self.bounds = bounds
        self.size = size
        self.boundary = (max(self.bounds.values())-1)*self.size
        self.numSquaresX = (abs(self.bounds['left'])*size + (self.bounds['right']-1)*size) // size
        self.numSquaresY = (abs(self.bounds['bottom'])*size + (self.bounds['top']-1)*size) // size
        self.generate(snake1, snake2)
        
    def generate(self, playerSnake, enemySnake):
        self.x = playerSnake[0][1]
        self.y = playerSnake[0][1]
        while self.isInvalid((self.x,self.y), playerSnake, enemySnake):
            self.x = random.randrange(self.numSquaresX)*self.size-self.boundary
            self.y = random.randrange(self.numSquaresY)*self.size-self.boundary

    def isInvalid(self, coords, playerSnake, enemySnake):
        return (coords in playerSnake or coords in enemySnake)

class Target:
    def __init__(self, playerSnake, enemySnake, size, boundary):
        """ This class produces a target for a snake to hit """
        self.targetSize = size
        self.boundary = boundary
        self.size = size
        self.numSquares = 600 // self.targetSize
        self.colors = ('', '#0099cc')
        self.spawn(playerSnake, enemySnake)

    def draw_target(self, point):
        """ Create the target for the snake to hit """
        turtle.color(self.colors[0], self.colors[1])
        turtle.setpos(point.x, point.y)
        turtle.pendown()
        turtle.begin_fill()
        for _ in range(4):
            turtle.left(90) 
            turtle.forward(self.targetSize)
        turtle.end_fill()
        turtle.penup()
        
    def spawn(self, snake1, snake2):
        """ Logic to produce the target """
        self.coords = RandomNumber(snake1, snake2, self.size, self.boundary)
        self.draw_target(self.coords)

class Snake:
    #The snake moves by jumping one square at a time.
    def __init__(self, home, size, target, enemySnake):
        #home is the starting location (by default is 0, 0)
        #size is the size of the square in each cell of the snake
        #The snake location is stored as a list of tuples, where each tuple
        #is the position of a segment of the snake
        self.snakeSize = size
        self.snakeDefaultSeg = 3
        self.playerSnakeSize = self.snakeDefaultSeg
        self.enemySnake = enemySnake
        self.create_snake_body(home)
        
        
        self.snakeColors = [('white', '#00ff80'),
                            ('#ff00bf', '#ff9f00'),
                            ('', 'white')]
        self.moveData = {'up':(0,self.snakeSize),
                         'down':(0,-self.snakeSize),
                         'left':(-self.snakeSize,0),
                         'right':(self.snakeSize,0)}
        self.obstruction = {'up':'down', 'down':'up',
                            'left':'right','right':'left'}
        self.previousMove = 'left'
        self.outOfBounds = (320, -300)
        self.target = target
        self.targetLocation = (self.target.coords.x, self.target.coords.y)
        

    def create_snake_body(self, headLocation):
        """ Create the variable for the snake to store its segments """
        if self.enemySnake != None:
            headLocation = (0, 0)
        self.playerSnakeSeg = [
            (headLocation[0]+x*self.snakeSize, headLocation[1]) for x in range(self.snakeDefaultSeg, -1, -1)
            ]

    def enemy_collision(self, enemySnake):
        return (self.playerSnakeSeg[-1] in enemySnake)
        
    def draw_segment(self, point, color):
        #Draws a square equal to the size of the snake, where the location
        #given is the bottom left corner of the square
        turtle.setposition(point[0], point[1])
        turtle.color(color[0], color[1])
        turtle.pendown()
        turtle.begin_fill()
        for _ in range(4):
            turtle.left(90)
            turtle.forward(self.snakeSize)
        turtle.end_fill()
        turtle.penup()
    
    def draw(self):
        #Draws each of the segments, and then draws the head with red colour
        for coords in self.playerSnakeSeg[:self.playerSnakeSize]:
            self.draw_segment(coords,
                              self.snakeColors[0])
        self.draw_segment(self.playerSnakeSeg[-1],
                          self.snakeColors[1])
    
    def move(self, direction):
        #move the snake in the direction given by adding a new
        #head position to the list of locations, and removing
        #the end of the snake.  The snake grows automatically every 10
        #moves.  That is, every 10 moves, the tail of the snake is not
        #removed.
        self.draw_segment(self.playerSnakeSeg[0],
                          self.snakeColors[2])
        
        if (self.previousMove == self.obstruction[direction]):
            direction = self.previousMove
        else:
            self.previousMove = direction

        coords = (self.moveData[direction][0], self.moveData[direction][1])
        
        tail = self.playerSnakeSeg[0]
        head = (self.playerSnakeSeg[-1][0]+coords[0],
                self.playerSnakeSeg[-1][1]+coords[1])

        self.enemySnakeSeg = self.enemySnake.call.playerSnakeSeg
        if self.targetLocation != self.playerSnakeSeg[self.playerSnakeSize]:
            
            self.playerSnakeSeg = self.playerSnakeSeg[1:]
        else: 
            self.target.spawn(self.playerSnakeSeg, self.enemySnakeSeg)
            self.targetLocation = (self.target.coords.x, self.target.coords.y)
            self.enemySnake.call.targetLocation = (self.target.coords.x, self.target.coords.y)
            self.playerSnakeSize += 1

        self.playerSnakeSeg.append(head)
    
    def hit_self(self):
        #check if the head of the snake has hit one of its own segments
        return (self.playerSnakeSeg[-1] in
                self.playerSnakeSeg[:self.playerSnakeSize-1])

    def hit_bounds(self, bounds): #left, top, right, bottom bounding box
        #check if the snake has hit the bounds given
        boundary = bounds['right']*self.snakeSize
        return (self.playerSnakeSeg[-1][0] == boundary+20 or
                self.playerSnakeSeg[-1][0] == -boundary or
                self.playerSnakeSeg[-1][1] == boundary+20 or
                self.playerSnakeSeg[-1][1] == -boundary)

class SnakeGame:
    def __init__(self):
        #set up the window for the game, the methods that are called when keys are pressed, and
        #the method that is called each new game turn
        self.framework = GameFramework(800, 800, 'COMPSCI 130 Project')
        self.framework.add_key_action(self.move_right, 'Right')
        self.framework.add_key_action(self.move_up, 'Up')
        self.framework.add_key_action(self.move_down, 'Down')
        self.framework.add_key_action(self.move_left, 'Left')
        self.framework.add_key_action(self.setup_game, ' ') #Pressing space will restart the game
        self.framework.add_tick_action(self.next_turn, 100) #Delay (speed) is 100.  Smaller is faster.

    #set of methods to keep track of which key was most recently pressed
    def move_right(self):
        self.last_key = 'Right'

    def move_left(self):
        self.last_key = 'Left'

    def move_down(self):
        self.last_key = 'Down'

    def move_up(self):
        self.last_key = 'Up'
        
    def setup_game(self):
        #initializes starting variables and begins the animation loop
        self.last_key = 'None' #No initial direction specified
        self.snake_size = 20
        self.boundary_limit = {'left':-15, 'right':15, 'top':15, 'bottom':-15}
        self.spawn_points = {'left':-14, 'right':11, 'top':14, 'bottom':-14}
        snake_home = [(0,0),(20,0),(40,0),(60,0)]
        self.snake_boundary = [(-60,0),(-40,0),(-20,0),(0,0),(20,0),(40,0),(60,0)]
        self.target = Target(snake_home, [(0,0)], self.snake_size, self.boundary_limit)
        target_boundary = [(self.target.coords.x + self.snake_size*i,
                            self.target.coords.y) for i in range(5)]
        
        randstart = RandomNumber(self.snake_boundary,
                                 target_boundary, self.snake_size, self.spawn_points)
        self.enemySnake = sSnake(Snake((randstart.x, randstart.y),
                                       self.snake_size, self.target, None))
        self.snake = Snake(0,
                            self.snake_size, self.target, self.enemySnake)
        self.enemySnake.get_player(self.snake)
        self.framework.start_game()
    
    def draw_bounds(self):
        #draws the box that defines the limit for the snake
        left = self.boundary_limit['left']
        top = self.boundary_limit['top']
        size = self.snake_size
        turtle.goto(left * size, top * size)
        turtle.color('black', 'black')
        turtle.pendown()
        for i in range(0, 4): #Draw a bounding square
            turtle.rt(90)
            turtle.forward(abs(left) * size * 2)
        turtle.penup()

    def next_turn(self):
        #called each time the game 'ticks'
        turtle.clear()
        snake = self.snake
        if self.last_key == 'Right':
            snake.move('right')
        if self.last_key == 'Up':
            snake.move('up')
        if self.last_key == 'Down':
            snake.move('down')
        if self.last_key == 'Left':
            snake.move('left')
        self.draw_bounds()
        self.enemySnake.playerSnakeLocation = snake.playerSnakeSeg
        self.enemySnake.call.draw()
        snake.draw()
        if self.enemySnake.movement and self.last_key != 'None':
            self.enemySnake.new_move()
        self.target.draw_target(self.target.coords)
        if self.enemySnake.call.hit_self() or self.enemySnake.call.hit_bounds(self.boundary_limit) or self.enemySnake.snake_collision(snake.playerSnakeSeg):
            self.enemySnake.movement = False
        if snake.hit_self() or snake.hit_bounds(self.boundary_limit) or snake.enemy_collision(self.enemySnake.call.playerSnakeSeg):
            self.framework.stop_game() #game over
            
    def start(self):
        #starts the game
        self.setup_game() #set up the game.
        turtle.mainloop() #must appear last.


#Shouldn't need to edit this at all
class GameFramework:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.game_running = False
        self.tick = None #function to call for each animation cycle
        self.delay = 100 #default is .1 second.       
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.hideturtle() #prevent turtle appearance
        turtle.tracer(False) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything
        self.__animation_loop()
        
    def start_game(self):
        self.game_running = True
        
    def stop_game(self):
        self.game_running = False

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func, delay):
        self.tick = func
        self.delay = delay

    def __animation_loop(self):
        if self.game_running:
            self.tick()
        turtle.ontimer(self.__animation_loop, self.delay)
   
g = SnakeGame()
g.start()
