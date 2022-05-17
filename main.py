"""
An upgrade tree simulation.

By: Caleb Shea
"""

import pygame as pyg
import random
import math
import os

from colors import colors
from node_data import *


class Node(pyg.sprite.Sprite):
    """
    Description: A class to represent a single node. The node has a parent,
                 children, and attributes used for purchasing, inspecting, and
                 learning about this node.
    Parameters:
        window [pyg.Surface] -> A reference to the screen.
        data [dict] -> All the data necessary for the creation and use of the
                       node.
    Returns: None
    """
    def __init__(self, window, data):
        super().__init__()

        self.window = window

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
        self.draw_image = self.image_src.copy()
        self.draw_rect = self.image_src.get_rect()

        # Create the menu that pops up once clicked
        self.menu = pyg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.menu.fill(colors['clear'])
        name_img = fonts['zrnic36'].render(self.data['name'], True, colors['white'])
        name_rect = name_img.get_rect()
        name_rect.center = (WIDTH//3, 30)
        self.menu.blit(name_img, name_rect)
        desc_img = fonts['zrnic24'].render(self.data['desc'], True, colors['white'])
        desc_rect = desc_img.get_rect()
        desc_rect.center = (WIDTH//3, 70)
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
            self.rect.center = (WIDTH//2, HEIGHT//2)
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
                pyg.draw.aaline(window, colors['gray'],
                              self.rect.center, child.rect.center) # Use arcs later
            else:
                # Draw an orbit
                pyg.draw.circle(window, colors['gray'], self.rect.center,
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
        m_pos = pyg.mouse.get_pos()
        if math.dist(m_pos, self.rect.center) <= self.radius or self.is_selected:
            self.is_hovered = True
            self.draw_rect = self.rect.inflate(math.ceil(self.radius * .2), math.ceil(self.radius * .2))
            self.draw_image = pyg.transform.smoothscale(self.image_src, self.draw_rect.size)

        else:
            self.is_hovered = False
            self.draw_rect = self.rect.copy()
            self.draw_image = pyg.transform.smoothscale(self.image_src, self.draw_rect.size)

        # Center the name
        self.name_rect.center = self.rect.center

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
        self.window.blit(self.draw_image, self.draw_rect)
        self.window.blit(self.name_img, self.name_rect)


class FullMenu():
    def __init__(self, window):
        """
        Description: A class to represent a single node. The node has a parent,
                     children, and attributes used for purchasing, inspecting, and
                     learning about this node.
        Parameters:
            window [pyg.Surface] -> A reference to the screen.
        Returns: None
        """
        self.window = window

        self.rect = self.window.get_rect().inflate(-20, -20)
        self.image = pyg.Surface(self.rect.size)
        self.image.fill(colors['darkgray'])


        self.tab_names = ['ACQUISITIONS', 'OPS', 'PERSONNEL', 'INTEL', 'CYBER']
        self.tabs = []
        for i, tab in enumerate(self.tab_names):
            size = self.rect.width//len(self.tab_names)
            rect = pyg.rect.Rect(i * size, 0, size, 50)
            self.tabs.append(rect)

        self.cur_tab = self.tab_names[1]

    def update(self):
        """
        Description: Detect mouse clicks and update active tab.
        Parameters: None
        Returns: None
        """
        m_pos = pyg.mouse.get_pos()
        m_pressed = pyg.mouse.get_pressed()
        for rect, name in zip(self.tabs, self.tab_names):
            # If a tab is clicked on, select it
            # We move the rect because the mouse coords are absolute, but the
            # rect coords are based on the topleft of the menu
            if rect.move(10, 10).collidepoint(m_pos) and m_pressed[0]:
                self.cur_tab = name

    def render_tabs(self):
        """
        Description: Draw the tabs at the top of the screen.
        Parameters: None
        Returns: None
        """
        for rect, name in zip(self.tabs, self.tab_names):
            if self.cur_tab == name:
                pyg.draw.rect(self.image, colors['darkgray'], rect)
            else:
                pyg.draw.rect(self.image, colors['gray'], rect)

            text = fonts['zrnic24'].render(name, True, colors['white'])
            text_rect = text.get_rect(center=rect.center)
            self.image.blit(text, text_rect)

        # Draw lines separating each tab
        size = self.rect.width//len(self.tab_names)
        pyg.draw.line(self.image, colors['black'], (0, 50), (self.rect.right, 50))
        for i in range(1, 5):
            pyg.draw.line(self.image, colors['darkgray'], (i*size, 0), (i*size, 50))

    def render(self):
        """
        Description: Render this menu on the screen.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.image, self.rect)
        self.render_tabs()

def terminate():
    """
    Description: Cleanly exit the program.
    Parameters: None
    Returns: None
    """
    pyg.quit()
    raise SystemExit()

def get_path(path):
    """
    Description: Get the full path from a partial file path.
    Parameters:
        path [path-like-object] -> The partial path to get the full path from
    Returns:
        [path-like-object] -> The full path
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)

def play_sound(sound):
    """
    Description: Play a sound out of any available channel.
    Parameters:
        sound [sound file] -> The sound to play
    Returns: None
    """
    se_channel = pyg.mixer.find_channel()
    se_channel.play(sound)

def init_nodes():
    """
    Description: Create a dictionary that contains all the nodes the program
                 needs.
    Parameters: None
    Returns:
        node_dict [dict] -> The dict with all the nodes
    """
    # Create all nodes from node_data.py
    earth_nodes = pyg.sprite.Group()
    for data in main_data:
        node = Node(window, data)
        earth_nodes.add(node)

    gssap_nodes = pyg.sprite.Group()
    for data in gssap_data:
        node = Node(window, data)
        gssap_nodes.add(node)

    iss_nodes = pyg.sprite.Group()
    for data in iss_data:
        node = Node(window, data)
        iss_nodes.add(node)

    milstar_nodes = pyg.sprite.Group()
    for data in milstar_data:
        node = Node(window, data)
        milstar_nodes.add(node)

    aehf_nodes = pyg.sprite.Group()
    for data in aehf_data:
        node = Node(window, data)
        aehf_nodes.add(node)

    gps_nodes = pyg.sprite.Group()
    for data in gps_data:
        node = Node(window, data)
        gps_nodes.add(node)

    sbirs_nodes = pyg.sprite.Group()
    for data in sbirs_data:
        node = Node(window, data)
        sbirs_nodes.add(node)

    # Once all nodes have been made, init phase two
    for node in earth_nodes:
        node.phase_two_init(earth_nodes)
    for node in gssap_nodes:
        node.phase_two_init(gssap_nodes)
    for node in iss_nodes:
        node.phase_two_init(iss_nodes)
    for node in milstar_nodes:
        node.phase_two_init(milstar_nodes)
    for node in aehf_nodes:
        node.phase_two_init(aehf_nodes)
    for node in gps_nodes:
        node.phase_two_init(gps_nodes)
    for node in sbirs_nodes:
        node.phase_two_init(sbirs_nodes)


    node_dict = {'EARTH': earth_nodes,
                 'GSSAP': gssap_nodes,
                 'ISS': iss_nodes,
                 'MILSTAR': milstar_nodes,
                 'AEHF': aehf_nodes,
                 'GPS': gps_nodes,
                 'SBIRS': sbirs_nodes,

                 # These are included because although they use a different menu
                 # system, we still need to clear the screen
                 'OPS': [],
                 'PERSONNEL': [],
                 'INTEL': [],
                 'CYBER': [],
                 'ACQUISITIONS': []}

    return node_dict

def zoom_to(node, cur_center):
    """
    Description: Replace the menu nodes with the node map of the passed node.
    Parameters:
        node [Node()] -> The node to zoom in on
        cur_center [str] -> The name of the node currently in the center
    Returns: str -> The name of the node in the center
    """

    if node.data['name'] != cur_center:
        if node.data['is_zoomable']:
            return node.data['name']

    return cur_center

def render_back_arrow(window):
    """
    Description: Render a back arrow that will take us back to the main menu.
    Parameters:
        window [pyg.Surface] -> The surface to draw on
    Returns: None
    """
    arrow = fonts['zrnic48'].render("<--- EARTH", True, colors['white'])

    window.blit(arrow, (20, 20))

def render_bg(window, bg_star_coords):
    """
    Description: Render a faux starscape.
    Parameters:
        window [pyg.Surface] -> The surface to draw on
        bg_star_coords [list] -> A list containing coordinates and size data
                                 for each star
    Returns: None
    """
    for star in bg_star_coords:
        # Unpack the list
        x = star[0]
        y = star[1]
        size = star[2]
        corner = star[3]

        if corner == 1:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_top_left=True)
        elif corner == 2:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_top_right=True)
        elif corner == 3:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_bottom_left=True)
        else:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_bottom_right=True)

