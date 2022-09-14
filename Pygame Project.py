import os, time, pygame
from states.title import Title
from util import load_save, reset_keys
from controls import Controls_Handler

# initiate the pygame window
class Game():
    def __init__(self):
        pygame.init()
        # set the game window width and height
        self.GAME_W, self.GAME_H = 480, 270
        # set the screen width and height
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 960, 540
        # set the surface for pygame
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        # set the screen for pygame
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # define true statement when the game is running
        self.running, self.playing = True, True
        # define the init actions
        self.actions = {"left": False, "right": False, "up": False, "down": False, "action1": False, "acton2": False,
                        "start": False}
        # set the time
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_states()
        
    # Load the current save file
    save = load_save()
    control_handler = Controls_Handler(save)

    def game_loop(self):
        while self.playing:
            # computer delta time
            self.get_dt()
            # get the events which are the interactions from the users
            self.get_events()
            # update the game according to the players' interactions
            self.update()
            # render them all onto the screen
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            # getting the key actions from users
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.playing = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.actions["left"] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.actions["right"] = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.actions["up"] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.actions["down"] = True
                if event.key == pygame.K_p:
                    self.actions["action1"] = True
                if event.key == pygame.K_o:
                    self.actions["action2"] = True
                if event.key == pygame.K_RETURN:
                    self.actions["start"] = True

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        # text_surface.set_color_key((0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    # Create pointers to directory
    # using os path can create itself
    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprite")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)


    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
