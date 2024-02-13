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


    def clicked(self):
        self.color = (46, 184, 82)
        pygame.draw.rect(self.image, self.color, (0, 0, 100, 100))

    def not_clicked(self):
        self.color = (28, 156, 62)
        pygame.draw.rect(self.image, self.color, (0, 0, 100, 100))

    def nearby(self):
        if self.occupied == False:
            pygame.draw.rect(self.image, (15, 189, 142), (0,0,100,100))


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
    red.add(Unit("Blue",i,5,"blue"))

blue.add(Unit("Blue", 3, 3, "blue"))

units = pygame.sprite.Group()
units.add(red)
units.add(blue)

objects.add(units)

player = 0
mouse_state = 0
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
        for unit in units:
            if pygame.sprite.collide_rect(unit,square):
                square.occupied = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        for square in grid:
            if square.rect.collidepoint(mouse_pos):
                square.clicked()
                if square.occupied:
                    mouse_state = 1
                    for nearsquare in grid:
                        if (nearsquare.pos[0] >= square.pos[0] - 1 and nearsquare.pos[0] <= square.pos[0] + 1) and (nearsquare.pos[1] >= square.pos[1] - 1 and nearsquare.pos[1] <= square.pos[1] + 1):
                            nearsquare.nearby()
            else:
                square.not_clicked()

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()