def main():
    # all_nodes is a dictionary that holds every node
    all_nodes = init_nodes()
    cur_center = 'EARTH'

    # full_menu is an object that is used for Earth's menu
    full_menu = FullMenu(window)

    # Create the background star effect
    bg_star_coords = []
    for i in range(10000):
        x = random.randint(-WIDTH, 2 * WIDTH)
        y = random.randint(-HEIGHT, 2 * HEIGHT)
        size = random.random() + 1.5
        corner = random.randint(1, 4)

        bg_star_coords.append([x, y, size, corner])


    # Timekeeping
    clock = pyg.time.Clock()
    FPS = 60

    while True:
        # Handle all events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()
                elif event.key == pyg.K_SPACE:
                    ...

            elif event.type == pyg.KEYUP:
                ...

            elif event.type == pyg.MOUSEBUTTONUP: # This will need to be fixed
                if event.pos[0] < 200 and event.pos[1] < 100 and cur_center != 'EARTH': # Will need to be changed
                    cur_center = 'EARTH'

                for node in all_nodes[cur_center]:
                    if node.is_selected and m_rel == (0, 0):
                        if math.dist(event.pos, node.rect.center) <= node.radius:
                            cur_center = zoom_to(node, cur_center)
                        else:
                            node.is_selected = False

                    # If a node is clicked on, select it
                    if node.is_hovered:
                        if math.dist(event.pos, node.rect.center) <= node.radius:
                            node.is_selected = True


        # Handle held down keys and mouse movement
        event_keys = pyg.key.get_pressed()
        mouse_keys = pyg.mouse.get_pressed()
        m_rel = pyg.mouse.get_rel()
         # Move all the nodes/stars if a key is pressed
        if event_keys[pyg.K_LEFT] or event_keys[pyg.K_a]:
            for node in all_nodes[cur_center]:
                node.rect.x += 15
            for star in bg_star_coords:
                star[0] += 1.5 # Move the nodes less for a parallax effect
        if event_keys[pyg.K_RIGHT] or event_keys[pyg.K_d]:
            for node in all_nodes[cur_center]:
                node.rect.x -= 15
            for star in bg_star_coords:
                star[0] -= 1.5
        if event_keys[pyg.K_UP] or event_keys[pyg.K_w]:
            for node in all_nodes[cur_center]:
                node.rect.y += 15
            for star in bg_star_coords:
                star[1] += 1.5
        if event_keys[pyg.K_DOWN] or event_keys[pyg.K_s]:
            for node in all_nodes[cur_center]:
                node.rect.y -= 15
            for star in bg_star_coords:
                star[1] -= 1.5
        # Move all the nodes/stars if the mouse is dragged
        if mouse_keys[0]:
            for node in all_nodes[cur_center]:
                node.rect.x += m_rel[0]
                node.rect.y += m_rel[1]
            for star in bg_star_coords:
                star[0] += m_rel[0] * .1
                star[1] += m_rel[1] * .1

        # Render the background
        window.fill(colors['black'])
        render_bg(window, bg_star_coords)

        # Update and render all the nodes
        for node in all_nodes[cur_center]:
            node.update()
            node.render()

        # If a node is selected, render it's menu
        for node in all_nodes[cur_center]:
            if node.is_selected:
                node.render_menu()
                break

        # If the current center node doesn't use nodes (e.x. OPS or CYBER), use
        # a full screen menu
        if len(all_nodes[cur_center]) == 0:
            full_menu.update()
            full_menu.render()

        # Give the user a way back to the main screen
        if cur_center != 'EARTH':
            render_back_arrow(window)

        # Update the display, and don't exceed FPS
        pyg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    # Initalize pygame and create a window
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("Upgrade Tree")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # Import assets after initalizing pygame
    from asset_loader import *

    # Start the program
    main()
