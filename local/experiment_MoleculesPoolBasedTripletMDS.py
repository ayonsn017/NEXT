import os, sys

# import launch_experiment. We assume that it is located in the next-discovery top level directory.
sys.path.append("../")
from launch_experiment import *

target_file = 'molecule_images.json'

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
#initExp['args']['n'] = 30
initExp['args']['d'] = 2
initExp['args']['failure_probability'] = .01
initExp['args']['participant_to_algorithm_management'] = 'one_to_many' 
initExp['args']['algorithm_management_settings'] = algorithm_management_settings 
initExp['args']['alg_list'] = alg_list 
initExp['args']['instructions'] = 'Are the following two molecules the same?'
initExp['args']['debrief'] = 'Test debrief'
initExp['app_id'] = 'MoleculesPoolBasedTripletMDS'
#initExp['site_id'] = 'replace this with working site id'
#initExp['site_key'] = 'replace this with working site key'


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
# Update the cartoon_dueling.html file wit the exp_uid_list and widget_key_list
# with open('strange_fruit_triplet.html','r') as page:
#   print "opended file"
#   page_string = page.read()
#   page_string = page_string.replace("{{exp_uid_list}}", str(exp_uid_list))
#   page_string = page_string.replace("{{widget_key_list}}", str(widget_key_list))
#   with open('../../next_frontend_base/next_frontend_base/templates/strange_fruit_triplet.html','w') as out:
#     out.write(page_string)
#     out.flush()
#     out.close()
