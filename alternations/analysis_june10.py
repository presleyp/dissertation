from __future__ import division
import pandas as pd
import math
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
current = exclude_old(df, '7.0') # 6.0 is beginning of real experiment
# current = exclude_before(current, 2015, 5, 13)
# old_workers = set(current[current.PageType == 'Lexical'].WorkerID)
# current = current[~current.WorkerID.isin(old_workers)]
workers = exclude_debug(current)
dedup = exclude_duplicates(workers)
non_minors = exclude_minors(dedup, '569')
# feedback problem fixed now
# feedback = non_minors[non_minors.PageType == 'Feedback']
# plt.hist(feedback.ReactionTime, range = (0, 1000))
# plt.show()
questions = non_minors[pd.notnull(non_minors.OptionOrder)]
questions['Answered'] = questions.apply(parse_selected_text, axis = 1)
answered = questions[questions['Answered'] == True]
humans = exclude_bot_speed(answered)

humans['SelectedText'] = humans.SelectedText.apply(lambda x: x[0])

exposure = humans[humans.PageType == 'Exposure']
# print set(exposure.SelectedText)
blank_exposure = set(exposure[exposure.SelectedText == ''].WorkerID)
print 'Number of participants excluded for skipping exposure questions:'
print len(blank_exposure)

did_exposure = humans[~humans.WorkerID.isin(blank_exposure)]
train_test = did_exposure[did_exposure.PageType.isin(['Wug', 'Catch', 'Test'])]
# humans['SelectedPosition'] = humans.SelectedPosition.apply(lambda x: x[0])
attentive = exclude_one_sided(train_test)
# read: language answers, strategy answers


def exclude_inaccurate(df, criterion):
    # df['Accuracy'] = df.apply(lambda row: row[, axis = 1)
    scores = get_accuracy(df)
    passed = scores[scores.Accuracy > criterion].index
    return (df[df.WorkerID.isin(passed)], df[~df.WorkerID.isin(passed)])

