import pygame, sys, pygame_textinput, math
pygame.init()

#Screen Variables
x = 600
y = 400
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()

#Colors
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
GRAY = (160,160,160)

#Text
def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

def text(txt,size,posx,posy):
    text_font = pygame.font.SysFont('arial',size)
    text_surf, text_rect = text_objects(txt,text_font)
    text_rect.center = (posx,posy)
    screen.blit(text_surf,text_rect)

#Buttons
def but(txt,x,y,w,h,co1,co2,fun=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, co2, (x,y,w,h))
        if click[0] == 1 and fun != None:
            fun()
    else:
        pygame.draw.rect(screen, co1, (x,y,w,h))
    font = pygame.font.SysFont('arial',15)
    text_surf, text_rect = text_objects(txt,font)
    text_rect.center = ((x+(w/2)),(y+(h/2)))
    screen.blit(text_surf,text_rect)

def mass_check(mass_stats,i,text_list,text):
    if mass_stats[i] < 0:
        del text_list[i]
        del mass_stats[i]
        text.clear_text()
        return True

#Mass Class
class Mass():
    def __init__(self,m,v,x,y,r,col,fin_v):
        self.m = m
        self.v = v
        self.x = x
        self.y = y
        self.r = r
        self.col = col
        self.fin_v = fin_v
    def draw_mass(self):
        pygame.draw.circle(screen,self.col,(self.x,self.y),self.r)
    def set_mass(self, mass):
        self.m = mass
    def set_vel(self, velocity):
        self.v = velocity
    def get_fin_v(self):
        return self.fin_v
    def set_fin_v(self, final):
        self.fin_v = final
    def can_move(self):
        if self.m != None and self.v != None:
            return True
    def move(self):
        if self.v > 0:
            self.x += math.ceil(self.v)
        elif self.v < 0:
            self.x += math.floor(self.v)
        self.draw_mass()
    def front_collide_check(self, other):
        if (self.x + self.r) >= (other.x - other.r):
            return True
    def back_collide_check(self, other):
        if (self.x - self.r) <= (other.x + other.r) and (self.x+self.r) >= other.x:
            return True
    def can_collide(self,other):
        if self.v < 0 and other.v > 0 or self.v < other.v:
            return False
        else:
            return True
    def final_calc(self, other):
        self.fin_v = ((((self.m - other.m)/(self.m + other.m))*(self.v))
        + (((2*other.m)/(self.m + other.m))*(other.v)))
    def in_final_calc(self, other):
        self.fin_v = (((self.m)/(self.m + other.m))*self.v)
    def impulse_calc(self, other):
        self.fin_v = (other.f*other.t)/(self.m)
    def set_dir(self):
        if self.v < 0:
            self.x = 400

#Force Class
class Force():
    def __init__(self,f,t):
        self.f = f
        self.t = t
        self.x = 60
        self.x_two = 200
        self.y = 35
    def draw_force(self):
        if self.f > 0:
            pygame.draw.polygon(screen, BLACK, ((20+self.x, 75+self.y), (20+self.x, 100+self.y),
                                            (70+self.x, 100+self.y), (70+self.x, 125+self.y),
                                            (95+self.x, 88+self.y), (70+self.x, 50+self.y), (70+self.x, 75+self.y)))
        elif self.f < 0:
            pygame.draw.polygon(screen, BLACK, ((275+self.x_two, 75+self.y), (275+self.x_two, 100+self.y),
                                                (200+self.x_two, 100+self.y), (200+self.x_two, 125+self.y),
                                                (175+self.x_two, 88+self.y), (200+self.x_two, 50+self.y), (200+self.x_two, 75+self.y)))

    def set_force(self,force):
        self.f = force
    def set_time(self,time):
        self.t = time
        

