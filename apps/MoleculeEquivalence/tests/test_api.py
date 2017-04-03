import numpy
import numpy.random
import random
import json
import time
import requests
from scipy.linalg import norm
from multiprocessing import Pool
import os
import sys
import re
import csv
import imp
import getopt
import zipfile
import datetime
from StringIO import StringIO
try:
    import next.apps.test_utils as test_utils
except:
    sys.path.append('../../../next/apps')
    import test_utils

app_id = 'MoleculeEquivalence'


def generate_target_blob(prefix,
                         primary_file,
                         primary_type,
                         experiment=None,
                         alt_file=None,
                         alt_type='text'):
    '''
    Upload targets and return a target blob for upload with the target_manager.

    Inputs: ::\n
        file: fully qualified path of a file on the system.
          Must be a zipfile with pictures or a text file.
        prefix: string to prefix every uploaded file name with
   '''
    print "generating blob"
    targets = []
    is_primary_zip = ((type(primary_file) is str and primary_file.endswith('.zip'))
                      or (zipfile.is_zipfile(primary_file)))

    if is_primary_zip:
        target_file_dict, target_name_dict = zipfile_to_dictionary(primary_file)
        if alt_type != 'text':
            assert alt_file != None, 'Need an alt_file.'
            alt_file_dict, alt_name_dict = zipfile_to_dictionary(alt_file)
            try:
                pairs = [(target_name_dict[key],
                          target_file_dict[key],
                          alt_name_dict[key],
                          alt_file_dict[key])
                         for key in target_file_dict.keys()]
            except:
                raise Exception('Primary target names must'
                                'match alt target names.')

            for primary_name, primary_file, alt_name, alt_file in pairs:
                    target = {'target_id': '{}_{}'.format(prefix, primary_name),
                              'primary_type': primary_type,
                              'alt_type': alt_type,
                              'alt_description': alt_url}
                    targets.append(target)
        else:
           for i, (key, primary_file) in enumerate(target_file_dict.iteritems()):
                primary_file_name = target_name_dict[key]
                if i % 100 == 0 and i != 0:
                    print('percent done = {}'.format(i / 50e3))
                target = {'target_id': '{}_{}'.format(prefix, primary_file_name),
                          'primary_type': primary_type,
                          'alt_type': 'text',
                          'alt_description': primary_file_name}
                targets.append(target)
    elif primary_type == 'json-urls':
        with open(primary_file, 'r') as f:
            targets_dict = json.load(f)
        targets_next = []
        for i, (name, url) in enumerate(targets_dict.items()):
            target_next = {'target_id': str(i),
                           'primary_type': 'image',
                           'primary_description': '"' + url + '"',
                           'alt_type': 'text',
                           'alt_description': name}
            targets_next += [target_next]
        targets = targets_next
    else:
        if type(primary_file) is str:
            f = open(primary_file)
        else:
            f = primary_file
            f.seek(0)
        i = 0
        for line in f.read().splitlines():
            line = line.strip()
            if line:
                i += 1
                target = {'target_id': str(i),
                          'primary_type': 'text',
                          'primary_description':line,
                          'alt_type': 'text',
                          'alt_description':line}
                targets.append(target)
        print "\ntargets formatted like \n{}\n".format(targets[0])
    return targets


def zipfile_to_dictionary(filename):
    """
    Takes in a zip file and returns a dictionary with the filenames
    as keys and file objects as values

    Inputs: ::\n
        file: the concerned zip file

    Outputs: ::\n
        result: the returned dictionary
    """
    zf = zipfile.ZipFile(filename, 'r')
    files_list = zf.namelist()
    dictionary = {}
    names_dictionary = {}
    for i in files_list:
        if re.search(r"\.(jpe?g|png|gif|bmp|mp4|mp3)",
                     i, re.IGNORECASE) and not i.startswith('__MACOSX'):
            f = zf.read(i)
            name = os.path.basename(i).split('.')[0]
            dictionary[name] = f
            names_dictionary[name] = os.path.basename(i)
    return dictionary, names_dictionary


def import_experiment_list(file):
    # Load experiment file
    mod = imp.load_source('experiment', file)
    experiment_list = mod.experiment_list
    return experiment_list


