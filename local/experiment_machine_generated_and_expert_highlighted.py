"""
script to experiment with Martina's highlighting
Created on: September 30, 2019

@author: Ayon
"""
import os, sys
import csv

# import launch_experiment.
# We assume that it is located in the next-discovery top level directory.
sys.path.append("../")
from launch_experiment import *

def get_backend():
    """
    Get the backend host and port.

    Defaults to dict(host='localhost', port=8000).
    """
    return {
        'host': os.environ.get('NEXT_BACKEND_GLOBAL_HOST', 'localhost'),
        'port': os.environ.get('NEXT_BACKEND_GLOBAL_PORT', '8000')
    }


def read_csv_to_dictlist(fname):
    """
    read a csv file. return a list of dictionaries for each row in the csv file
    :param fname: string, path to the input csv file
    :return a list of dictionaries
    """
    with open(fname) as f:
        dictlist = [{k: str(v) for k, v in row.items()}
                    for row in csv.DictReader(f, skipinitialspace=True)]

    return dictlist


if __name__ == '__main__':
    # path to files
    SAMPLE_DATA_DIR = './data/04_SampleDataset/'
    target_file = './data/01_X/mol_dict_with_expert_annotation.json'
    pretest_dist_fname = './data/02_TestDistribution/test_dist_LewisSF.csv'
    training_dist_fname = './data/03_TrainingPool/training_dist_LewisSF.csv'
    guard_dataset_fname = \
        './data/04_SampleDataset/guard_questions_Lewis_SF.csv'
    posttest_dist_fname = './data/02_TestDistribution/test_dist_LewisSF.csv'
    training_dataset_fnames = ['DataE.txt',
                               'machine_generated_sequence_expert_annotated.txt']

    # keys
    pretest_dist_key = 'pretest_dist'
    training_data_key = 'training_data'
    posttest_dist_key = 'posttest_dist'
    guard_data_key = 'guard_data'
    alg_id_key = 'alg_id'
    alg_label_key = 'alg_label'
    time_required_key = 'time_required'
    monetary_gain_key = 'monetary_gain'
    seed_key = 'seed'

    experiment_list = []
    fixed_alg_id = 'FixedTrainRandomTest'
    alg_labels = ['MachineGenerated',
                  'MachineGeneratedExpertHighlighted']
    time_required = '30'

    # Create common alg_list
    alg_list = []

    # parameters for FixedTrainRandomTest
    for training_dataset_fname, alg_label in zip(training_dataset_fnames,
                                                 alg_labels):
        alg_item = {}
        alg_item[alg_id_key] = fixed_alg_id
        alg_item[alg_label_key] = alg_label
        alg_item[pretest_dist_key] = read_csv_to_dictlist(pretest_dist_fname)
        alg_item[training_data_key] = \
            read_csv_to_dictlist(SAMPLE_DATA_DIR + training_dataset_fname)
        alg_item[posttest_dist_key] = read_csv_to_dictlist(posttest_dist_fname)
        alg_item[guard_data_key] = read_csv_to_dictlist(guard_dataset_fname)
        alg_item[time_required_key] = time_required
        alg_item[monetary_gain_key] = ''
        alg_list.append(alg_item)

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
    initExp['args']['pretest_count'] = 20
    initExp['args']['training_count'] = 60
    initExp['args']['posttest_count'] = 40
    initExp['args']['guard_gap'] = 19
    initExp['args']['seed'] = 1000
    initExp['args']['participant_to_algorithm_management'] = 'one_to_one'  # assign one participant to one condition only
    initExp['args']['algorithm_management_settings'] = \
        algorithm_management_settings
    initExp['args']['alg_list'] = alg_list
    initExp['args']['instructions'] = '<h3>Do not click back or refresh the page!!!</h3>'
    initExp['args']['debrief'] = 'Go to the following \n ' + \
        '<a href="https://uwmadison.co1.qualtrics.com/jfe/form/SV_0BztEXJExjnvWCx" target="_blank">link</a>.\n ' + \
        '<br>Copy the User ID found below and enter the ID in the new survey to answer four ' + \
        'more questions. <b>Note that this is not the User ID you should enter in Mechanical Turk. That ID will be generated after you have ' + \
        'answered the four remaining questions. </b>'
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
    #host = "localhost:8000"
    backend = get_backend()
    host = "{}:{}".format(backend['host'], backend['port'])

    print "It's happening"
    exp_uid_list = launch_experiment(host, experiment_list)
    print "Made experiments {}".format(exp_uid_list)
