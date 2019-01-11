from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *

import pandas as pd
from snorkel.models import StableLabel
from snorkel.db_helpers import reload_annotator_labels

FPATH = 'data/automated_labels.tsv'


    
def load_external_trend_labels(session, candidate_class, annotator_name='gold'):
    gold_labels = pd.read_csv(FPATH, sep="\t")
    for index, row in gold_labels.iterrows():    

        # We check if the label already exists, in case this cell was already executed
        context_stable_ids = row['tr']
        #print(context_stable_ids)
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)
        #print(query.count())
#         for x in query.:
#            print(x)
#         print(query.all())
        if query.count() == 0:
            print('********************************')
            print('adding gold labels for this row')
            print(row)
            session.add(StableLabel(
                context_stable_ids=context_stable_ids,
                annotator_name=annotator_name,
                value=row['label']))
        else:
            print('----------------------------')
            print('stable label is found for this one!: ')
            print(row)
            
            
                    
    # Commit session
    session.commit()
    # Reload annotator labels
    reload_annotator_labels(session, candidate_class, annotator_name, split=1, filter_label_split=False)
    reload_annotator_labels(session, candidate_class, annotator_name, split=2, filter_label_split=False)

def load_external_tr_ind_labels(session, candidate_class, annotator_name='gold'):
    gold_labels = pd.read_csv(FPATH, sep="\t")
    for index, row in gold_labels.iterrows():    
        # We check if the label already exists, in case this cell was already executed
        context_stable_ids = "~~".join([row['trend'], row['indicator']])
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)
     #   print(row)
      #  print(row['label']
        if query.count() == 0:
            session.add(StableLabel(
                context_stable_ids=context_stable_ids,
                annotator_name=annotator_name,
                value=row['label']))

    # Commit session
    session.commit()

    # Reload annotator labels
    reload_annotator_labels(session, candidate_class, annotator_name, split=1, filter_label_split=False)
    reload_annotator_labels(session, candidate_class, annotator_name, split=2, filter_label_split=False)