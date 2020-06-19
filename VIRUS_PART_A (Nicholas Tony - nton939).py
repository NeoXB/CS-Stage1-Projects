"""
COMPSCI 130, Semester 01 2019
Project One - Virus
Author: Nicholas Tony (nton939)
ID: 124598632
"""

import turtle
import random
 
class Virus:
    """This class will be the virus that is used to infect the people in the
    simulated world.
    """
    def __init__(self, colour, duration):
        self.colour = colour
        self.duration = duration
        
class Person:
    """This class represents every person in the simulated world.
    """
    def __init__(self, world_size):
        self.world_size = world_size
        self.radius = 7
        self.location = (0, 0)
        self.destination = (0, 0)
        self.colour = "black"
        self.duration = 0
        self.infected_before = False
        
    def _get_random_location(self):
        """This method assigns a random destination for the person using random
        locations. The random locations are not closer than 1 radius to the
        edge of the world boundaries.
        """
        x_range = (self.world_size[0] / 2) - self.radius
        y_range = (self.world_size[1] / 2) - self.radius
        random_x_coordinate = random.randrange(-x_range, x_range + 1)
        random_y_coordinate = random.randrange(-y_range, y_range + 1)
        self.destination = (random_x_coordinate, random_y_coordinate)
 
    def draw(self):
        """Person is drawn using a dot. Colour is used to implement viruses.
        """
        turtle.goto(self.location[0], self.location[1])
        turtle.pendown()
        turtle.dot(self.radius * 2, self.colour)
        turtle.penup()

    def collides(self, other):
        """If the distance between self and other is less than the diameter,
        True will be returned; False will be returned otherwise.
        """
        self_position = self.location
        other_position = other.location
        turtle.goto(self_position)
        if turtle.distance(other_position) < (self.radius * 2):
            return True
        else:
            return False

    def collision_list(self, list_of_others):
        """A list of people will be given at the start, then only those people
        who collided with self will be returned as a list.
        """
        collided_people = []
        for other in list_of_others:
            if self.collides(other):
                collided_people += [other]
        return collided_people

    def infect(self, virus):
        """A random person will be infected with the given virus.
        """
        self.colour = virus.colour
        self.duration = virus.duration
        self.infected_before = True

    def reached_destination(self):
        """Will return True if the current location is within 1 radius of the
        destination and False otherwise.
        """
        x_range = self.destination[0]
        y_range = self.destination[1]
        if (x_range - self.radius <= self.location[0] <= x_range + self.radius
            and
            y_range - self.radius <= self.location[1] <= y_range + self.radius):
            return True
        else:
            return False
    
    def progress_illness(self):
        """The hours of sickness are increased and the duration of virus are
        checked if it is reached. If the duration is reached, then the person
        will be cured.
        """
        if self.duration > 0:
            self.duration -= 1
        elif self.duration == 0:
            self.cured()
        else:
            pass
    
    def update(self):
        """Each person will be updated per hour by:
        - Moving each person using the move method.
        - If the destination of that person is reached, then a new destination
          will be set.
        - Any illness progresses if the person is infected.
        """
        if self.reached_destination():
            self._get_random_location()
        if not self.reached_destination():
            self.move()
        self.progress_illness()
    
    def move(self):
        """Person is moved towards the destination.
        """
        turtle.goto(self.location[0], self.location[1])
        angle_to_destination = turtle.towards(self.destination[0],
                                              self.destination[1])
        turtle.right(angle_to_destination)
        turtle.forward(self.radius/2)
        current_x_coordinate = turtle.xcor()
        current_y_coordinate = turtle.ycor()
        self.location = (current_x_coordinate, current_y_coordinate)
        turtle.home()
                   
    def cured(self):
        """A person that is infected will be cured but the person will remain
        IMMUNED FROM FUTURE INFECTIONS UNLESS the simulated world is RESETTED
        OR the population of the world is MANUALLY (deliberately) CURED.
        """
        self.colour = "black"
        self.duration = 0
      