#Title Page
def intro():
    intro = True
    while intro:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                
        screen.fill(WHITE)
        text("Collision Simulator",60,x//2,y//5)

        but("1D Elastic", x//12, y//2, 75, 50, GRAY, GREEN, elastic)
        but("1D Inelastic", 5*x//12, y//2, 75, 50, GRAY, GREEN, inelastic)
        but("1D Impulse", 9*x//12, y//2, 75, 50, GRAY, GREEN, impulse)

        pygame.display.update()
        clock.tick(30)

#1D Elastic
def elastic():
    elastic_flag = True
    mass1 = Mass(None,None,200,125,15,GREEN,0)
    mass2 = Mass(None,None,400,125,15,BLUE,0)
    county = 200
    countx = 150
    count = 0
    mass_stats = []
    text_list = ["","","",""]
    elastic_input = pygame_textinput.TextInput()
    while elastic_flag:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        screen.fill(WHITE)
        but("Return to Title", 50, 350, 100, 50, GRAY, GREEN, intro)
        but("Reset", 500, 350, 75, 50, GRAY, GREEN, elastic)

        if (mass1.can_move() and mass2.can_move()):
            mass1.move()
            mass2.move()
        else:
            mass1.draw_mass()
            mass2.draw_mass()
        
        text("1D Elastic Collision",30,x//2,y//12)
        text("Green Mass",14,150,175)
        text("Blue Mass",14,450,175)
        text("Initial Masses (kg)",15,x//2,200)
        text("Initial Velocities (m/s)",15,x//2,250)
        text("Final Velocities (m/s)",15,x//2,300)

        if (elastic_input.update(events)):
            try:
                mass_stats.append(float(elastic_input.get_text()))
                text_list.insert(count,str(elastic_input.get_text()))
                count += 1
            except ValueError:
                elastic_input.clear_text()
                count += 1
                count -= 1
            if count == 1:
                if mass_check(mass_stats,0,text_list,elastic_input):
                    count -= 1
                else:
                    county = 250
                    elastic_input.clear_text()
            if count == 2:
                elastic_input.clear_text()
                countx = 450
                county = 200
            if count == 3:
                if mass_check(mass_stats,2,text_list,elastic_input):
                    count -= 1
                else:
                    county = 250
                    elastic_input.clear_text()
            if count == 4:
                county = 700
                mass1.set_mass(mass_stats[0])
                mass1.set_vel(mass_stats[1])
                mass2.set_mass(mass_stats[2])
                mass2.set_vel(mass_stats[3])
                if mass1.can_collide(mass2):
                    mass1.final_calc(mass2)
                    mass2.final_calc(mass1)
                else:
                    mass1.set_fin_v(mass1.v)
                    mass2.set_fin_v(mass2.v)

        text(text_list[0],30,150,200)
        text(text_list[1],30,150,250)
        text(text_list[2],30,450,200)
        text(text_list[3],30,450,250)
        text(str(round(mass1.get_fin_v(),3)),30,150,300)
        text(str(round(mass2.get_fin_v(),3)),30,450,300)
        
        screen.blit(elastic_input.get_surface(), (countx,county))

        if mass1.front_collide_check(mass2):
            mass1.set_vel(mass1.get_fin_v())
            mass2.set_vel(mass2.get_fin_v())
        
        pygame.display.update()
        clock.tick(60)


#1D Inelastic
def inelastic():
    inelastic_flag = True
    mass1 = Mass(None,0,150,125,15,GREEN,0)
    mass2 = Mass(None,0,300,125,15,BLUE,0)
    county = 200
    countx = 150
    count = 0
    mass_stats = []
    text_list = ["","","",""]
    inelastic_input = pygame_textinput.TextInput()
    while inelastic_flag:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        screen.fill(WHITE)
        but("Return to Title", 50, 350, 100, 50, GRAY, GREEN, intro)
        but("Reset", 500, 350, 75, 50, GRAY, GREEN, inelastic)

        if (mass1.can_move() and mass2.can_move()):
            mass1.move()
            mass2.move()
        else:
            mass1.draw_mass()
            mass2.draw_mass()
        
        text("1D Inelastic Collision",30,x//2,y//12)
        text("Green Mass",14,150,175)
        text("Blue Mass",14,450,175)
        text("Initial Masses (kg)",15,x//2,200)
        text("Initial Velocity (m/s)",15,x//2,250)
        text("Final Velocity (m/s):",15,150,300)

        if (inelastic_input.update(events)):
            try:
                mass_stats.append(float(inelastic_input.get_text()))
                text_list.insert(count,str(inelastic_input.get_text()))
                count += 1
            except ValueError:
                inelastic_input.clear_text()
                count += 1
                count -= 1
            if count == 1:
                if mass_check(mass_stats,0,text_list,inelastic_input):
                    count -= 1
                else:
                    county = 250
                    inelastic_input.clear_text()
            if count == 2:
                countx = 450
                county = 200
                inelastic_input.clear_text()
            if count == 3:
                if mass_check(mass_stats,2,text_list,inelastic_input):
                    count -= 1
                else:
                    county = 600
                    mass1.set_mass(mass_stats[0])
                    mass1.set_vel(mass_stats[1])
                    mass1.set_dir()
                    mass2.set_mass(mass_stats[2])
                    mass1.in_final_calc(mass2)
                    inelastic_input.clear_text()
        
        text(text_list[0],30,150,200)
        text(text_list[1],30,150,250)
        text(text_list[2],30,450,200)
        if count == 3:
            text(str(round(mass1.get_fin_v(),3)),30,300,300)
        
        screen.blit(inelastic_input.get_surface(), (countx,county))

        if mass1.v < 0:
            if mass1.back_collide_check(mass2):
                mass1.set_vel(mass1.get_fin_v())
                mass2.set_vel(mass1.get_fin_v())

        if mass1.v > 0:
            if mass1.front_collide_check(mass2):
                mass1.set_vel(mass1.get_fin_v())
                mass2.set_vel(mass1.get_fin_v())
        
        pygame.display.update()
        clock.tick(60)

#1D Impulsive Force
def impulse():
    impulse_flag = True
    force = Force(None,None)
    mass2 = Mass(None,0,300,125,15,BLUE,0)
    county = 200
    countx = 150
    count = 0
    mass_stats = []
    text_list = ["","","",""]
    impulse_input = pygame_textinput.TextInput()
    while impulse_flag:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        screen.fill(WHITE)
        but("Return to Title", 50, 350, 100, 50, GRAY, GREEN, intro)
        but("Reset", 500, 350, 75, 50, GRAY, GREEN, impulse)

        if (mass2.can_move()):
            mass2.move()
            force.draw_force()
        else:
            mass2.draw_mass()
        
        text("1D Impulsive Force",30,x//2,y//12)
        text("Force Inputs",14,150,175)
        text("Mass Input",14,450,175)
        text("Initial Force (N)",15,x//2,200)
        text("Time of Impulse (s)",15,x//2,250)
        text("Initial Mass (kg)",15,x//2,300)
        text("Final Velocity (m/s)",15,x//2,350)

        if (impulse_input.update(events)):
            try:
                mass_stats.append(float(impulse_input.get_text()))
                text_list.insert(count,str(impulse_input.get_text()))
                count += 1
            except ValueError:
                impulse_input.clear_text()
                count += 1
                count -= 1
            if count == 1:
                county = 250
                impulse_input.clear_text()
            if count == 2:
                if mass_check(mass_stats,1,text_list,impulse_input):
                    count -= 1
                else:
                    countx = 450
                    county = 300
                    impulse_input.clear_text()
            if count == 3:
                if mass_check(mass_stats,2,text_list,impulse_input):
                    count -= 1
                else:
                    county = 600
                    impulse_input.clear_text()
                    mass2.set_mass(mass_stats[2])
                    force.set_force(mass_stats[0])
                    force.set_time(mass_stats[1])
                    mass2.impulse_calc(force)
                    mass2.set_vel(mass2.get_fin_v())

        text(text_list[0],30,150,200)
        text(text_list[1],30,150,250)
        text(text_list[2],30,450,300)
        text(str(round(mass2.get_fin_v(),3)),30,400,350)
        
        screen.blit(impulse_input.get_surface(), (countx,county))

        
        pygame.display.update()
        clock.tick(60)
intro()
