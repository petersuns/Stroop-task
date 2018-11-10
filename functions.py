import random
import csv
import os
from psychopy import visual, event, core, gui
from time import gmtime, strftime

global my_window, text_stim_intro, text_stim_stimuli
#conda install wxpython


# Run a phase of the experiment and return the result.
def run_phase(explanation_text, phase_word_list, keys_to_color, time_to_enter_item_seconds, time_between_item_seconds, amount_blocks=1):
    show_text(explanation_text)

    block_results = []
    for i in range(amount_blocks):
        random.shuffle(phase_word_list)
        block_results.append(run_block(phase_word_list, keys_to_color, time_to_enter_item_seconds, time_between_item_seconds))

    return block_results


# Runs the experiment with a given list of color pairs
def run_block(word_list, keys_to_color, time_to_enter_item_seconds, time_between_item_seconds):
    global my_window, text_stim_stimuli

    block_results = []
    timer = core.Clock()
    for pair in word_list:
        focus(time_between_item_seconds)
        text_stim_stimuli.setText(pair[0])
        text_stim_stimuli.setColor(pair[1])
        timer.reset()

        text_stim_stimuli.draw()
        my_window.flip()

        possible_pressed_keys = ['escape'] + keys_to_color.keys()
        pressed_keys = event.waitKeys(keyList=possible_pressed_keys, maxWait=time_to_enter_item_seconds)

        if pressed_keys is None:
            new_result = (pair, 'None', timer.getTime())
            block_results.append(new_result)
        elif 'escape' in pressed_keys:
            my_window.close() + core.quit()
        else:
            chosen_color = keys_to_color[pressed_keys[0]]
            new_result = (pair, chosen_color, timer.getTime())
            block_results.append(new_result)

    return block_results

# Focus between each item for a given amount of seconds (default 1 sec)
def focus(num_seconds=1):

    timer = core.CountdownTimer(num_seconds)
    text_stim_stimuli.setText('+');
    text_stim_stimuli.setColor('black')
    while timer.getTime() > 0:
        text_stim_stimuli.draw()
        my_window.flip()

        pressed_keys = event.getKeys(['escape'])
        if 'escape' in pressed_keys:
            my_window.close() + core.quit()

# Calculates score from phase
def calculate_score_phase(phase_results, phase_number):
    amount_tests = 0
    score = 0

    for block in phase_results:
        amount_tests = amount_tests + len(block)
        for result in block:

            if phase_number == 1:
                correct_color = result[0][0]

            elif phase_number == 2:
                correct_color = result[0][1]

            else:
                correct_color = None

            chosen_color = result[1]
            if correct_color == chosen_color:
                score = score + 1

    return float(score) / amount_tests




# Gives the participant feedback about the amount of correct items
def draw_feedback(score):
    show_text("You had " + "{0:.2f}".format(score * 100) + "% of the items correct.")


# Shows a given text on the screen until the user presses enter
def show_text(text, color='black'):
    global my_window, text_stim_intro

    text_stim_intro.setText(text)
    text_stim_intro.setColor(color)
    text_stim_intro.draw()
    my_window.flip()

    pressed_keys = event.waitKeys(keyList=['escape', 'return'])
    if 'escape' in pressed_keys:
        my_window.close() + core.quit()


def export_phase_results(write_title, output_folder_path, time, phase_number, phase_results, phase_score, participant_age, participant_gender, participant_number):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    filename = 'PartNr' + '_' + str(participant_number) + '_' + time + '.csv'

    with open(output_folder_path + '/' + filename, 'ab') as output_file:
        csv_writer = csv.writer(output_file, dialect=csv.excel)
        if(write_title):
            title_row = ['Participant number', 'Age', 'Gender', 'Phase', 'Phase score', 'Block', 'Word', 'Color',
                         'Response', 'Time']
            csv_writer.writerow(title_row)

        block_number = 0
        for block in phase_results:
            block_number = block_number + 1
            for result in block:
                word = result[0][0]
                color = result[0][1]
                response = result[1]
                time = result[2]
                row = [participant_number, participant_age, participant_gender, phase_number, phase_score, block_number,
                       word, color, response, time]
                csv_writer.writerow(row)


# Here we ask for participant info, such as participant number, age and gender
def get_participant_info():
    dialog = gui.Dlg(title="Participant Information")
    dialog.addField("Please enter your age:")
    dialog.addField("Please enter your gender(m/f):")
    dialog.addField("Participant number: ")
    ok_data = dialog.show()
    ok_data = ['None', 'None', 'None'] if ok_data is None else ok_data

    if dialog.OK:
        participant_age = "not given" if ok_data[0] is None else ok_data[0]
        participant_gender = "not given" if ok_data[1] is None else ok_data[1]
        participant_number = "not given" if ok_data[2] is None else ok_data[2]

        return participant_age, participant_gender, participant_number
    else:
        core.quit()

# Get the text in a textfile/path
def load_text_file(file_path):
    f = open(file_path, "r")
    f_text = f.read()
    f.close()
    return f_text


def initialize_gui():
    global my_window, text_stim_intro, text_stim_stimuli

    # Create window
    my_window = visual.Window(units='pix', color="gray", fullscr=True,
                              screen=1)
    
    text_stim_intro = visual.TextStim(my_window, height=40, wrapWidth=my_window.size[1])
    text_stim_stimuli = visual.TextStim(my_window, height=80, wrapWidth=my_window.size[1])


def close_gui():
    global my_window
    my_window.close()
