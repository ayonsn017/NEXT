import next.utils as utils
from next.apps.SimpleTargetManager import SimpleTargetManager

class AltDescTargetManager(SimpleTargetManager):

    def get_target_item_alt_desc(self, exp_uid, alt_description):
        """
        Get a target from the targetset. Th
        """
        # Get an individual target form the DB given exp_uid and index
        try:
            got_target = self.db.get_docs_with_filter(self.bucket_id,{'exp_uid': exp_uid, 'alt_description': alt_description})
        except:
            raise Exception("Failed to get_target_item given index")
        try:
            # targets are something else
            target = got_target.pop(0)
        except:
            # targets are numbers
            target = {'target_id':target_id,
                      'primary_description':str(target_id),
                      'primary_type':'text',
                      'alt_description':str(target_id),
                      'alt_type':'text'}
    
            
        # This line might fail; only tested under the except: statement above
        #del target['exp_uid']
        return target
