import json
import next.utils as utils
import next.apps.AltDescTargetManager

class MyApp:
    alg_list_key = 'alg_list'
    alg_label_key = 'alg_label'
    pretest_file_key = 'pretest_file'
    training_file_key = 'training_file'
    posttest_file_key = 'posttest_file'
    test_int = 0

    def __init__(self,db):
        self.app_id = 'MoleculesPoolBasedTripletMDS'
        self.TargetManager = next.apps.AltDescTargetManager.AltDescTargetManager(db)

    def initExp(self, butler, init_algs, args):
        exp_uid = butler.exp_uid
        alg_label = butler.alg_label

        if 'targetset' in args['targets'].keys():
            n  = len(args['targets']['targetset'])
            self.TargetManager.set_targetset(exp_uid, args['targets']['targetset'])
        else:
            n = args['targets']['n']
        args['n'] = n
        del args['targets']

        alg_data = {}
        algorithm_keys = ['pretest_count', 'training_count', 'posttest_count']
        for key in algorithm_keys:
            if key in args:
                alg_data[key]=args[key]

        # calculate the number of questions to show
        num_tries = args['pretest_count']
        num_tries += args['training_count']
        num_tries += args['posttest_count']

        args['num_tries'] = num_tries

        # get pretest, training and posttest file names
        alg_list = args[self.alg_list_key]

        # log data
        log_fname = 'log.txt'
        log_file = open(log_fname, 'a')
        if alg_label is None:
            log_file.write('Original Label: none' + '\n')
        else:
            log_file.write('Original Label: ' + alg_label  + '\n')

        log_file.write(str(butler) + '\n')


        for alg_item in alg_list:
            #log_file.write(str(alg_item) + '\n')
            if alg_item[self.alg_label_key] == alg_label:
                alg_data[pretest_file_key] = alg_item[self.pretest_file_key]
                alg_data[training_file_key] = alg_item[self.training_file_key]
                alg_data[posttest_file_key] = alg_item[self.posttest_file_key]
                break
        log_file.close()
        
        alg_data['pretest_file'] =str(self.test_int)
        self.test_int += 1
        alg_data['training_file'] = 'sdfasf'
        alg_data['posttest_file'] = 'asfdasdf'

        # calls initExp from algs
        init_algs(alg_data)
        return args

    def getQuery(self, butler, alg, args):
        exp_uid = butler.exp_uid
        participant_uid = args['participant_uid']
        alg_response = alg({'participant_uid':participant_uid})
        mol1  = self.TargetManager.get_target_item_alt_desc(exp_uid, alg_response[0])
        mol2  = self.TargetManager.get_target_item_alt_desc(exp_uid, alg_response[1])
        same = alg_response[2]
        ques_type = alg_response[3]
        mol1['label'] = 'mol1'
        mol2['label'] = 'mol2'

        return {'target_indices':[mol1, mol2], 'same': same, 'ques_type': ques_type, 'participant_uid': participant_uid}

    def processAnswer(self, butler, alg, args):
        
        query = butler.queries.get(uid=args['query_uid'])
        '''
        targets = query['target_indices']
        for target in targets:
            if target['label'] == 'center':
                center_id = target['target_id']
            elif target['label'] == 'left':
                left_id = target['target_id']
            elif target['label'] == 'right':
                right_id = target['target_id']
        '''
        target_winner = args['target_winner']
        participant_uid = args['participant_uid']
        # make a getModel call ~ every n/4 queries - note that this query will NOT be included in the predict
        experiment = butler.experiment.get()
        num_reported_answers = butler.experiment.increment(key='num_reported_answers_for_' + query['alg_label'])
        
        '''
        n = experiment['args']['n']
        q = [left_id, right_id,center_id] if target_winner==left_id else [right_id, left_id,center_id]
        '''

        # this is a call to the algorithm processAnswer method
        alg({'left_id':0, 'right_id':1, 'center_id':2, 'target_winner':target_winner})
        
        q= [0, 1, 2]

        return {'target_winner':target_winner, 'q':q}

    def getModel(self, butler, alg, args):
        return alg()




