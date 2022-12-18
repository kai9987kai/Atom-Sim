import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption('Atom Simulation')

# Set the background color
bg_color = (255, 255, 255)

# Set the radius of the atom
atom_radius = 50

# Set the speed of the electrons
electron_speed = 5

# Create a list to store the electrons
electrons = []

# Set the running flag to True
running = True

# Set the current element to None
current_element = None

# Define a function to create the electrons for a given element
def create_electrons(element):
    # Clear the list of electrons
    electrons.clear()

    # Get the number of electrons and the colors for the given element
    if element == 'Hydrogen':
        num_electrons = 1
        electron_colors = [(0, 0, 255)]
    elif element == 'Helium':
        num_electrons = 2
        electron_colors = [(0, 0, 255), (255, 0, 0)]
    elif element == 'Lithium':
        num_electrons = 3
        electron_colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]
    elif element == 'Beryllium':
        num_electrons = 4
        electron_colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]
    else:
        num_electrons = 10
        electron_colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]

    # Create the electrons
    for i in range(num_electrons):
        # Choose a random color for the electron
        color = random.choice(electron_colors)

        # Choose a random starting position for the electron
        x = random.randint(atom_radius, window_size[0] - atom_radius)
        y = random.randint(atom_radius, window_size[1] - atom_radius)

        # Choose a random starting velocity for the electron
        vx = random.uniform(-electron_speed, electron_speed)
        vy = random.uniform(-electron_speed, electron_speed)

        # Create the electron and add it to the list
        electron = [x, y, vx, vy, color]
        electrons.append(electron)

# Set the current element to Hydrogen
current_element = 'Hydrogen'
create_electrons(current_element)

# Run the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if the user pressed a key to change the
             if event.key == pygame.K_1:
               
              current_element = 'Hydrogen'
              
        elif event.key == pygame.K_2:
              current_element = 'Helium'
        elif event.key == pygame.K_3:
              current_element = 'Lithium'
        elif event.key == pygame.K_4:
              current_element = 'Beryllium'
        else:
              current_element = 'Default'

            # Create the electrons for the new element
            
        create_electrons(current_element)

    # Update the positions of the electrons
    for electron in electrons:
        # Update the position of the electron
        electron[0] += electron[2]
        electron[1] += electron[3]

        # Check if the electron has reached the edge of the screen
        if electron[0] < atom_radius or electron[0] > window_size[0] - atom_radius:
            electron[2] = -electron[2]
        if electron[1] < atom_radius or electron[1] > window_size[1] - atom_radius:
            electron[3] = -electron[3]

    # Clear the screen
    screen.fill(bg_color)

    # Draw the electrons
    for electron in electrons:
        pygame.draw.circle(screen, electron[4], (int(electron[0]), int(electron[1])), 5)

    # Draw the atom
    pygame.draw.circle(screen, (0, 0, 0), (400, 300), atom_radius, 2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