class World:
    """This class represents a simulated world.
    """
    def __init__(self, width, height, n):
        self.size = (width, height)
        self.hours = 0
        self.people = []
        self.population = n
        self.add_person()
        self.infected = 0
        self.random_viruses = ["red", "lime"]
        self.duration_of_virus = 168 #hours in a week

    def add_person(self):
        """A person will be added to the list of people using this method.
        """
        for number_of_people in range(self.population):
            new_person = Person(self.size)
            self.people += [new_person]

    def infect_person(self):
        """A random person will be chosen to be infected with a random Virus
        but the random person will ONLY BE INFECTED IF THE PERSON HAS NOT BEEN
        INFECTED BEFORE.
        
        Two types of viruses are implemented for the simulation and they are
        differentiated by two colours: 'red' and 'lime'. Assume both viruses
        will last for exactly one week.
        """
        random_person_index = random.randrange(len(self.people))
        random_person = self.people[random_person_index]
        random_virus_index = random.randrange(2)
        current_virus = self.random_viruses[random_virus_index]
        if random_person.infected_before == False:
            random_person.infect(Virus(current_virus, self.duration_of_virus))

    def cure_all(self):
        """All people that HAVE BEEN INFECTED BEFORE will be cured by removing
        the infections.
        """
        for people in self.people:
            if people.infected_before == True:
                people.cured()
                people.infected_before = False

    def update_infections_slow(self):
        """Collisions between the people in the world population are checked and
        the virus from infected person(s) will be transmitted to other people
        only if collisions occur AND IF THE OTHER PEOPLE HAVE NOT BEEN INFECTED
        BEFORE.
        """
        for person in self.people:
            if person.colour != "black":
                check_people = []
                for check_person in self.people:
                    if check_person.infected_before == False:
                        check_people += [check_person]
                collided_people = person.collision_list(check_people)
                for contacted_person in collided_people:
                    contacted_person.infect(Virus(person.colour,
                                                  self.duration_of_virus))
                       
    def update_infections_fast(self):
        """This increases the efficiency of the collision detection.
        """
        pass
                    
    def simulate(self):
        """One hour in the world is simulated by:
        - Increasing the hours that passed.
        - All people in the world population updates.
        - All transmissions of virus infection updates.
        """
        self.hours += 1

        for person in self.people:
            person.update()

        self.update_infections_slow()
        
    def draw(self):
        """The simulated world is drawn in the following order:
        - Current screen is cleared.
        - All the people in the simulated population is drawn.
        - The rectangle that represents the world boundaries is drawn.
        - Number of hours and number of people infected are written above the
          simulated world frame.
        """
        turtle.clear()

        for person in self.people:
            person.draw()
            
        turtle.goto(-self.size[0]/2, self.size[1]/2)
        turtle.setheading(0)
        turtle.pendown()
        is_width = True
        for step in range(4):
            if is_width:
                turtle.right(90)
                turtle.forward(self.size[0])
                is_width = not is_width
            else:
                turtle.right(90)
                turtle.forward(self.size[1])
                is_width = not is_width
        turtle.penup()

        turtle.write("Hours: {}".format(self.hours), move = False,
                     align = 'left')
       
        turtle.goto(0, 250)
        self.infected = self.count_infected()
        turtle.write("Infected: {}".format(self.infected), move = False,
                     align = 'center')
        turtle.home()
               
    def count_infected(self):
        """The number of people that are infected are counted.
        """
        infected_people = 0
        for person in self.people:
            if person.colour != "black":
                infected_people += 1
        return infected_people
    
#---------------------------------------------------------
#Should not need to alter any of the code below this line
#---------------------------------------------------------
class GraphicalWorld:
    """Handles the user interface for the simulation

    space - starts and stops the simulation
    'z' - resets the application to the initial state
    'x' - infects a random person
    'c' - cures all the people
    """
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.TITLE = 'COMPSCI 130 Project One'
        self.MARGIN = 50 #gap around each side
        self.PEOPLE = 200 #number of people in the simulation
        self.framework = AnimationFramework(self.WIDTH, self.HEIGHT, self.TITLE)
        
        self.framework.add_key_action(self.setup, 'z') 
        self.framework.add_key_action(self.infect, 'x')
        self.framework.add_key_action(self.cure, 'c')
        self.framework.add_key_action(self.toggle_simulation, ' ') 
        self.framework.add_tick_action(self.next_turn)
        
        self.world = None

    def setup(self):
        """ Reset the simulation to the initial state """
        print('resetting the world')        
        self.framework.stop_simulation()
        self.world = World(self.WIDTH - self.MARGIN * 2, self.HEIGHT - self.MARGIN * 2, self.PEOPLE)
        self.world.draw()
        
    def infect(self):
        """ Infect a person, and update the drawing """
        print('infecting a person')
        self.world.infect_person()
        self.world.draw()

    def cure(self):
        """ Remove infections from all the people """
        print('cured all people')
        self.world.cure_all()
        self.world.draw()

    def toggle_simulation(self):
        """ Starts and stops the simulation """
        if self.framework.simulation_is_running():
            self.framework.stop_simulation()
        else:
            self.framework.start_simulation()           

    def next_turn(self):
        """ Perform the tasks needed for the next animation cycle """
        self.world.simulate()
        self.world.draw()
        
## This is the animation framework
## Do not edit this framework
class AnimationFramework:
    """This framework is used to provide support for animation of
       interactive applications using the turtle library.  There is
       no need to edit any of the code in this framework.
    """
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
        self.tick = None #function to call for each animation cycle
        self.delay = 1 #smallest delay is 1 millisecond      
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.hideturtle() #prevent turtle appearance
        turtle.tracer(0, 0) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything
        turtle.setundobuffer(None)
        self.__animation_loop()

    def start_simulation(self):
        self.simulation_running = True
        
    def stop_simulation(self):
        self.simulation_running = False

    def simulation_is_running(self):
        return self.simulation_running
    
    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func):
        self.tick = func

    def __animation_loop(self):
        try:
            if self.simulation_running:
                self.tick()
            turtle.ontimer(self.__animation_loop, self.delay)
        except turtle.Terminator:
            pass


gw = GraphicalWorld()
gw.setup()
turtle.mainloop() #Need this at the end to ensure events handled properly
