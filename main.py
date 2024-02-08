import pygame, random, sys

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Square, self).__init__()
        self.xpos = x * 100
        print(self.xpos)
        self.ypos = y * 100
        print(self.ypos)
        self.image = pygame.Surface((100,100),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.color = (28, 156, 62)
        pygame.draw.rect(self.image, self.color, (2, 2, 100, 100), border_radius = 0)
        self.rect = self.image.get_rect(center = (self.xpos + 50, self.ypos + 50))





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

player = 0
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

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()