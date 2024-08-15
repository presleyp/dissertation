import numpy as np

def exclude_duplicates(df):
    before = len(set(df.WorkerID))
    dedup = df.drop_duplicates(['WorkerID', 'PageID'])
    after = len(set(dedup.WorkerID))
    print "Number of duplicate participants dropped"
    print before - after
    return dedup

def exclude_debug(df):
    debug = [worker for worker in set(df.WorkerID) if worker.startswith('debug')]
    workers = df[~df.WorkerID.isin(debug)]
    print "Number of participants in data that were debuggers"
    print len(debug)
    return workers

def exclude_minors(df, age_question_id):
    age_rows = df[df.PageID == age_question_id]
    age_rows['Minor'] = age_rows.apply(lambda row: row['SelectedText'][0] < 18, axis = 1)
    minor_rows = age_rows[age_rows.Minor == True]
    minor_workers = minor_rows.WorkerID
    workers = df[~df.WorkerID.isin(minor_workers)]
    print "Number of minors dropped"
    print len(minor_workers)
    return workers

def parse_selected_text(row):
    if type(row['SelectedText']) == list:
        return row['SelectedText'][0] != ''
    else:
        return False

def exclude_bot_speed(test):
    bot_speed = set(test[test['ReactionTime'] < 50]['WorkerID'])
    humans = test[~test.WorkerID.isin(bot_speed)]
    print "Number of participants dropped for being unhumanly fast"
    print len(bot_speed)
    return humans

def parse_selected_position(row):
    if type(row['SelectedPosition']) == list:
        return row['SelectedPosition'][0]
    else:
        return False

def exclude_one_sided(test):
    test['SelectedPosition'] = test.SelectedPosition.apply(lambda x: x[0])
    worker_groups = test.groupby('WorkerID', as_index = False)
    aggregation = worker_groups.agg({'SelectedPosition': np.mean})
    one_side = set(aggregation[aggregation['SelectedPosition'] > 0.9]['WorkerID'])\
                | set(aggregation[aggregation['SelectedPosition'] < 0.1]['WorkerID'])
    attentive = test[~test.WorkerID.isin(one_side)]
    print "Number of participants dropped for favoring one option position"
    print len(one_side)
    return attentive

