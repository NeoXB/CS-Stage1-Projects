""" COMPSCI 130, Semester 1 2019
Project Two - Creatures
Author: Nicholas Tony
ID: 124598632
UPI: nton939"""
import turtle
import hashlib
 
class Creature:
    """This class represents a creature"""
 
    def __init__(self, row, col, dna, direction):
        """A creature stores its position and direction and its "DNA" -
        the list of instructions it follows"""
        self.direction = direction
        self.row = row
        self.col = col
        self.dna = dna
        self.next_instruction = 1

    def draw(self, grid_size, top_left_x, top_left_y):
        """ A creature draws itself using the colour specified as part of its dna
        the size of the grid squares, and the position of the top-left pixel are
        provided as input"""

        ## Compute the position of the top left hand corner of the cell this creature is in
        x = top_left_x + (self.col-1)*grid_size
        y = top_left_y - (self.row-1)*grid_size
        turtle.color(self.dna[0].split(":")[1])   

        ## Draw the creature
        turtle.goto(x, y)
        turtle.pendown()
        turtle.begin_fill()
        if self.direction == 'North':
            turtle.goto(x + grid_size/2, y)
            turtle.goto(x + grid_size, y - grid_size)
            turtle.goto(x, y - grid_size)
            turtle.goto(x + grid_size/2, y)
        elif self.direction == 'East':
            turtle.goto(x + grid_size, y - grid_size/2)
            turtle.goto(x + grid_size, y - grid_size/2)
            turtle.goto(x, y - grid_size)
            turtle.goto(x, y)
        elif self.direction == 'South':
            turtle.goto(x + grid_size, y)
            turtle.goto(x + grid_size/2, y - grid_size)
            turtle.goto(x, y)
        elif self.direction == 'West':
            turtle.goto(x + grid_size, y)
            turtle.goto(x + grid_size, y - grid_size)
            turtle.goto(x, y - grid_size/2)
            turtle.goto(x + grid_size, y)
        turtle.end_fill()
        turtle.penup()
        turtle.color("black")

    def get_species(self):
        """Returns the name of the species for this creature"""
        return self.dna[0].split(":")[0]

    def get_position(self):
        """Gets the current position of the creature"""
        return (self.row, self.col)

    def get_direction(self):
        """Gets the current direction of the creature"""
        return self.direction

    def __str__(self):
        """Returns a string representation of the creature"""
        return str(self.get_species() + ' ' + str(self.row) + ' ' + str(self.col) + ' ' + str(self.direction))

    def get_next_position(self):
        """Returns the next position of the creature"""
        ahead_row = self.row
        ahead_col = self.col
        if self.direction == 'North':
            ahead_row = ahead_row - 1 
        elif self.direction == 'South':
            ahead_row = ahead_row + 1 
        elif self.direction == 'East':
            ahead_col = ahead_col + 1 
        elif self.direction == 'West':
            ahead_col = ahead_col - 1
        return (ahead_row, ahead_col)
        
    def make_move(self, world):
        """Execute a single move (either hop, left or right) for this creature by
        following the instructions in its dna"""
        finished = False
        # Find out what lies ahead
        ahead_row = self.row
        ahead_col = self.col
        if self.direction == 'North':
            ahead_row = ahead_row - 1 
        elif self.direction == 'South':
            ahead_row = ahead_row + 1 
        elif self.direction == 'East':
            ahead_col = ahead_col + 1 
        elif self.direction == 'West':
            ahead_col = ahead_col - 1 
        ahead_value = world.get_cell(ahead_row, ahead_col)

        # Continue to execute the creature's instructions until a "hop" instruction is reached
        while not finished:
            next_op = self.dna[self.next_instruction]
            op = next_op.split()
            ################## GO ##########################2
            if op[0] == 'go':
                self.next_instruction = int(op[1])
            ################## HOP #########################3
            if op[0] == 'hop':
                if ahead_value == 'EMPTY':
                    self.row = ahead_row
                    self.col = ahead_col
                self.next_instruction = self.next_instruction + 1
                finished = True
            ################## REVERSE #####################4
            if op[0] == 'reverse':
                if self.direction == "North":
                    self.direction = "South"
                elif self.direction == "South":
                    self.direction = "North"
                elif self.direction == "East":
                    self.direction = "West"
                else:
                    self.direction = "East"
                self.next_instruction += 1
                finished = True
            ################## IFNOTWALL ###################5
            if op[0] == 'ifnotwall':
                if ahead_value == 'EMPTY':
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
            ################## TWIST #######################6
            if op[0] == 'twist':
                if self.direction == 'North':
                    self.direction = 'East'
                elif self.direction == 'East':
                    self.direction = 'South'
                elif self.direction == 'South':
                    self.direction = 'West'
                else:
                    self.direction = 'North'
                self.next_instruction += 1
                finished = True
            ################## IFSAME ######################7 
            if op[0] == 'ifsame':
                ifsame = False
                ahead_coord = self.get_next_position()
                for creature in world.creature:
                    if ahead_coord == creature.get_position():
                        if self.dna == creature.dna:
                            ifsame = True

                if True:
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
            ################# IFENEMY ######################8
            if op[0] == 'ifenemy':
                enemy = None
                ifenemy = False
                ahead_coord = self.get_next_position()
                for creature in world.creature:
                    if ahead_coord == creature.get_position():
                        if self.dna != creature.dna:
                            ifenemy = True
                            enemy = creature
                            self.next_instruction = int(op[1])
                        break
            
                if ifenemy == False:
                    self.next_instruction += 1
            ################ IFRANDOM ######################9
            if op[0] == 'ifrandom':
                if world.pseudo_random() == 1:
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
            ################ INFECT ########################10
            if op[0] == 'infect':
                if enemy:
                    for creature in world.creature:
                        if creature == enemy:
                            creature.dna = self.dna
                            creature.next_instruction = 1
                self.next_instruction += 1
                finished = True

