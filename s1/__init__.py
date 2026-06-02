from otree.api import *

import random
import time
import string
import json
import os


_tasks_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
with open(_tasks_path, 'r') as f:
    HARD_CODED_TASKS = json.load(f)



doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 's1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TASK_TIME = 120  # seconds
    NUM_TASKS = 100  # pre-generate this many tasks


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    score = models.IntegerField(initial=0)
    bonus = models.FloatField(initial=0)
    current_task_index = models.IntegerField(initial=0)
    task_start_time = models.FloatField(initial=0)
    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)
    task_blur_log = models.LongStringField(blank=True)
    task_blur_count = models.IntegerField(initial=0, blank=True)


def creating_session(subsession: Subsession):
    if 'decryption_tasks' not in subsession.session.vars:
        subsession.session.vars['decryption_tasks'] = HARD_CODED_TASKS
# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class Task(Page):
    form_model = 'player'
    task_blur_log = models.LongStringField(blank=True)
    task_blur_count = models.IntegerField(initial=0, blank=True)
    @staticmethod
    def vars_for_template(player: Player):
        tasks = player.session.vars['decryption_tasks']
        idx = player.current_task_index
        task = tasks[idx]
        # Sort key items for display
        key_items = sorted(task['key'].items())
        return dict(
            task_index=idx,
            code=task['code'],
            key_items=key_items,
            time_limit=C.TASK_TIME,
            score=player.score,
            hidden_fields=['blur_log', 'blur_count', 'blur_warned'],
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass  # score is updated via live_method

    @staticmethod
    def live_method(player: Player, data):
        """
        Handles AJAX calls from the page:
          - 'start': records the start timestamp
          - 'submit': checks the answer and advances task or ends
        """
        tasks = player.session.vars['decryption_tasks']

        if data['type'] == 'start':
            if player.task_start_time == 0:
                player.task_start_time = float(data['timestamp'])
            return {player.id_in_group: {'type': 'ack'}}

        if data['type'] == 'submit':
            now = float(data['timestamp'])
            elapsed = now - player.task_start_time
            time_remaining = C.TASK_TIME - elapsed

            if time_remaining <= 0:
                return {player.id_in_group: {'type': 'timeout'}}

            idx = player.current_task_index
            task = tasks[idx]
            user_answer = data['answer'].strip().upper()

            if user_answer != task['answer']:
                return {player.id_in_group: {
                    'type': 'error',
                    'message': 'Your decryption is incorrect, try again.'
                }}

            # Correct answer
            player.score += 1
            player.current_task_index += 1

            if player.current_task_index >= len(tasks):
                return {player.id_in_group: {'type': 'done', 'score': player.score}}

            # Send next task
            next_task = tasks[player.current_task_index]
            key_items = sorted(next_task['key'].items())
            return {player.id_in_group: {
                'type': 'next_task',
                'code': next_task['code'],
                'key_items': key_items,
                'score': player.score,
                'time_remaining': time_remaining,
            }}


class Results(Page):

    @staticmethod
    def vars_for_template(player):
        player.participant.s1score = player.score
        player.bonus = 0.05 * player.score

class Redirect(Page):
    form_model = 'player'

    @staticmethod
    def js_vars(player: Player):
        return dict(
            completionlinkfull=player.session.config.get('completionlinkfull')
        )

page_sequence = [Intro, Task, Results, Redirect]
