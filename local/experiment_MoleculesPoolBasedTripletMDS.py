import os, sys

# import launch_experiment. We assume that it is located in the next-discovery top level directory.
sys.path.append("../")
from launch_experiment import *

target_file = 'data/01_X/mol_img_dict.json'
pretest_dist_fname = './local/data/02_TestDistribution/test_dist_LewisSF.csv'
training_dist_fname = './local/data/03_TrainingPool/training_dist_LewisSF.csv'
posttest_dist_fname = './local/data/02_TestDistribution/test_dist_LewisSF.csv'

pretest_file_key = 'pretest_file'
training_file_key = 'training_file'
posttest_file_key = 'posttest_file'

experiment_list = []
alg_ids = ['RandomTrainTest','RandomTrainTest']

# Create common alg_list
alg_list = []
for idx,alg_id in enumerate(alg_ids):
    alg_item = {}
    alg_item['alg_id'] = alg_id
    if idx==0:
        alg_item['alg_label'] = 'Test'
    else:
        alg_item['alg_label'] = alg_id    
    alg_item['test_alg_label'] = 'Test'
    alg_item[pretest_file_key] = pretest_dist_fname
    alg_item[training_file_key] = training_dist_fname
    alg_item[posttest_file_key] = posttest_dist_fname

    #alg_item['params'] = {}
    alg_list.append(alg_item)

# Create common algorithm management settings  
params = []
for algorithm in alg_list:
    params += [{'alg_label': algorithm['alg_label'],
	        'proportion': 1.0 / len(alg_list)}]

algorithm_management_settings = {}
algorithm_management_settings['mode'] = 'fixed_proportions'
algorithm_management_settings['params'] = params


# Create experiment dictionary
initExp = {}
initExp['args'] = {}
initExp['args']['pretest_count'] = 2
initExp['args']['training_count'] = 6
initExp['args']['posttest_count'] = 4
initExp['args']['participant_to_algorithm_management'] = 'one_to_one'  # assign one participant to one condition only
initExp['args']['algorithm_management_settings'] = algorithm_management_settings 
initExp['args']['alg_list'] = alg_list 
initExp['args']['instructions'] = 'Answer the following question'
initExp['args']['debrief'] = 'Thank you for your participation. Your response has been recorded '
# the number of questions the participant will see, this value will be calculated by adding pretest_count, training_count and posttest_count
initExp['args']['num_tries'] = 1 
initExp['app_id'] = 'MoleculesPoolBasedTripletMDS'


curr_dir = os.path.dirname(os.path.abspath(__file__))
experiment = {}
experiment['initExp'] = initExp
experiment['primary_type'] = 'json-urls'
experiment['primary_target_file'] = target_file
experiment_list.append(experiment)

# Launch the experiment
host = "localhost:8000"
print "It's happening"
exp_uid_list = launch_experiment(host, experiment_list)
print "Made experiments {}".format(exp_uid_list)