class World:
    """This class represents the grid-based world"""

    def __init__(self, size, max_generations):
        """The world stores its grid-size, and the number of generations to be
        executed.  It also stores a creature."""
        self.size = size
        self.generation = 0
        self.max_generations = max_generations
        self.creature = []   #5

    def add_creature(self, c):
        """Adds a creature to the world"""
        self.creature.append(c)

    def get_cell(self, row, col):
        """Gets the contents of the specified cell.  This could be 'WALL' if the
        cell is off the grid or 'EMPTY' if the cell is unoccupied"""
        if row <= 0 or col <= 0 or row >= self.size + 1 or col >= self.size + 1:
            return 'WALL'            
        return 'EMPTY'

    def simulate(self):
        """Executes one generation for the world - the creature moves once.
        If there are no more generations to simulate, the world is printed"""
        if self.generation < self.max_generations:
            for creature in self.creature:
                creature.make_move(self)
            self.generation += 1
            return False
        else:
            print(self)
            return True

    def __str__(self):
        """Returns a string representation of the world"""
        creature_dict = {}
        for creature in self.creature:
            if creature.get_species() not in creature_dict:
                creature_dict[creature.get_species()] = 1
            else:
                creature_dict[creature.get_species()] += 1
                
        creature_count_list = []
        for creature_count in creature_dict.values():
            if creature_count not in creature_count_list:
                creature_count_list.append(creature_count)

        creature_list = []
        for creature_count in sorted(creature_count_list, reverse = True):
            new_dict = {}
            for creature in creature_dict:
                if creature_dict[creature] == creature_count:
                    new_dict[creature] = creature_count
            creature_list.append(new_dict)

        new_creature_list = []
        for a_dict in creature_list:
            for creature in sorted(a_dict.keys()):
                creature_tuple = (creature, a_dict[creature])
                new_creature_list.append(creature_tuple)

        string = str(self.size) + '\n' + str(new_creature_list) + '\n'

        for creature in self.creature:
            string += (creature.get_species() + ' ' +
                       str(creature.get_position()[0]) + ' ' +
                       str(creature.get_position()[1]) + ' ' +
                       creature.get_direction() + '\n')
        
        return string
        
    def draw(self):
        """Display the world by drawing the creature, and placing a grid around it"""

        # Basic coordinates of grid within 800x800 window - total width and position of top left corner
        grid_width = 700
        top_left_x = -350
        top_left_y = 350
        grid_size = grid_width / self.size

        # Draw the creature
        for creature in self.creature:
            creature.draw(grid_size, top_left_x, top_left_y)

        # Draw the bounding box
        turtle.goto(top_left_x, top_left_y)
        turtle.setheading(0)
        turtle.pendown()
        for i in range(0, 4):
            turtle.rt(90)
            turtle.forward(grid_width)
        turtle.penup()

        # Draw rows
        for i in range(self.size):
            turtle.setheading(90)
            turtle.goto(top_left_x, top_left_y - grid_size*i)
            turtle.pendown()
            turtle.forward(grid_width)
            turtle.penup()

        # Draw columns
        for i in range(self.size):
            turtle.setheading(180)
            turtle.goto(top_left_x + grid_size*i, top_left_y)
            turtle.pendown()
            turtle.forward(grid_width)
            turtle.penup()

    def pseudo_random(self):
        """Returns a random number that is completely determined by the positions of
        the creatures in the world."""
        sums = 0
        for creature in self.creature:
            sums += creature.get_position()[0] + creature.get_position()[1]
        sums *= self.generation
        string_total = str(sums)
        return int(hashlib.sha256(string_total.encode()).hexdigest(), 16) % 2
    