def test_api(assert_200=True, num_experiments=1, num_clients=8):
    """
    method to test the app
    :param assert_200: boolean, default value True
    :param num_experiments: int, number of experiments to run
    :param num_clients: int, number of clients to simulate
    """
    print os.getcwd()

    # path to files
    target_file = '../../../local/data/01_X/mol_img_dict.json'
    pretest_dist_fname = './local/data/02_TestDistribution/test_dist_LewisSF.csv'
    training_dist_fname = './local/data/03_TrainingPool/training_dist_LewisSF.csv'
    training_dataset_fname = './local/data/04_SampleDataset/training_dataset.csv'
    guard_dataset_fname = './local/data/04_SampleDataset/guard_dataset.csv'
    posttest_dist_fname = './local/data/02_TestDistribution/test_dist_LewisSF.csv'

    # keys
    pretest_file_key = 'pretest_file'
    training_file_key = 'training_file'
    posttest_file_key = 'posttest_file'
    guard_file_key = 'guard_file'
    alg_id_key = 'alg_id'
    alg_label_key = 'alg_label'
    time_required_key = 'time_required'
    monetary_gain_key = 'monetary_gain'

    # question count variables
    pretest_count = 2
    training_count = 6
    posttest_count = 4
    guard_gap = 5

    pool = Pool(processes=num_clients)
    supported_alg_ids = ['FixedTrainRandomTest', 'RandomTrainTest']
    alg_list = []

    # parameters for FixedTrainRandomTest
    alg_item = {}
    alg_item[alg_id_key] = supported_alg_ids[0]
    alg_item[alg_label_key] = supported_alg_ids[0]
    alg_item[pretest_file_key] = pretest_dist_fname
    alg_item[training_file_key] = training_dataset_fname
    alg_item[posttest_file_key] = posttest_dist_fname
    alg_item[guard_file_key] = guard_dataset_fname
    alg_item[time_required_key] = '5-10'
    alg_item[monetary_gain_key] = 'You will be entered in a lottery to win a $50 cash prize.'
    alg_list.append(alg_item)

    # parameters for RandomTrainTest
    alg_item = {}
    alg_item[alg_id_key] = supported_alg_ids[1]
    alg_item[alg_label_key] = supported_alg_ids[1]
    alg_item[pretest_file_key] = pretest_dist_fname
    alg_item[training_file_key] = training_dist_fname
    alg_item[posttest_file_key] = posttest_dist_fname
    alg_item[guard_file_key] = guard_dataset_fname
    alg_item[time_required_key] = '5-10'
    alg_item[monetary_gain_key] = 'You will be entered in a lottery to win a $50 cash prize.'
    alg_list.append(alg_item)

    params = []
    for algorithm in alg_list:
        params.append({'alg_label': algorithm['alg_label'],
                       'proportion': 1. / len(alg_list)})
    algorithm_management_settings = {}
    algorithm_management_settings['mode'] = 'custom'  # switch between algorithms for each participant
    algorithm_management_settings['params'] = params

    # Test POST Experiment
    initExp_args_dict = {}
    initExp_args_dict['app_id'] = app_id
    initExp_args_dict['args'] = {}
    initExp_args_dict['args']['pretest_count'] = pretest_count
    initExp_args_dict['args']['training_count'] = training_count
    initExp_args_dict['args']['posttest_count'] = posttest_count
    initExp_args_dict['args']['guard_gap'] = guard_gap
    initExp_args_dict['args']['participant_to_algorithm_management'] = 'one_to_one'  # assign one participant to one
    # condition only
    initExp_args_dict['args']['algorithm_management_settings'] = algorithm_management_settings
    initExp_args_dict['args']['alg_list'] = alg_list
    initExp_args_dict['args']['instructions'] = 'Answer the following question.'
    initExp_args_dict['args']['debrief'] = 'Thank you for your participation. Your response has been recorded.'
    # the number of questions the participant will see, this value will be calculated by adding pretest_count,
    # training_count, posttest_count and number of instruction questions
    initExp_args_dict['args']['num_tries'] = 1

    experiment = {}
    experiment['initExp'] = initExp_args_dict
    experiment['primary_type'] = 'json-urls'
    experiment['primary_target_file'] = target_file

    targets = generate_target_blob(prefix=str(datetime.date.today()), primary_file=experiment['primary_target_file'],
                                   primary_type=experiment['primary_type'],
                                   alt_file=experiment.get('alt_target_file', None), experiment=experiment,
                                   alt_type=experiment.get('alt_type', 'text'))
    initExp_args_dict['args']['targets'] = {'targetset': targets}

    exp_info = []
    for ell in range(num_experiments):
        initExp_response_dict, exp_uid = test_utils.initExp(initExp_args_dict)
        exp_info += [exp_uid]

    # Generate participants
    participants = []
    pool_args = []
    for i in range(num_clients):
        participant_uid = '%030x' % random.randrange(16**30)
        participants.append(participant_uid)

        experiment = numpy.random.choice(exp_info)
        exp_uid = experiment['exp_uid']
        pool_args.append((exp_uid, participant_uid, assert_200, pretest_count, training_count, posttest_count,
                          guard_gap))
    results = pool.map(simulate_one_client, pool_args)

    for result in results:
        print result

    test_utils.getModel(exp_uid, app_id, supported_alg_ids, alg_list)


