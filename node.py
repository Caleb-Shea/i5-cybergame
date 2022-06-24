import pygame as pyg
import random
import math

from assets import *
from helper_func import *


class Node(pyg.sprite.Sprite):
    """
    Description: A class to represent a single node. The node has a parent,
                 children, and attributes used for purchasing, inspecting, and
                 learning about this node.
    Parameters:
        data [dict] -> All the data necessary for the creation and use of the
                       node.
    Returns: Node()
    """
    def __init__(self, data):
        super().__init__()

        self.window = pyg.display.get_surface()
        self.WIDTH, self.HEIGHT = self.window.get_rect().size

        self.data = data
        self.parent = self.data['parent']

        # The size of the node is dependant on which generation it is
        # Will probably be deprecated once images are made
        self.radius = 50 + (3 - (self.data['generation'] * 5))

        self.image_src = pyg.Surface((self.radius * 3, self.radius * 3)).convert_alpha()
        self.image_src.fill(colors['clear'])

        self.rect = self.image_src.get_rect()
        pyg.draw.circle(self.image_src, colors[self.data['color']], (self.rect.centerx, self.rect.centery), self.radius)

        # Make a separate image for rendering so we don't lose fidelity
        self.image = self.image_src.copy()
        self.draw_rect = self.image_src.get_rect()

        # Create the menu that pops up once clicked
        self.menu = pyg.Surface((self.WIDTH, self.HEIGHT)).convert_alpha()
        self.menu.fill(colors['clear'])
        name_img = fonts['zrnic36'].render(self.data['name'], True, colors['white'])
        name_rect = name_img.get_rect()
        name_rect.center = (self.WIDTH//2, 30)
        self.menu.blit(name_img, name_rect)
        desc_img = fonts['zrnic24'].render(self.data['desc'], True, colors['white'])
        desc_rect = desc_img.get_rect()
        desc_rect.center = (self.WIDTH//2, 70)
        self.menu.blit(desc_img, desc_rect)

        # All booleans required for the node to function
        self.is_selected = False
        self.is_hovered = False

        # The surface and rect for the name of this node
        if len(self.data['name']) < 7:
            self.name_img = fonts['zrnic24'].render(self.data['name'], True, colors['darkgray'])
        elif len(self.data['name']) < 10:
            self.name_img = fonts['zrnic16'].render(self.data['name'], True, colors['darkgray'])
        else:
            self.name_img = fonts['zrnic14'].render(self.data['name'], True, colors['darkgray'])

        self.name_rect = self.name_img.get_rect()

    def phase_two_init(self, nodes):
        """
        Description: Initalize parts of the node that cannot be initalized
                     without more information, specifially the complete list
                     of nodes.
        Parameters:
            nodes [pyg.sprite.Group] -> The complete lists of nodes.
        Returns: None
        """
        self.nodes = nodes

        # Find the parent of this node
        for node in nodes:
            if self.parent == node.data['name']:
                self.parent = node

        self.get_children()
        self.get_siblings()

        # Initalize position and rotation
        if self.parent == None:
            # If center node, center on the screen
            self.rect.center = (self.WIDTH//2, self.HEIGHT//2)
            # The center has a theta so it's children don't overlap
            self.theta = random.random() * (4 * math.pi)
        else:
            # Otherwise, center on parent
            self.theta = self.parent.theta

            if self.data['generation'] > 1:
                # Use the number of siblings to space said siblings apart
                num_sibs = len(self.siblings) + 1
                self.theta += (2 * math.pi) / num_sibs * int(self.data['index'])
                self.theta += math.pi # Additional rotation to face the non-central nodes away from the center
            else:
                # This only runs for 1st gen nodes
                num_sibs = len(self.siblings)
                self.theta += (2 * math.pi) / num_sibs * int(self.data['index'])

            # Set distances between parent and this node based on generation
            self.dist = self.data['dist']
            self.rect.center = (self.parent.rect.centerx + self.dist * math.cos(self.theta),
                                self.parent.rect.centery + self.dist * math.sin(self.theta))

        # Get the spritesheet for earth
        if self.data['name'] == 'EARTH':
            self.ss = images['earth_ss']
            self.ss_cur = 0
            self.ss_rects = []
            for j in range(4):
                for i in range(12):
                    x = i * 100
                    y = j * 100
                    self.ss_rects.append(pyg.rect.Rect(x, y, 100, 100))

    def get_children(self):
        """
        Description: Create a list of this node's children.
        Parameters: None
        Returns: None
        """
        self.children = []
        for child in self.data['children']:
            for node in self.nodes:
                if node.data['name'] == child:
                    self.children.append(node)

    def get_siblings(self):
        """
        Description: Create a list of this node's siblings.
        Parameters: None
        Returns: None
        """
        self.siblings = []
        if self.parent != None:
            for potential in self.parent.children:
                if potential.data['generation'] == self.data['generation']:
                    self.siblings.append(potential)

    def draw_connections(self):
        """
        Description: Either draw lines between this node and it's children or
                     draw orbits.
        Parameters: None
        Returns: None
        """
        for child in self.children:
            if child.dist < 300:
                # Draw straight lines
                pyg.draw.aaline(self.window, colors['gray'],
                              self.rect.center, child.rect.center) # Use arcs later
            else:
                # Draw an orbit
                pyg.draw.circle(self.window, colors['gray'], self.rect.center,
                                child.data['dist'], 1) # Use ellipses later?

    def update(self):
        """
        Description: Spin this node around the central node.
                     Set is_hovered booleans.
                     Position text.
        Parameters: None
        Returns: None
        """
        # Slowly spin this node around the center
        if self.parent != None:
            self.theta += 0.001

            # If this node is really far away (i.e. it has an orbit), go faster
            if self.data['dist'] >= 300:
                self.theta += 0.0004

            self.rect.center = (self.parent.rect.centerx + self.dist * math.cos(self.theta),
                                self.parent.rect.centery + self.dist * math.sin(self.theta))

        # If the mouse is hovering over this node, make it bigger
        if self.is_hovered or self.is_selected:
            if self.data['name'] != 'EARTH':
                self.draw_rect = self.rect.inflate(math.ceil(self.radius * .2), math.ceil(self.radius * .2))
                self.image = pyg.transform.smoothscale(self.image_src, self.draw_rect.size)
            else:
                self.draw_rect = self.rect
        else:
            self.draw_rect = self.rect.copy()
            self.image = pyg.transform.smoothscale(self.image_src, self.draw_rect.size)

        # Center the name
        self.name_rect.center = self.rect.center

        # Update the image for earth
        if self.data['name'] == 'EARTH':
            self.image.fill(colors['clear'])
            self.image.blit(self.ss, (30, 30), self.ss_rects[math.floor(self.ss_cur)%len(self.ss_rects)])
            self.ss_cur += 1/3

    def render_menu(self):
        """
        Description: Render this node's menu on the screen.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.menu, (0, 0))

    def render(self):
        """
        Description: Render this node on the screen.
        Parameters: None
        Returns: None
        """
        self.draw_connections()
        self.window.blit(self.image, self.draw_rect)
        self.window.blit(self.name_img, self.name_rect)
