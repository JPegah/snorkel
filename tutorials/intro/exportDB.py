import sqlite3
import json

def get_trend_span(tr_id, c):
    pair = c.execute('SELECT sentence_id, char_start, char_end  FROM span p WHERE p.id=\'' + str(tr_id) + '\';')
    for p in pair:
        return {'sent_id':p[0], 'start_char':p[1], 'end_char':p[2]}

def get_sentence(sent_id, c):
    pair = c.execute('SELECT document_id, position FROM sentence p WHERE p.id=\'' + str(sent_id) + '\';')
    for p in pair:
        return {'doc_id': p[0], 'pos_id':p[1]}

# I will return pair. each pair id is: doc_id:sentence_id:
def get_tr_ind_pair_info(pair_id, c):
    pair = c.execute('SELECT tr_id, ind_id FROM indicator p WHERE p.id=\'' + str(pair_id)+'\';')
    # want to look and tr_id , in_id --> it makes a span
    for p in pair:
        tr_id, ind_id = p[0], p[1]
        tr = get_trend_span(tr_id, c)
        ind = get_trend_span(ind_id, c)
        # get the doc info here
        doc = get_sentence(tr['sent_id'], c)
        return tr, ind, doc

def process_db():
    out_file = open('trends.tsv', mode='w')
    connection = sqlite3.connect('snorkel.db')
    c = connection.cursor()
    pr = c.execute('SELECT * FROM indicator')
    doc_ids =[]
    for p in pr:
        doc_ids.append(p[0])
    for p in doc_ids:
        tr, ind, doc = get_tr_ind_pair_info(p, c)
        if int(doc['doc_id']) > 20:
            d = str(doc['doc_id']) + ':' + str(doc['pos_id'])
            out_file.write(d + ":span:" + str(tr['start_char']) + ':' + str(tr['end_char']) + '\t')
            out_file.write(d + ":span:" + str(ind['start_char']) + ':' + str(ind['end_char']) + '\n')
        continue

process_db()

