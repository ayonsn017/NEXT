import time
import numpy.random
from apps.MoleculesPoolBasedTripletMDS.algs.RandomTrainTest import utilsMDS
import next.utils as utils

class RandomTrainTest:
  pretest_count_key = 'pretest_count'
  training_count_key = 'training_count'
  posttest_count_key = 'posttest_count'
  num_reported_answers_key = 'num_reported_answers'
  pretest_key = 'pretest'
  training_key = 'training'
  posttest_key = 'posttest'
  participant_answers_count_dict_key = 'participant_answers_count_dict'
  def initExp(self,butler, n, d, pretest_count, training_count, posttest_count):
    X = numpy.random.randn(n,d)
    butler.algorithms.set(key='n',value= n)
    butler.algorithms.set(key='d',value= d)
    butler.algorithms.set(key='pretest_count', value=pretest_count)
    butler.algorithms.set(key='training_count', value=training_count)
    butler.algorithms.set(key='posttest_count', value=posttest_count)
    butler.algorithms.set(key='X',value= X.tolist())
    butler.algorithms.set(key='num_reported_answers', value=0)  # the number of total questions answered for this algorithm
    butler.algorithms.set(key=self.participant_answers_count_dict_key, value={}) # dictionary to store the number of questions the participant has answered
    return True


  def getQuery(self, butler, participant_uid):
    n = numpy.array(butler.algorithms.get(key='n'))
    num_reported_answers = butler.algorithms.get(key='num_reported_answers')

    participant_answers_count_dict = butler.algorithms.get(key=self.participant_answers_count_dict_key)

    if participant_uid not in participant_answers_count_dict:
      participant_answers_count_dict[participant_uid] = 0
      num_reported_answers = 0
    else:
      num_reported_answers = participant_answers_count_dict[participant_uid]

    pretest_count = butler.algorithms.get(key=self.pretest_count_key)
    training_count = butler.algorithms.get(key=self.training_count_key)
    posttest_count = butler.algorithms.get(key=self.posttest_count_key)

    if num_reported_answers < pretest_count:
      mol1, mol2, same = utilsMDS.getRandomQuery()
      ques_type = self.pretest_key
    elif num_reported_answers >= pretest_count and num_reported_answers < pretest_count + training_count:
      mol1, mol2, same =  utilsMDS.get_random_training_query()
      ques_type = self.training_key
    elif num_reported_answers >= pretest_count + training_count:
      mol1, mol2, same = utilsMDS. getRandomQuery()
      ques_type = self.posttest_key

    participant_answers_count_dict[participant_uid] = num_reported_answers + 1    
    butler.algorithms.set(key=self.participant_answers_count_dict_key, value=participant_answers_count_dict)  
    return [mol1, mol2, same, ques_type]

  def processAnswer(self,butler,center_id,left_id,right_id,target_winner):
    '''
    if left_id==target_winner:
      q = [left_id,right_id,center_id]
    else:
      q = [right_id,left_id,center_id]
    butler.algorithms.append(key='S',value=q)
    n = butler.algorithms.get(key='n')
    '''
    # increment the number of questions this participant has seen
    num_reported_answers = butler.algorithms.increment(key='num_reported_answers')
    '''
    if num_reported_answers % int(n) == 0:
      butler.job('full_embedding_update', {}, time_limit=30)
    else:
      butler.job('incremental_embedding_update', {},time_limit=5)
    '''
    # must return this true value to record stats like time
    return True


  def getModel(self, butler):
    return butler.algorithms.get(key=['X','num_reported_answers'])


  def incremental_embedding_update(self,butler,args):
    S = butler.algorithms.get(key='S')
    X = numpy.array(butler.algorithms.get(key='X'))
    # set maximum time allowed to update embedding
    t_max = 1.0
    epsilon = 0.01 # a relative convergence criterion, see computeEmbeddingWithGD documentation
    # take a single gradient step
    t_start = time.time()
    X,emp_loss_new,hinge_loss_new,acc = utilsMDS.computeEmbeddingWithGD(X,S,max_iters=1)
    k = 1
    while (time.time()-t_start<0.5*t_max) and (acc > epsilon):
      X,emp_loss_new,hinge_loss_new,acc = utilsMDS.computeEmbeddingWithGD(X,S,max_iters=2**k)
      k += 1
    butler.algorithms.set(key='X',value=X.tolist())

  def full_embedding_update(self,butler,args):
    n = butler.algorithms.get(key='n')
    d = butler.algorithms.get(key='d')
    S = butler.algorithms.get(key='S')

    X_old = numpy.array(butler.algorithms.get(key='X'))

    t_max = 5.0
    epsilon = 0.01 # a relative convergence criterion, see computeEmbeddingWithGD documentation

    emp_loss_old,hinge_loss_old = utilsMDS.getLoss(X_old,S)
    X,tmp = utilsMDS.computeEmbeddingWithEpochSGD(n,d,S,max_num_passes=16,epsilon=0,verbose=False)
    t_start = time.time()
    X,emp_loss_new,hinge_loss_new,acc = utilsMDS.computeEmbeddingWithGD(X,S,max_iters=1)
    k = 1
    while (time.time()-t_start<0.5*t_max) and (acc > epsilon):
      X,emp_loss_new,hinge_loss_new,acc = utilsMDS.computeEmbeddingWithGD(X,S,max_iters=2**k)
      k += 1
    emp_loss_new,hinge_loss_new = utilsMDS.getLoss(X,S)
    if emp_loss_old < emp_loss_new:
      X = X_old
    butler.algorithms.set(key='X',value=X.tolist())



