"""Created on Wed Nov 22 22:02:21 2017
@author: Chiara & Shuo
"""
import itertools
import os

# Please change this to your path
os.chdir('/Users/shuosun/Documents/KU Leuven/Stroop task') 

from time import gmtime, strftime
from functions import *


keys_to_color = {'1': 'red', '2': 'blue', '3': 'yellow', '4': 'purple', '5': 'green'}
color_list = list(keys_to_color.values())
word_list = list(itertools.permutations(color_list, 2))

time_between_item_seconds = 1
time_to_enter_item_seconds = 5 

write_output_file_column_names = True
output_folder_path = 'output'
show_feedback = True

amount_blocks_phase_1 = 4
amount_blocks_phase_2 = 4

participant_age, participant_gender, participant_number = get_participant_info()

initialize_gui()


phase_one_text = load_text_file("data/prompt_phase1.txt")
phase_two_text = load_text_file("data/prompt_phase2.txt")

results_phase_one = run_phase(phase_one_text, word_list, keys_to_color, time_to_enter_item_seconds, time_between_item_seconds, amount_blocks_phase_1)
score_phase_one = calculate_score_phase(results_phase_one, 1)

if show_feedback:
    draw_feedback(score_phase_one)

results_phase_two = run_phase(phase_two_text, word_list, keys_to_color, time_to_enter_item_seconds, time_between_item_seconds, amount_blocks_phase_2)
score_phase_two = calculate_score_phase(results_phase_two, 2)

if show_feedback:
    draw_feedback(score_phase_two)

time = strftime('%Y%m%d%H%M', gmtime())

export_phase_results(write_output_file_column_names, output_folder_path, time, 1, results_phase_one, score_phase_one, participant_age, participant_gender, participant_number)
export_phase_results(False, output_folder_path, time, 2, results_phase_two, score_phase_two, participant_age, participant_gender, participant_number)

close_gui()
