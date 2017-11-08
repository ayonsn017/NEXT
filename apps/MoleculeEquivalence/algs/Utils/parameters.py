pretest_seed = 1023  # the starting seed to generate pretest questions
training_seed = 424  # the starting seed to generate training questions
posttest_seed = 7864  # the starting seed to generate postest questions

pretest_key = 'pretest'  # this is used as ques_type for pretest questions for the widget
training_key = 'training'  # this is used as ques_type for pretest questions for the widget
posttest_key = 'posttest'  # this is used as ques_type for pretest questions for the widget
instruction_key = 'instruction'  # this is used as ques_type for instruction questions for the widget
terms_key = 'terms'  # this is used as a ques_type for instruction quesiton where a check box must be clicked to proceed
guard_key = 'guard'

ques_gen_lock_name = 'ques_gen_lock'  # the name of the lock to be used for question generation

# instruction question counts
# introduction_instructions_count = 2
introduction_instructions_count = 1  # removing the first instruction since we do not need consent in MTurk
pretest_instructions_count = 1
training_instructions_count = 1
posttest_instructions_count = 1

# keys common across algorithms
pretest_count_key = 'pretest_count'
training_count_key = 'training_count'
posttest_count_key = 'posttest_count'
guard_gap_key = 'guard_gap'
guard_count_key = 'guard_count'
total_questions_key = 'total_questions'
num_reported_answers_key = 'num_reported_answers'
pretest_seed_key = 'pretest_seed'
training_seed_key = 'training_seed'
posttest_seed_key = 'posttest_seed'
participant_info_dict_key = 'participant_info_dict'
alg_label_key = 'alg_label'
monetary_gain_key = 'monetary_gain'
pretest_dist_key = 'pretest_dist'
training_data_key = 'training_data'
posttest_dist_key = 'posttest_dist'
guard_data_key = 'guard_data'
time_required_key = 'time_required'
