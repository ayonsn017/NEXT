import json
import next.utils as utils
import next.apps.AltDescTargetManager

class MyApp:
    def __init__(self,db):
        self.app_id = 'MoleculesPoolBasedTripletMDS'
        self.TargetManager = next.apps.AltDescTargetManager.AltDescTargetManager(db)

    def initExp(self, butler, init_algs, args):
        exp_uid = butler.exp_uid

        if 'targetset' in args['targets'].keys():
            n  = len(args['targets']['targetset'])
            self.TargetManager.set_targetset(exp_uid, args['targets']['targetset'])
        else:
            n = args['targets']['n']
        args['n'] = n
        del args['targets']

        alg_data = {}
        algorithm_keys = ['n', 'd', 'pretest_count', 'training_count', 'posttest_count']
        for key in algorithm_keys:
            if key in args:
                alg_data[key]=args[key]

        # calculate the number of questions to show
        num_tries = args['pretest_count']
        num_tries += args['training_count']
        num_tries += args['posttest_count']

        args['num_tries'] = num_tries

        # calls initExp from algs
        init_algs(alg_data)
        return args

    def getQuery(self, butler, alg, args):
        alg_response = alg()
        exp_uid = butler.exp_uid
        center  = self.TargetManager.get_target_item(exp_uid, 0)
        left  = self.TargetManager.get_target_item_alt_desc(exp_uid, alg_response[0])
        right  = self.TargetManager.get_target_item_alt_desc(exp_uid, alg_response[1])
        center['label'] = 'center'
        left['label'] = 'left'
        right['label'] = 'right'

        return {'target_indices':[center, left, right]}

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