def get_accuracy(df):
    training = df[df.PageType == 'Wug']
    training['Correct'] = training.Correct.apply(lambda x: 1 if x[0] == True else 0)
    scores = training.groupby('WorkerID').aggregate(np.mean)
    df['Accuracy'] = scores.merge(
    return df



# 'Workers by max iteration'
# number_iterations = attentive.groupby('WorkerID').Iteration.aggregate(max)
# # print np.mean(number_iterations)
# attentive['NumberIterations'] = attentive.apply(lambda row:
#         number_iterations[row['WorkerID']], axis = 1)

# learned = exclude_unlearned(attentive, 5)
learned, unlearned = exclude_incorrect(attentive, .8)
print '''Number of participants included:'''
print len(set(learned.WorkerID))
learned_subj = learned.groupby('WorkerID')
# print learned_subj.Permutation.aggregate(np.mean)


# learned_pt = learned.groupby('PageType')
# # print 'learned'
# # print learned_pt['ReactionTime'].aggregate(np.mean)
# # print set(learned.WorkerID)
# unlearned = examine_unlearned(attentive, 5)
# unlearned_pt = unlearned.groupby('PageType')
# # print "didn't learn"
# # print unlearned_pt['ReactionTime'].aggregate(np.mean)
# unlearned_subj = unlearned.groupby('WorkerID')
# print unlearned_subj.Permutation.aggregate(np.mean)

attentive['TrainedOn'] = attentive.Permutation.apply(lambda x: 'Devoicing' if x == 0
        else 'PlaceAssimilation')
# print set(attentive.TrainedOn)
test = attentive[attentive.PageType == 'Test']
catch = attentive[attentive.PageType == 'Catch']


# add columns for analyzing test questions

test['SelectedViolation'] = test.apply(lambda row: row['Violation'][row['SelectedPosition']], axis = 1)
test['BooleanViolation'] = test.SelectedViolation.apply(lambda x: 1 if x == 'True' else 0)
# test['ViolatesPlace'] = test.SelectedViolation.apply(lambda x: x == u'place')

test_groups = test.groupby(['Permutation', 'Violates', 'SelectedViolation'])
# print test_groups['SelectedViolation'].count()

test_0_groups = test[test.Permutation == 0].groupby('Violates')
test_1_groups = test[test.Permutation == 1].groupby('Violates')
test_0_groups['BooleanViolation'].aggregate(np.mean).plot(kind = 'line', label =
        "Voicing Language")
test_1_groups['BooleanViolation'].aggregate(np.mean).plot(kind = 'line', label =
        "Place Language")
plt.title('Learned Quickly')
plt.ylabel('Percent of times violation was chosen')
plt.legend()
plt.show()

unlearned_test = unlearned[unlearned.PageType == 'Test']
unlearned_test['SelectedViolation'] = unlearned_test.apply(lambda row: row['Violation'][row['SelectedPosition']], axis = 1)
unlearned_test['BooleanViolation'] = unlearned_test.SelectedViolation.apply(lambda x: 1 if x == 'True' else 0)
unlearned_0_groups = unlearned_test[unlearned_test.Permutation == 0].groupby('Violates')
unlearned_1_groups = unlearned_test[unlearned_test.Permutation == 1].groupby('Violates')
unlearned_0_groups.BooleanViolation.aggregate(np.mean).plot(kind = 'line', label
        = 'Voicing Language')
unlearned_1_groups.BooleanViolation.aggregate(np.mean).plot(kind = 'line', label
        = 'Place Language')
plt.title('Did Not Pass Training')
plt.legend()
plt.show()

# catch['Alternates'] = catch.apply(lambda row: row['Alternates'][row['SelectedPosition']], axis = 1)
# catch_groups = catch.groupby(['Permutation', 'Alternates'])
# print catch_groups.Alternates.count()

# def get_alternation_position(row):
#     return row['Alternates'].index(1)

# test['AlternationPosition'] = test.apply(get_alternation_position, axis = 1)
# catch['AlternationPosition'] = catch.apply(get_alternation_position, axis = 1)

# add columns for analyzing catch questions
# def chose_right(row):
#     language = 'pilot_voice' if row['Permutation'] == 0 else 'pilot_nasal'
#     should_alternate = 'T' if row['Condition'] == language else 'F'
#     did_alternate = 'T' if row['Alternates'][row['SelectedPosition']] == 'T' else 'F'
#     return did_alternate == should_alternate

# catch['Right'] = catch.apply(chose_right, axis = 1)

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

test['ViolationPosition'] = test.apply(lambda row: row['Violation'].index('True'), axis = 1)
test['TestedOn'] = test.Violates.apply(lambda x: '*DF' if x == 'Voicing' else '*NF')

# include just the right columns
to_analyze = pd.DataFrame({
    # 'ViolatesPlace': test.ViolatesPlace,
    'Violates': test.Violates,
    'ChoseViolation': test.BooleanViolation,
    'Permutation': test.Permutation,
    'TrainedOn': test.TrainedOn,
    'TestedOn': test.TestedOn,
    'Segment': test.Segment,
    'Subject': test.WorkerID,
    'Item': test.PageID,
    # 'NumberIterations': test.NumberIterations,
    'Accuracy': test.Accuracy,
    'ViolationPosition': test.ViolationPosition,
    'ReactionTime': test.ReactionTime,
    'TrialNumber': test.TrialNumber})

# write to csv
to_analyze.to_csv('alternations_dataframe.csv')

to_analyze_catch = pd.DataFrame({
    'Alternates': catch.Alternates,
    'Permutation': catch.Permutation,
    'TrainedOn': catch.TrainedOn,
    'Segment': catch.Segment,
    'Subject': catch.WorkerID,
    'Item': catch.PageID,
    'SelectedPosition': catch.SelectedPosition,
    'ReactionTime': catch.ReactionTime,
    'TrialNumber': catch.TrialNumber
    })

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

# catch_groups = catch.groupby(['TrainedOn', 'Alternates'])
# catch_counts = catch_groups.count()
# catch_counts['Alternates'].plot(kind = 'bar')
# plt.show()

# make graphs #TODO graph results and reaction times
# chose_violate_place = to_analyze[to_analyze.ViolatesPlace == True]
# groups = to_analyze.groupby(['TrainedOn', 'ViolatesPlace'])
# counts = groups.count()
# print counts.ViolatesPlace
# counts['ViolatesPlace'].plot(kind = 'bar')
# plt.show()

language_groups = to_analyze.groupby(['Permutation'])
# print language_groups['Subject'].count()
unlearned_groups = to_analyze[to_analyze.NumberIterations == 5].groupby(['Permutation'])
# print unlearned_groups['Subject'].count()

# reaction times
# time_groups = catch.groupby(['Condition', 'Permutation', 'Right'])
# mean_times = time_groups['ReactionTime'].aggregate(np.mean)
# # sd_times = time_groups['ReactionTime'].aggregate(np.sd)
# mean_times.plot(kind = 'bar')
# plt.show()

# write to csv
to_analyze.to_csv('alternations_dataframe.csv')

included_workers = set(to_analyze.Subject)
freetext_questions = dedup[dedup.PageID.isin(['635', '637', '639'])]
freetext_included = freetext_questions[freetext_questions.WorkerID.isin(included_workers)]
freetext_df = pd.DataFrame({
    'WorkerID': freetext_included.WorkerID,
    'PageID': freetext_included.PageID,
    'SelectedText': freetext_included.SelectedText
})

freetext_df.to_csv('alternations_freetext.csv')
