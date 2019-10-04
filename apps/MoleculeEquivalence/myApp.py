"""
the main app file

@author: Ayon
"""
import next.apps.AltDescTargetManager
from apps.MoleculeEquivalence.algs.Utils import parameters


class MyApp:
    """class for the MoleculeEquivalence app"""

    # keys in dictionary; defined here so in only one place and easy changing
    alg_list_key = 'alg_list'
    alg_label_key = 'alg_label'
    participant_count_key = 'participant_count'

    def __init__(self, db):
        """:param db: the database object"""
        self.app_id = 'MoleculeEquivalence'
        self.TargetManager = \
            next.apps.AltDescTargetManager.AltDescTargetManager(db)

    def initExp(self, butler, init_algs, args):
        """
        method to initialize the experiment
        :param butler: Butler, the butler
        :param init_algs: the list of algorithms to initialize
        :param args: dict, the input arguments
        :return the arguments
        """
        exp_uid = butler.exp_uid

        if 'targetset' in args['targets'].keys():
            n = len(args['targets']['targetset'])
            self.TargetManager.set_targetset(exp_uid,
                                             args['targets']['targetset'])
        else:
            n = args['targets']['n']
        args['n'] = n
        del args['targets']

        # get the pretest, training and posttest questions count along with
        # the gap between guard questions forward them to the algorithms
        alg_data = {}
        algorithm_keys = ['pretest_count', 'training_count', 'posttest_count',
                          'guard_gap']
        for key in algorithm_keys:
            if key in args:
                alg_data[key] = args[key]

        # calculate the number of questions to show
        num_tries = args['pretest_count'] + args['training_count'] + \
            args['posttest_count']

        # calculate
        guard_count = num_tries // args['guard_gap']
        num_tries = num_tries + guard_count + \
            parameters.introduction_instructions_count + \
            parameters.pretest_instructions_count + \
            parameters.training_instructions_count + \
            parameters.posttest_instructions_count

        args['num_tries'] = num_tries

        # get pretest, training and posttest file names and add them to the
        # alg data
        alg_list = args[self.alg_list_key]
        alg_data[self.alg_list_key] = str(alg_list)

        # initialize the participant count
        butler.other.set(key=self.participant_count_key, value=0)

        # calls initExp from algs
        init_algs(alg_data)
        return args

    def getQuery(self, butler, alg, args):
        """
        method to generate a new query for the participant
        :param butler: Butler, the butler
        :param alg: function pointer for the algorithm getQuery
        :param args: dict, the arguments
        :return dict(string, objects), inputs for the widgets as specified in
        the yaml file
        """
        mol1_index = 0
        mol2_index = 1
        same_index = 2
        ques_type_index = 3
        ques_count_index = 4
        total_ques_count_index = 5
        highlight_index1, highlight_index2 = 6, 7

        exp_uid = butler.exp_uid
        # get the participant_uid to send to the front end
        participant_uid = args['participant_uid']

        # get a specific question for this participant
        alg_response = alg({'participant_uid': participant_uid})

        ques_type = alg_response[ques_type_index]

        highlight1, highlight2 = '', ''

        if ques_type == parameters.instruction_key or ques_type == parameters.terms_key:
            mol1 = alg_response[mol1_index]
            mol2 = alg_response[mol2_index]
        else:
            mol1 = self.TargetManager.get_target_item_alt_desc(
                exp_uid, alg_response[mol1_index]
                )
            mol2 = self.TargetManager.get_target_item_alt_desc(
                exp_uid, alg_response[mol2_index]
                )

            # The highlights
            if alg_response[highlight_index1] != '':
                highlight1 = self.TargetManager.get_target_item_alt_desc(
                    exp_uid, alg_response[highlight_index1]
                )
            else:
                highlight1 = mol1

            if alg_response[highlight_index2] != '':
                highlight2 = self.TargetManager.get_target_item_alt_desc(
                    exp_uid, alg_response[highlight_index2]
                )
            else:
                highlight2 = mol2

            mol1['label'] = 'mol1'
            mol2['label'] = 'mol2'

        same = alg_response[same_index]

        ques_count = alg_response[ques_count_index]
        total_ques_count = alg_response[total_ques_count_index]

        return {'target_indices': [mol1, mol2], 'same': same,
                'ques_type': ques_type, 'ques_count': ques_count,
                'total_ques_count': total_ques_count,
                'highlights': [highlight1, highlight2]}

    def processAnswer(self, butler, alg, args):
        """
        method to process the answer submitted by the participant
        :param butler: Butler, the butler
        :param alg: funciton pointer for the algorithm process answer
        :param args: dict, the arguments
        :return dict(key, object): the target chosen by the participant and
        the participant uid
        """
        query = butler.queries.get(uid=args['query_uid'])

        target_winner = args['target_winner']
        participant_uid = args['participant_uid']
        butler.experiment.increment(key='num_reported_answers_for_' +
                                    query['alg_label'])

        # this is a call to the algorithm processAnswer method
        alg({'target_winner': target_winner,
             'participant_uid': participant_uid})

        return {'target_winner': target_winner,
                'participant_uid': participant_uid}

    def getModel(self, butler, alg, args):
        """
        returns the current model. stub in our case.
        :param butler: Butler, the butler
        :param alg: function pointer to algorithm getModel
        :param args: dict, the arguments
        :return the output of the algorithms getModel method
        """
        return alg()

    def chooseAlg(self, butler, alg_list, args):
        """
        method to choose which algorithm a new participant gets assigned to
        we currently assign participants to algorithms in a round robin way
        :param butler: Butler, the butler
        :alg_list: list(dict), list of algorithms
        :args: dict, the arguments
        :return the algorithm to assign to this participant
        """
        # choose the algorithms in a round robin fashion
        participant_count = \
            butler.other.increment(key=self.participant_count_key)
        alg_index = participant_count % len(alg_list)
        return alg_list[alg_index]
