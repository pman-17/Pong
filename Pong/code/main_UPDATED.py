from settings import * 
from sprites import *
import json

class Game:
    def __init__(self):
        pygame.init() 
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.running = True

        # === ADDED: Track game over state ===
        self.game_over = False

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        # === ADDED: score & high score setup ===
        self.score = {'player': 0, 'opponent': 0}
        self.high_score = 0

        # ===ADDED: Load existing high score ===
        try:
            with open(join('data', 'score.txt')) as score_file:
                data = json.load(score_file)
                if isinstance(data, dict):
                    self.high_score = data.get('high_score', 0)
        except Exception:
            pass

        self.font = pygame.font.Font(None, 150)
        self.high_score_font = pygame.font.Font(None, 40)
        # === ADDED: Game over fonts ===
        self.game_over_font = pygame.font.Font(None, 80)
        self.sub_font = pygame.font.Font(None, 35)

    def display_score(self):
        # player score
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2))
        self.display_surface.blit(player_surf, player_rect)

        # opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        #  # === ADDED: high score display ===
        high_score_surf = self.high_score_font.render(f'High Score: {self.high_score}', True, COLORS['bg detail'])
        high_score_rect = high_score_surf.get_frect(midtop = (WINDOW_WIDTH/8 * .75, 5))
        self.display_surface.blit(high_score_surf, high_score_rect)

        # net
        pygame.draw.line(self.display_surface, COLORS['bg detail'], (WINDOW_WIDTH /2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT), 5)

    # === ADDED: Overlay screen for game over ===
    def display_game_over(self):
        # Semi-transparent dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display_surface.blit(overlay, (0, 0))

        # === ADDED: Game Over title ===
        title_surf = self.game_over_font.render("GAME OVER", True, '#ee322c')
        title_rect = title_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 80))
        self.display_surface.blit(title_surf, title_rect)

        # === ADDED: Final Score text ===
        score_surf = self.sub_font.render(f"Final Score: {self.score['player']}  |  High Score: {self.high_score}", True, '#ffffff')
        score_rect = score_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.display_surface.blit(score_surf, score_rect)

        # === ADDED: Restart instruction ===
        restart_surf = self.sub_font.render("Press SPACE to Restart or ESC to Quit", True, '#aaaaaa')
        restart_rect = restart_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 70))
        self.display_surface.blit(restart_surf, restart_rect)

# === ADDED: GAME ENDS IF BALL HITS YOUR WALL ===
    def update_score(self, side):
        if side == 'player':
            self.score['player'] += 1
        else:
            # when ball hits player's wall (opponent scores)
            self.score['opponent'] += 1
            if self.score['opponent'] == 5:
                self.trigger_game_over() # GAME ENDS IF BALL HITS YOUR WALL

    # === ADDED: Logic to handle game over and record high score ===
    def trigger_game_over(self):
        self.game_over = True
        if self.score['player'] > self.high_score:
            self.high_score = self.score['player']
        self.save_data()

    # === ADDED: Reset method to start a new game ===
    def restart_game(self):
        self.score = {'player': 0, 'opponent': 0}
        self.game_over = False
        self.ball.reset()

    #ADDED =======
    def save_data(self):
        try:
            with open(join('data', 'score.txt'), 'w') as score_file:
                json.dump({'score': self.score, 'high_score': self.high_score}, score_file)
        except Exception:
            pass

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.save_data() #ADDED========

                # === ADDED: Controls to restart or quit from Game Over screen ===
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.restart_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False

            # === CHANGED: Pause sprite updates when game over ===
            if not self.game_over:
                self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS['bg'])
            self.display_score()
            self.all_sprites.draw(self.display_surface)

            # === ADDED: Render game over screen if active ===
            if self.game_over:
                self.display_game_over()

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()