def simulate_one_client(input_args):
    """
    method to simulate client behavior
    :param input_args: list(object): the input arguments
    :return list of statistics regarding client simulation
    """
    exp_uid, participant_uid, assert_200, pretest_count, training_count, posttest_count, guard_gap = input_args
    # count for instruction questions
    introduction_instructions_count = 2
    pretest_instructions_count = 1
    training_instructions_count = 1
    posttest_instructions_count = 1
    # total number of questions
    total_pulls = pretest_count + training_count + posttest_count
    guard_count = total_pulls / guard_gap
    total_pulls = total_pulls + guard_count + introduction_instructions_count + pretest_instructions_count + \
        training_instructions_count + posttest_instructions_count

    getQuery_times = []
    processAnswer_times = []
    for t in range(total_pulls):
        print "Participant {1} has taken {0} pulls".format(t, participant_uid)
        # test POST getQuery #
        widget = True
        getQuery_args_dict = {'args': {'participant_uid': participant_uid,
                                       'widget': widget},
                              'exp_uid': exp_uid}

        query_dict, dt = test_utils.getQuery(getQuery_args_dict)
        getQuery_times += [dt]

        if widget:
            query_dict = query_dict['args']

        query_uid = query_dict['query_uid']
        same = query_dict['same']
        ques_type = query_dict['ques_type']
        ques_count = query_dict['ques_count']
        total_ques_count = query_dict['total_ques_count']
        molecules = query_dict['target_indices']

        #  print targets
        '''
        for target in molecules:

            print 'here', target['label']
            if target['label'] == 'mol1':
                index_left = target['target_id']
            elif target['label'] == 'mol2':

                index_right = target['target_id']
        '''
        index_left = molecules[0]
        index_right = molecules[1]

        ts = test_utils.response_delay()
        # sleep for a bit to simulate response time

        if ques_type == 'instruction':
            target_winner = 1
        else:
            target_winner = same            # just returns the correct answer

        response_time = time.time() - ts

        # test POST processAnswer
        processAnswer_args_dict = {}
        processAnswer_args_dict["exp_uid"] = exp_uid
        processAnswer_args_dict["args"] = {}
        processAnswer_args_dict["args"]["query_uid"] = query_uid
        processAnswer_args_dict["args"]["target_winner"] = target_winner
        processAnswer_args_dict["args"]["participant_uid"] = exp_uid + '_' + participant_uid  # next appends exp_uid
        # with participant_uid
        processAnswer_args_dict["args"]['response_time'] = response_time

        processAnswer_json_response, dt = test_utils.processAnswer(processAnswer_args_dict)
        print 'Here', same, ques_type, ques_count, total_ques_count
        processAnswer_times.append(dt)

    r = test_utils.format_times(getQuery_times, processAnswer_times, total_pulls, participant_uid)
    return r


if __name__ == '__main__':
    test_api()
    #  test_api(assert_200=False, num_objects=5, desired_dimension=2,
             #  total_pulls_per_client=100, num_experiments=1,
             #  num_clients=5, delta=0.01)