class CreatureWorld:
    """This class reads the data files from disk and sets up the window"""

    def __init__(self):
        """Initialises the window, and registers the begin_simulation function to be
        called when the space-bar is pressed"""
        self.framework = SimulationFramework(800, 800, 'COMPSCI 130 Project Two')
        self.framework.add_key_action(self.begin_simulation, ' ')
        self.framework.add_tick_action(self.next_turn, 100) # Delay between animation "ticks" - smaller is faster.

    def begin_simulation(self):
        """Starts the animation"""
        self.framework.start_simulation()

    def end_simulation(self):
        """Ends the animation"""
        self.framework.stop_simulation()

    def setup_simulation(self):
        """Reads the data files from disk"""
        
        ## If new creatures are defined, they should be added to this list: #6
        all_creatures = ['Hopper', 'Parry', 'Rook', 'Roomber', 'Randy', 'Flytrap',
                         'Guard', 'SpinnerGuard']        

        # Read the creature location data
        with open('world_input.txt') as f:
            world_data = f.read().splitlines()

        # Read the dna data for each creature type
        dna_dict = {}
        for creature in all_creatures:
            with open('Creatures//' + creature + '.txt') as f:
                dna_dict[creature] = f.read().splitlines()        

        # Create a world of the specified size, and set the number of generations to be performed when the simulation runs
        world_size = world_data[0]
        world_generations = world_data[1]
        self.world = World(int(world_size), int(world_generations))
        creature_list = []
        coordinate_list = []
        for i in range(2, len(world_data)):
            data = world_data[i].split()
            coordinate = (int(data[1]), int(data[2]))
            if coordinate not in coordinate_list:
                coordinate_list.append(coordinate)
                creature_list.append(world_data[i])
                
        for creature in creature_list:
            data = creature.split()            
            self.world.add_creature(Creature(int(data[1]), int(data[2]), dna_dict[data[0]], data[3]))

        # Draw the initial layout of the world
        self.world.draw()

    def next_turn(self):
        """This function is called each time the animation loop "ticks".
        The screen should be redrawn each time."""         
        turtle.clear()
        self.world.draw() 
        if self.world.simulate():
            self.end_simulation()

    def start(self):
        """This function sets up the simulation and starts the animation loop"""
        self.setup_simulation() 
        turtle.mainloop() # Must appear last.


class SimulationFramework:
    """This is the simulation framework - it does not need to be edited"""

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
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
        
    def start_simulation(self):
        self.simulation_running = True
        
    def stop_simulation(self):
        self.simulation_running = False

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func, delay):
        self.tick = func
        self.delay = delay

    def __animation_loop(self):
        if self.simulation_running:
            self.tick()
        turtle.ontimer(self.__animation_loop, self.delay)
   
cw = CreatureWorld()
cw.start()
