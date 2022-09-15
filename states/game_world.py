import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu
from camera import *

# create the game world
class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        # create the background
        self.grass_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))
        self.player = Player(self.game)

    def update(self, delta_time, actions):
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)

    def render(self, display):
        display.blit(self.grass_img, (0, 0))
        self.player.render(display)

# create the character
class Player():
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = 200, 200
        self.current_frame, self.last_frame_update = 0, 0

    def update(self, delta_time, actions):
        # get the direction from input
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]
        # update the position
        self.position_x += 100 * delta_time * direction_x
        self.position_y += 100 * delta_time * direction_y
        # animate the sprite
        self.animate(delta_time, direction_x, direction_y)

    def render(self, display):
        display.blit(self.curr_image, (self.position_x, self.position_y))

    def animate(self, delta_time, direction_x, direction_y):
        # compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # if no direction is pressed, set image to idle and run
        if not (direction_x or direction_y):
            self.curr_image = self.curr_anim_list[0]
            return
        # if an image was pressed, use the appropriate list of frames according to the direction
        if direction_x:
            if direction_x > 0:
                self.curr_anim_list = self.right_sprites
            else:
                self.curr_anim_list = self.left_sprites

        if direction_y:
            if direction_y > 0:
                self.curr_anim_list = self.front_sprites
            else:
                self.curr_anim_list = self.back_sprites

        # advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        # Get the directory with the player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [], [], [], []
        # Load in the frames for each direction
        for i in range(1, 5):
            self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) + ".png")))
            self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) + ".png")))
        # set the default frames to facing front
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites
        
        # Load the camera that follow the player
        player = Player()
        camera = Camera(player)
        follow = Follow(camera, player)
        border = Border(camera, player)
        auto = Auto(camera, player)
        camera.set_method(follow)
        




