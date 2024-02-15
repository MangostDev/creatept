import pygame, random, sys

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Square, self).__init__()
        self.pos = (x,y)
        self.xpos = x * 100
        self.ypos = y * 100
        self.image = pygame.Surface((100,100),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.color = (28, 156, 62)
        pygame.draw.rect(self.image, self.color, (0, 0, 100, 100))
        self.rect = self.image.get_rect(center = (self.xpos + 50, self.ypos + 50))
        self.occupied = False
        self.near = False


    def clicked(self):
        self.color = (46, 184, 82)
        pygame.draw.rect(self.image, self.color, (0, 0, 100, 100))

    def not_clicked(self):
        self.color = (28, 156, 62)
        pygame.draw.rect(self.image, self.color, (0, 0, 100, 100))

    def nearby(self):
            self.near = True

    def not_nearby(self):
        self.near = False




class Unit(pygame.sprite.Sprite):
    def __init__(self,color,x,y,team):
        super(Unit, self).__init__()
        self.pos = (x,y)
        self.team = team
        self.xpos = (x * 100) + 50
        self.ypos = (y * 100) + 50
        self.image = pygame.Surface((25,25),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.color = color
        pygame.draw.rect(self.image, self.color, (2, 2, 100, 100))
        self.rect = self.image.get_rect(center = (self.xpos,self.ypos))
        self.selected = False
        self.ready = True
        self.turn = False

    def move(self, newx, newy):
        self.pos = (newx, newy)
        self.xpos = (self.pos[0] * 100) + 50
        self.ypos = (self.pos[1] * 100) + 50
        self.rect.centerx = self.xpos
        self.rect.centery = self.ypos

    def show_ready(self):
        if self.ready:
            pygame.draw.rect(self.image, self.color, (2, 2, 100, 100))
        else:
            if self.team == "red":
                pygame.draw.rect(self.image, (200, 150, 150), (2,2,100,100))
            else:
                pygame.draw.rect(self.image, (150,150,200), (2, 2, 100, 100))



def combat(r, b):
    red_support = 0
    blue_support = 0
    for unit in red:
        if abs(unit.pos[0] - r.pos[0]) == 1 and abs(unit.pos[1] - r.pos[1]) == 1:
            red_support += 1
    for unit in blue:
        if abs(unit.pos[0] - b.pos[0]) == 1 and abs(unit.pos[1] - b.pos[1]) == 1:
            blue_support += 1

    result = random.randint(1,10)
    print(result)
    result += blue_support
    result -= red_support
    print(result)
    if result > 8:
        r.kill()
    elif result < 3:
        b.kill()

def check_ready_units(group):
    ready = 0
    for unit in group:
        if unit.ready:
            ready += 1

    if ready > 0:
        return True
    else:
        return False








'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''


# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Create PT")

# Create clock to later control frame rate
clock = pygame.time.Clock()


grid = pygame.sprite.Group()
for y in range(6):
    for x in range(6):
        grid.add(Square(x,y))

objects = pygame.sprite.Group()
objects.add(grid)
print(objects)

grid.add(Square(3, 5))
objects.add(grid)

red = pygame.sprite.Group()
for i in range(6):
    red.add(Unit("Red",i,0,"red"))

blue = pygame.sprite.Group()
for i in range(6):
    blue.add(Unit("Blue",i,5,"blue"))


units = pygame.sprite.Group()
units.add(red)
units.add(blue)

objects.add(units)

player = 0
mouse_state = 0
selected_unit = None
activations = len(units.sprites())
# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    

    # Fill the screen with a color (e.g., white)
    screen.fill("Black")

    objects.draw(screen)
    
    for square in grid:
        if pygame.sprite.spritecollide(square,units,0):
            square.occupied = True
        else:
            square.occupied = False

    if not check_ready_units(red):
        player = 0
    if not check_ready_units(blue):
        player = 1

    for unit in units:
        unit.show_ready()

    if player == 0:
        for unit in units:
            if unit.team == "blue":
                unit.turn = True
            else:
                unit.turn = False
    elif player == 1:
        for unit in units:
            if unit.team == "red":
                unit.turn = True
            else:
                unit.turn = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        for square in grid:
            if square.rect.collidepoint(mouse_pos):
                if mouse_state == 0:
                    square.clicked()
                    if square.occupied:
                        for unit in units:
                            if unit.pos == square.pos and unit.ready and unit.turn:
                                unit.selected = True
                                mouse_state = 1
                                selected_unit = unit
                        for nearsquare in grid:
                            if (nearsquare.pos[0] >= square.pos[0] - 1 and nearsquare.pos[0] <= square.pos[0] + 1) and (nearsquare.pos[1] >= square.pos[1] - 1 and nearsquare.pos[1] <= square.pos[1] + 1):
                                nearsquare.nearby()
                            else:
                                nearsquare.not_nearby()
                    continue
                elif mouse_state == 1:
                    if square.near and not square.occupied:
                        selected_unit.move(square.pos[0],square.pos[1])
                        for square in grid:
                            square.not_nearby()
                        mouse_state = 0
                        selected_unit.ready = False
                        selected_unit.selected = False
                        activations -= 1
                        selected_unit = None
                        if player == 0:
                            player = 1
                        elif player == 1:
                            player = 0
                    if square.occupied:
                        mouse_state = 1
                        for unit in units:
                            if unit.pos == square.pos and unit.ready and unit.turn:
                                unit.selected = True
                                selected_unit = unit
                        for nearsquare in grid:
                            if (nearsquare.pos[0] >= square.pos[0] - 1 and nearsquare.pos[0] <= square.pos[0] + 1) and (nearsquare.pos[1] >= square.pos[1] - 1 and nearsquare.pos[1] <= square.pos[1] + 1):
                                nearsquare.nearby()
                    continue


            else:
                square.not_clicked()

    if activations == 0:
        for b in blue:
            for r in red:
                if abs(r.pos[0] - b.pos[0]) == 1 and abs(r.pos[1] - b.pos[1]) == 1:
                    combat(r, b)
        for unit in units:
            unit.ready = True
        activations = len(units.sprites())



    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()