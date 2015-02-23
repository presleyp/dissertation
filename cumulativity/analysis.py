import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

data = None
with open('cumulativity_results.json', 'r') as f:
    data = f.read()
js = json.loads(data)
df = pd.DataFrame(js)
dedup = df.drop_duplicates(['WorkerID', 'PageID'])
debug = [worker for worker in set(dedup.WorkerID) if worker.startswith('debug')]
workers = dedup[~dedup.WorkerID.isin(debug)]
questions = workers[pd.notnull(workers.OptionOrder)]
test = questions[pd.notnull(questions.Condition)]
test.SelectedPosition = test.SelectedPosition.apply(lambda x: x[0])
test['SelectedType'] = test.apply(lambda row: row['type'][row['SelectedPosition']], axis = 1)
test['Chosen'] = test.apply(lambda row: row['SelectedType'] if row['SelectedType'] != 'test' else
        row['Condition'], axis = 1)
for cond in set(test.Condition):
    print cond
    print len(test[test.Chosen == cond])
for worker in set(test.WorkerID):
    print worker
    print len(test[test.WorkerID == worker])
for t in set(test.SelectedType):
    print t
    print len(test[test.SelectedType == t])

# fillers are too good - chosen twice as often as tests
# catches work okay
# super preliminary data doesn't give the results i expect, but GG > BG > GB BB
# so they're not too crazy, but look at badness of codas vs onsets

# exclude people who missed catch trials, didn't take long enough, picked all
# one side, didn't answer language questions to my liking
# read: language answers, strategy answers
missed_catch = set(test[test['SelectedType'] == 'catch-bad']['WorkerID'])
test['ReactionTime'] = test.EndTime - test.StartTime
bot_speed = set(test[test['ReactionTime'] < 50]['WorkerID'])
worker_groups = test.groupby('WorkerID', as_index = False)
aggregation = worker_groups.agg({'SelectedPosition': np.mean})
one_side = set(aggregation[aggregation['SelectedPosition'] > 0.9]['WorkerID']) | set(aggregation[aggregation['SelectedPosition'] < 0.1]['WorkerID'])
exclude = missed_catch.union(bot_speed, one_side)
test = test[~test.WorkerID.isin(exclude)]

# remove catch trials
test = test[~test['SelectedType'].isin(['catch-good', 'catch-bad'])]

# make useful columns
test['SelectedTest'] = test.apply(lambda row: row['SelectedType'] == 'test', axis = 1)

def get_filler(row):
    filler_index = row['type'].index('filler')
    return row['OptionTexts'][filler_index]

test['Filler'] = test.apply(get_filler, axis = 1)

def get_test_position(row):
    return row['type'].index('test')

test['TestPosition'] = test.apply(get_test_position, axis = 1)

# include just the right columns
to_analyze = pd.DataFrame({
    'SelectedTest': test.SelectedTest,
    # 'OnsetViolation': test.OnsetViolation,
    # 'CodaViolation': test.CodaViolation,
    'Condition': test.Condition,
    'Subject': test.WorkerID,
    # 'Item': test.ItemID,
    'Filler': test.Filler,
    # 'Vowel': test.Vowel,
    'TrialNumber': test.TrialNumber,
    'Version': test.Version,
    'TestPosition': test.TestPosition})

# make graphs
chose_test = to_analyze[to_analyze.SelectedTest == True]
cond_groups = chose_test.groupby(['Condition', 'SelectedTest'])
chosen_counts = cond_groups.count()
chosen_counts['Condition'].plot(kind = 'bar')
plt.show()

# write to csv
to_analyze.to_csv('cumulativity_dataframe.csv')
