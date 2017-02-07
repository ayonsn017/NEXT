import json
import next.utils as utils
import next.apps.AltDescTargetManager
from apps.MoleculeEquivalence.algs.Utils import parameters

class MyApp:
    alg_list_key = 'alg_list'
    alg_label_key = 'alg_label'
    alg_counts_key = 'alg_counts'
    assign_alg_lock_name = 'assign_alg_lock'
    pretest_file_key = 'pretest_file'
    training_file_key = 'training_file'
    posttest_file_key = 'posttest_file'

    def __init__(self,db):
        self.app_id = 'MoleculeEquivalence'
        self.TargetManager = next.apps.AltDescTargetManager.AltDescTargetManager(db)
        self.alg_counts = None

    def initExp(self, butler, init_algs, args):
        exp_uid = butler.exp_uid
        
        if 'targetset' in args['targets'].keys():
            n  = len(args['targets']['targetset'])
            self.TargetManager.set_targetset(exp_uid, args['targets']['targetset'])
        else:
            n = args['targets']['n']
        args['n'] = n
        del args['targets']

        # get the pretest, training and posttest questions count and forward them to the algorithms
        alg_data = {}
        algorithm_keys = ['pretest_count', 'training_count', 'posttest_count']
        for key in algorithm_keys:
            if key in args:
                alg_data[key]=args[key]

        # calculate the number of questions to show
        num_tries = args['pretest_count']
        num_tries += args['training_count']
        num_tries += args['posttest_count']

        num_tries += parameters.introduction_instructions_count
        num_tries += parameters.pretest_instructions_count
        num_tries += parameters.training_instructions_count
        num_tries += parameters.posttest_instructions_count

        args['num_tries'] = num_tries

        # get pretest, training and posttest file names and add them to the alg data
        alg_list = args[self.alg_list_key]
        alg_data[self.alg_list_key] = str(alg_list)

        # calls initExp from algs
        init_algs(alg_data)
        return args

    def getQuery(self, butler, alg, args):

        mol1_index = 0
        mol2_index = 1
        same_index = 2
        ques_type_index = 3
        ques_count_index = 4
        total_ques_count_index = 5

        exp_uid = butler.exp_uid
        participant_uid = args['participant_uid'] # get the participant_uid to send to the front end
        
        alg_response = alg({'participant_uid':participant_uid}) # get a specific question for this participant

        ques_type = alg_response[ques_type_index]

        if ques_type == parameters.instruction_key:
            mol1 = alg_response[mol1_index]
            mol2 = alg_response[mol2_index]
        else:
            mol1  = self.TargetManager.get_target_item_alt_desc(exp_uid, alg_response[mol1_index])
            mol2  = self.TargetManager.get_target_item_alt_desc(exp_uid, alg_response[mol2_index])
            mol1['label'] = 'mol1'
            mol2['label'] = 'mol2'

        same = alg_response[same_index]
        
        ques_count = alg_response[ques_count_index]
        total_ques_count = alg_response[total_ques_count_index]

        return {'target_indices':[mol1, mol2], 'same': same, 'ques_type': ques_type, 'participant_uid': participant_uid, 'ques_count': ques_count, 
                     'total_ques_count': total_ques_count }

    def processAnswer(self, butler, alg, args):
                
        query = butler.queries.get(uid=args['query_uid'])

        target_winner = args['target_winner']
        participant_uid = args['participant_uid']
        # make a getModel call ~ every n/4 queries - note that this query will NOT be included in the predict
        experiment = butler.experiment.get()
        num_reported_answers = butler.experiment.increment(key='num_reported_answers_for_' + query['alg_label'])
        

        # this is a call to the algorithm processAnswer method
        alg({'target_winner':target_winner, 'participant_uid':participant_uid})
        
        q= [0, 1, 2]

        return {'target_winner':target_winner, 'q':q}

    def getModel(self, butler, alg, args):
        return alg()

    def chooseAlg(self, butler, alg_list, args):
        """
        method to choose which algorithm a new participant gets assigned to
        we currently assign participants to algorithms in a round robin way
        :param butler: Butler, the butler
        :alg_list: list(dict): list of algorithms
        :args: dict: the arguments
        """
        # acquiring lock before reading any information
        assign_alg_lock = butler.memory.lock(self.assign_alg_lock_name)
        assign_alg_lock.acquire()

        alg_counts = butler.other.get(key=self.alg_counts_key)

        # if this is the first participant in the experiment then initialize the alg_counts
        if alg_counts is None:
            alg_counts = [0] * len(alg_list)

        # find which algorithm has been assigned once less then to its predecessor in the list
        index = -1

        for i in range(1, len(alg_list)):
            if alg_counts[i] < alg_counts[i-1]:
                index = i
                break

        # if every algorithm has been chosen equal number of times then chose the first algorithm
        if index == -1:
            index = 0

        alg_counts[index] = alg_counts[index] + 1
        butler.other.set(key=self.alg_counts_key, value=alg_counts)

        chosen_alg = alg_list[index]

        # releasing lock after updating information
        assign_alg_lock.release()

        return chosen_alg





