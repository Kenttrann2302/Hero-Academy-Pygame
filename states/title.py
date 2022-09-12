from states.state import State
from states.game_world import Game_World

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)

    # handle the transition to other states of the game
    def update(self, delta_time, actions):
        if actions["start"]:
            new_state = Game_World(self.game)
            # add the new state to the top of the stack, the new state will render if we go the next frame
            new_state.enter_state()
        self.game.reset_keys()

    # fill the screen
    def render(self, display):
        display.fill((255, 255, 255))
        self.game.draw_text(display, "Game States Demo", (0, 0, 0), self.game.GAME_W/2, self.game.GAME_H/2)
