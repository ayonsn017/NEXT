import os, sys
import csv

# import launch_experiment. We assume that it is located in the next-discovery top level directory.
sys.path.append("../")
from launch_experiment import *


def read_csv_to_dictlist(fname):
    """
    read a csv file. return a list of dictionaries for each row in the csv file
    :param fname: string, path to the input csv file
    :return a list of dictionaries
    """
    with open(fname) as f:
        dictlist = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

    return dictlist


if __name__ == '__main__':
    # path to files
    target_file = './data/01_X/mol_img_dict.json'
    pretest_dist_fname = './data/02_TestDistribution/test_dist_LewisSF.csv'
    training_dist_fname = './data/03_TrainingPool/training_dist_LewisSF.csv'
    training_dataset_fname = './data/04_SampleDataset/training_sequence_Data2.csv'
    guard_dataset_fname = './data/04_SampleDataset/guard_questions_Lewis_SF.csv'
    posttest_dist_fname = './data/02_TestDistribution/test_dist_LewisSF.csv'

    # keys
    pretest_dist_key = 'pretest_dist'
    training_data_key = 'training_data'
    posttest_dist_key = 'posttest_dist'
    guard_data_key = 'guard_data'
    alg_id_key = 'alg_id'
    alg_label_key = 'alg_label'
    time_required_key = 'time_required'
    monetary_gain_key = 'monetary_gain'

    experiment_list = []
    alg_ids = ['FixedTrainRandomTest', 'RandomTrainTest']

    # Create common alg_list
    alg_list = []


    # parameters for FixedTrainRandomTest
    alg_item = {}
    alg_item[alg_id_key] = alg_ids[0]
    alg_item[alg_label_key] = alg_ids[0]
    alg_item[pretest_dist_key] = read_csv_to_dictlist(pretest_dist_fname)
    alg_item[training_data_key] = read_csv_to_dictlist(training_dataset_fname)
    alg_item[posttest_dist_key] = read_csv_to_dictlist(posttest_dist_fname)
    alg_item[guard_data_key] = read_csv_to_dictlist(guard_dataset_fname)
    alg_item[time_required_key] = '5-10'
    alg_item[monetary_gain_key] = 'You will be entered in a lottery to win a $50 cash prize.'
    alg_list.append(alg_item)

    # parameters for RandomTrainTest
    alg_item = {}
    alg_item[alg_id_key] = alg_ids[1]
    alg_item[alg_label_key] = alg_ids[1]
    alg_item[pretest_dist_key] = read_csv_to_dictlist(pretest_dist_fname)
    alg_item[training_data_key] = read_csv_to_dictlist(training_dist_fname)
    alg_item[posttest_dist_key] = read_csv_to_dictlist(posttest_dist_fname)
    alg_item[guard_data_key] = read_csv_to_dictlist(guard_dataset_fname)
    alg_item[time_required_key] = '5-10'
    alg_item[monetary_gain_key] = 'You will be entered in a lottery to win a $50 cash prize.'
    alg_list.append(alg_item)

    '''
    for idx,alg_id in enumerate(alg_ids):
        alg_item = {}
        alg_item['alg_id'] = alg_id
        if idx==0:
            alg_item['alg_label'] = 'Test'
        else:
            alg_item['alg_label'] = alg_id
        alg_item[pretest_file_key] = pretest_dist_fname
        alg_item[training_file_key] = training_dist_fname
        #alg_item[training_file_key] = training_dataset_fname
        alg_item[posttest_file_key] = posttest_dist_fname

        #alg_item['params'] = {}
        alg_list.append(alg_item)
    '''

    # Create common algorithm management settings
    params = []
    for algorithm in alg_list:
        params += [{'alg_label': algorithm['alg_label'],
    	        'proportion': 1.0 / len(alg_list)}]

    algorithm_management_settings = {}
    #algorithm_management_settings['mode'] = 'fixed_proportions'
    algorithm_management_settings['mode'] = 'custom'  # switch between algorithms for each participant
    algorithm_management_settings['params'] = params


    # Create experiment dictionary
    initExp = {}
    initExp['args'] = {}
    initExp['args']['pretest_count'] = 2
    initExp['args']['training_count'] = 6
    initExp['args']['posttest_count'] = 4
    initExp['args']['guard_gap'] = 5
    initExp['args']['participant_to_algorithm_management'] = 'one_to_one'  # assign one participant to one condition only
    initExp['args']['algorithm_management_settings'] = algorithm_management_settings
    initExp['args']['alg_list'] = alg_list
    initExp['args']['instructions'] = 'Do not click back or refresh the page!!!'
    initExp['args']['debrief'] = 'Thank you for your participation <a href="www.google.com" target="_blank">here</a>. Your response has been recorded.'
    # the number of questions the participant will see, this value will be calculated by adding pretest_count, training_count and posttest_count
    initExp['args']['num_tries'] = 1
    initExp['app_id'] = 'MoleculeEquivalence'


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
