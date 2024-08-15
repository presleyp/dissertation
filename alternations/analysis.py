import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from analysis_utils import *

# Chose to Violate Place Assimilation ~ Permutation + Segment + Item + Subject
data = None
with open('pilot_may5.json', 'r') as f:
    data = f.read()

js = json.loads(data)
df = pd.DataFrame(js)
df['ReactionTime'] = df.EndTime - df.StartTime

### Exclusions
current = exclude_old(df, '3.0')
current = exclude_before(current, 2015, 5, 7)
old_workers = set(current[current.PageType == 'Lexical'].WorkerID)
current = current[~current.WorkerID.isin(old_workers)]
workers = exclude_debug(current)
# dedup = exclude_duplicates(workers)
non_minors = exclude_minors(workers, '569')
questions = non_minors[pd.notnull(non_minors.OptionOrder)]
questions['Answered'] = questions.apply(parse_selected_text, axis = 1)
answered = questions[questions['Answered'] == True]
humans = exclude_bot_speed(answered)

humans['SelectedText'] = humans.SelectedText.apply(lambda x: x[0])

exposure = humans[humans.PageType == 'Exposure']
blank_exposure = set(exposure[exposure.SelectedText == ''].WorkerID)
print 'Number of participants excluded for skipping exposure questions:'
print len(blank_exposure)

did_exposure = humans[~humans.WorkerID.isin(blank_exposure)]
train_test = did_exposure[did_exposure.PageType.isin(['Wug', 'Catch', 'Test'])]
# humans['SelectedPosition'] = humans.SelectedPosition.apply(lambda x: x[0])
attentive = exclude_one_sided(train_test)
# read: language answers, strategy answers

'Workers by max iteration'
print attentive.groupby('WorkerID').Iteration.aggregate(max)

#TODO
learned = exclude_unlearned(attentive, 6)
print '''Number of participants included:'''
print len(set(learned.WorkerID))
learned_subj = learned.groupby('WorkerID')
print learned_subj.Permutation.aggregate(np.mean)


learned_pt = learned.groupby('PageType')
print 'learned'
print learned_pt['ReactionTime'].aggregate(np.mean)
print set(learned.WorkerID)
unlearned = examine_unlearned(attentive, 4)
unlearned_pt = unlearned.groupby('PageType')
print "didn't learn"
print unlearned_pt['ReactionTime'].aggregate(np.mean)
unlearned_subj = unlearned.groupby('WorkerID')
print unlearned_subj.Permutation.aggregate(np.mean)

learned['TrainedOn'] = learned.Permutation.apply(lambda x: 'voice' if x == 0 else 'place')
test = learned[learned.PageType == 'Test']
test = test[test.Segment != '']
catch = learned[learned.PageType == 'Catch']

# add columns for analyzing test questions
test['SelectedViolation'] = test.apply(lambda row: row['Violates'][row['SelectedPosition']], axis = 1)
test['ViolatesPlace'] = test.SelectedViolation.apply(lambda x: x == u'place')

def get_place_position(row):
    return row['Violates'].index('place')

test['PlacePosition'] = test.apply(get_place_position, axis = 1)

# add columns for analyzing catch questions
def chose_right(row):
    language = 'pilot_voice' if row['Permutation'] == 0 else 'pilot_nasal'
    should_alternate = 'T' if row['Condition'] == language else 'F'
    did_alternate = 'T' if row['Alternates'][row['SelectedPosition']] == 'T' else 'F'
    return did_alternate == should_alternate

catch['Right'] = catch.apply(chose_right, axis = 1)
catch['Alternates'] = catch.apply(lambda row: row['Alternates'][row['SelectedPosition']], axis = 1)

# data = None
# #TODO change from pilot
# with open('april2_results.json', 'r') as f:
#     data = f.read()
# js = json.loads(data)
# df = pd.DataFrame(js)
# dedup = df.drop_duplicates(['WorkerID', 'PageID'])
# debug = [worker for worker in set(dedup.WorkerID) if worker.startswith('debug')]
# workers = dedup[~dedup.WorkerID.isin(debug)]
# test_and_pilot = attentive[pd.notnull(attentive.Segment)]
# # test_and_pilot.SelectedPosition = test_and_pilot.SelectedPosition.apply(lambda x: x[0])
# test_and_pilot['ReactionTime'] = test_and_pilot.EndTime - test_and_pilot.StartTime
# PageType : Catch, Test
# test_and_pilot['TrainedOn'] = test_and_pilot.Permutation.apply(lambda x: 'voice' if x == 0 else 'place')
# pilot = test_and_pilot[pd.notnull(test_and_pilot.Alternates)]
# test_and_pilot.BlockIDs = test_and_pilot.BlockIDs.apply(lambda x: x[0])
# test = test_and_pilot[test_and_pilot.BlockIDs == u'576']



# for worker in set(test.WorkerID):
#     print worker
#     print set(test[test.WorkerID == worker].Permutation)
#     print len(test[test.WorkerID == worker])

# exclude people who didn't take long enough, picked all
# one side, didn't answer language questions to my liking
# read: language answers, strategy answers
# # missed_catch = set(test[test['SelectedType'] == 'catch-bad']['WorkerID'])
# bot_speed = set(test[test['ReactionTime'] < 50]['WorkerID'])
# worker_groups = test.groupby('WorkerID', as_index = False)
# aggregation = worker_groups.agg({'SelectedPosition': np.mean})
# one_side = set(aggregation[aggregation['SelectedPosition'] > 0.9]['WorkerID']) | set(aggregation[aggregation['SelectedPosition'] < 0.1]['WorkerID'])
# # exclude = missed_catch.union(bot_speed, one_side)
# exclude = bot_speed.union(one_side)
# test = test[~test.WorkerID.isin(exclude)]


# include just the right columns
to_analyze = pd.DataFrame({
    'ViolatesPlace': test.ViolatesPlace,
    'Permutation': test.Permutation,
    'TrainedOn': test.TrainedOn,
    'Segment': test.Segment,
    'Subject': test.WorkerID,
    'Item': test.PageID,
    'PlacePosition': test.PlacePosition,
    'ReactionTime': test.ReactionTime,
    'TrialNumber': test.TrialNumber})

# graph answers to pilot (catch) questions at end
# catch.groupby('Permutation')['Permutation'].count().plot(kind = 'bar')
# plt.show()
# right_answer_counts = catch.groupby('Right')['Right'].count()
# right_answer_counts.plot(kind = 'bar')
# plt.show()
# language_groups = catch.groupby(['WorkerID', 'TrainedOn', 'Condition', 'Alternates'])
# lang_group_counts = language_groups['Alternates'].count()
# lang_group_counts.plot(kind = 'bar')
# plt.show()
catch_groups = catch.groupby(['TrainedOn', 'Alternates'])
catch_counts = catch_groups.count()
catch_counts['Alternates'].plot(kind = 'bar')
plt.show()

# make graphs #TODO graph results and reaction times
# chose_violate_place = to_analyze[to_analyze.ViolatesPlace == True]
groups = to_analyze.groupby(['TrainedOn', 'ViolatesPlace'])
counts = groups.count()
print counts
counts['ViolatesPlace'].plot(kind = 'bar')
plt.show()



# reaction times
# time_groups = catch.groupby(['Condition', 'Permutation', 'Right'])
# mean_times = time_groups['ReactionTime'].aggregate(np.mean)
# # sd_times = time_groups['ReactionTime'].aggregate(np.sd)
# mean_times.plot(kind = 'bar')
# plt.show()

# write to csv
to_analyze.to_csv('alternations_dataframe.csv')
