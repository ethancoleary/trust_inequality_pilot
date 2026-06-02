# common.py

from otree.api import Page
from otree.api import BaseConstants
from otree.api import  models, widgets
import json

# %% Functions


# %% Player
# DOESNT WORK WITH PLAYER

# %% Pages
class MyBasePage(Page):
    form_model = 'player'
    form_fields = ['blur_log', 'blur_count', 'blur_warned']


    @staticmethod
    def vars_for_template(player):
            

        return {
            'hidden_fields': ['blur_log', 'blur_count','blur_warned'],
            'Completion_fee': CommonConstants.Completion_fee,
            
            'Instructions_path': Instructions_path,
            'Task_path': Task_path,

        }
                   

    @staticmethod
    def before_next_page(player, timeout_happened=False):
        blob = player.blur_log or '{}'
        page_counts = json.loads(blob)
        Blur_log = player.participant.vars.get('Blur_log', {})
        for page_name, count in page_counts.items():
            Blur_log[page_name] = Blur_log.get(page_name, 0) + count
        player.participant.vars['Blur_log'] = Blur_log
        player.participant.vars['Blur_count'] = (
            player.participant.vars.get('Blur_count', 0)
            + (player.blur_count or 0))
        
        # if player has been warned in this page, we set the flag and keep track of it, if not we keep the previous value
        # TODO: decide if you want the bonus to be determined based on the blur_warned flag, if so, adjust your bonus logic accordingly
        if player.blur_warned:
            player.participant.Blur_warned = 1
        
