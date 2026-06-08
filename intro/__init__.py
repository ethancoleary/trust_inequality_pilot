from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(
        widget=widgets.CheckboxInput,
        blank=False,
    )
    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)


# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def error_message(player, values):
        if values.get('consent') != 1:
            return "Please consent to participation or withdraw from the experiment by closing your browser."

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }






page_sequence = [
                Consent

                 ]
