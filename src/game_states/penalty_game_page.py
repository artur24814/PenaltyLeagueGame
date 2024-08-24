from src.game_states.abstract import GameState
from src.ui_components.colors import WHITE, RED
from src.models.game_models import MatchWeek, Match, FootballClub
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from src.game_sprites.goal import Goal
from src.game_sprites.goalkeeper import GoalKeeper
from src.game_sprites.ball import Ball
from src.game_sprites.kicker import Kicker
from src.game_states.penalty_states.defending import DefendingPenaltyState
from src.game_states.penalty_states.shooting import ShootingPenaltyState
from src.services import generate_results_and_save_matches


class PenaltyGamePage(GameState):
    def __init__(self, game, pygame, screen, match_week_id=None):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.small_font = self.pygame.font.Font(None, 23)
        self.matchWeek = MatchWeek.query_creator.get_one(_id=match_week_id).execute()
        self.matches = self.matchWeek.get_matches
        self.player_team = FootballClub.query_creator.get_one(computer=0).execute()
        self.match = self.get_current_match()
        self.home_team = self.match.get_club_home
        self.away_team = self.match.get_club_away
        self.current_team = self.home_team.title if self.home_team.title == self.player_team.title else self.away_team.title
        self.oponent_team = self.home_team.title if self.away_team.title == self.player_team.title else self.away_team.title
        self.scores = {self.home_team.title: 0, self.away_team.title: 0}
        self.defendingState = DefendingPenaltyState("Defending")
        self.shootingState = ShootingPenaltyState("Shooting")
        self.current_state = self.shootingState if self.home_team.title == self.player_team.title else self.defendingState
        self.end_turn = False
        self.goal = Goal()
        self.goalkeeper = GoalKeeper()
        self.ball = Ball(start_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200), image_path=['assets', 'img', 'ball'])
        self.kicker = Kicker(
            start_pos=(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 + 220),
            image_path=['assets', 'img', 'kicker'],
            start_size=(370, 370)
        )
        self.all_sprites = self.pygame.sprite.Group()
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.kicker)

    def get_current_match(self):
        if (home_match := Match.query_creator.get_one(club_home=self.player_team.id, match_week_id=self.matchWeek.id).execute()):
            return home_match
        return Match.query_creator.get_one(club_away=self.player_team.id, match_week_id=self.matchWeek.id).execute()

    def custome_events(self, event):
        from src.game_states.match_week_page import MatchWeekPage
        if event.type == self.pygame.KEYDOWN:
            if event.key == self.pygame.K_ESCAPE:
                self.game.change_state(MatchWeekPage(self.game, self.pygame, self.screen))

            if event.key == self.pygame.K_q:
                self.current_state.player_choice = 0
            elif event.key == self.pygame.K_w:
                self.current_state.player_choice = 1
            elif event.key == self.pygame.K_e:
                self.current_state.player_choice = 2
            elif event.key == self.pygame.K_a:
                self.current_state.player_choice = 3
            elif event.key == self.pygame.K_s:
                self.current_state.player_choice = 4
            elif event.key == self.pygame.K_d:
                self.current_state.player_choice = 5
            elif event.key == self.pygame.K_z:
                self.current_state.player_choice = 6
            elif event.key == self.pygame.K_x:
                self.current_state.player_choice = 7
            elif event.key == self.pygame.K_c:
                self.current_state.player_choice = 8
            elif event.key == self.pygame.K_SPACE:
                self.run_resolve_turn()

    def run_resolve_turn(self):
        self.scores[self.current_team], self.scores[self.oponent_team] = self.current_state.resolve_turn(
            self.scores[self.current_team], self.scores[self.oponent_team]
        )
        self.end_turn = True
        if not self.ball.moving and self.current_state.player_choice is not None:
            self.kicker.animation = True
            self.start_ball_movement()

    def start_ball_movement(self):
        actual_selected_zone = self.current_state.player_choice if self.current_state == self.shootingState else self.current_state.oponent_choice
        self.ball.target_position = self.goal.get_target_position_for_zone(actual_selected_zone)
        self.ball.moving = True
        self.ball.animation = True

    def update(self):
        self.mouse_pos = self.pygame.mouse.get_pos()
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100
        self.arrow_end = (2 * center_x - self.mouse_pos[0], 2 * center_y - self.mouse_pos[1],)

        self.current_state.update_player_choice(self.goal.get_zone_for_point(self.arrow_end))

        if self.kicker.animation:
            self.kicker.update()

        if self.ball.moving and not self.kicker.animation:
            self.ball.update()

    def draw(self):
        self.draw_base()
        if self.end_turn and not self.ball.moving:
            self.draw_after_end_turn()

    def draw_base(self):
        self.draw_background_image(path_dir_list=['assets', 'img', 'soccer_goal_bg.jpg'])
        self.goal.draw_goal_zones(self.pygame, self.screen, selected_zone=self.current_state.player_choice)
        self.current_state.draw(self.pygame, self.screen, self.arrow_end)
        self.all_sprites.draw(self.screen)
        self.draw_status()

        self.goalkeeper.draw(
            self.pygame, self.screen,
            *self.goal.get_target_position_for_zone(
                1 if not self.end_turn else
                (self.current_state.player_choice if self.current_state == self.defendingState else self.current_state.oponent_choice)
            )
        )
        self.pygame.display.flip()

    def draw_status(self):
        scores_text = f"{self.home_team.title} {self.scores[self.home_team.title]} - {self.scores[self.away_team.title]} {self.away_team.title}"
        scores_text_surface = self.font.render(scores_text, True, WHITE)
        current_state_text_surface = self.small_font.render(self.current_state.state_text, True, WHITE)

        self.screen.blit(scores_text_surface, (WINDOW_WIDTH // 2 - 150, 50))
        self.screen.blit(current_state_text_surface, (WINDOW_WIDTH // 2 - 100, 150))

        if self.end_turn:
            result_text_surface = self.small_font.render(self.current_state.result_message, True, RED)
            self.screen.blit(result_text_surface, (WINDOW_WIDTH // 2 - 100, 250))

    def draw_after_end_turn(self):
        self.pygame.time.wait(1000)
        self.ball.rect.center = self.ball.start_pos
        self.ball.size = self.ball.start_size
        self.ball.image = self.pygame.transform.scale(self.ball.image, self.ball.size)
        self.end_turn = False
        self.set_next_state()
        self.goalkeeper.draw(self.pygame, self.screen, *self.goal.get_target_position_for_zone(1))
        self.pygame.display.flip()

    def set_next_state(self):
        self.current_state = self.shootingState if self.current_state == self.defendingState else self.defendingState

    def is_end_state(self):
        return self.shootingState.attempts >= 5 and self.defendingState.attempts >= 5

    def run_end_state(self):
        from src.game_states.season_page import SeasonPage
        self.save_results()
        self.pygame.time.wait(3000)
        self.game.change_state(SeasonPage(self.game, self.pygame, self.screen))

    def save_results(self):
        self.set_points_for_teams_after_finish_game()
        self.home_team.save().execute()
        self.away_team.save().execute()
        self.match.save(save_instance=True).execute()

        self.matchWeek.end = 1
        generate_results_and_save_matches(matches=list(filter(lambda m: m.id != self.match.id, self.matchWeek.get_matches)))
        self.matchWeek.save().execute()

    def set_points_for_teams_after_finish_game(self):
        winner = self.get_winner()
        if winner.startswith(self.home_team.title):
            self.home_team.set_points(3)
            self.away_team.set_points(0)
        elif winner.startswith(self.away_team.title):
            self.home_team.set_points(0)
            self.away_team.set_points(3)
        else:
            self.home_team.set_points(1)
            self.away_team.set_points(1)

    def get_winner(self):
        return f'{self.home_team.title} Win!' if self.scores[self.home_team.title] > self.scores[self.away_team.title] else \
            (f'{self.away_team.title} Win!' if self.scores[self.home_team.title] < self.scores[self.away_team.title] else 'Draw')
