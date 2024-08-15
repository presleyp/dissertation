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
print 'original number of workers'
print len(set(workers.WorkerID))
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
    merged_df = get_accuracy(df)
    passed = set(merged_df[merged_df.Accuracy > criterion].WorkerID)
    return (merged_df[merged_df.WorkerID.isin(passed)], merged_df[~merged_df.WorkerID.isin(passed)])

def get_accuracy(df):
    training = df[df.PageType == 'Wug']
    training['Correct'] = training.Correct.apply(lambda x: 1 if x[0] == True else 0)
    scores = training.groupby('WorkerID').aggregate(np.mean)
    scores['Accuracy'] = scores['Correct']
    merged_df = df.join(scores['Accuracy'], on = 'WorkerID')
    return merged_df


# add columns for analyzing test questions

attentive['TrainedOn'] = attentive.Permutation.apply(lambda x: 'Devoicing' if x == 0
        else 'PlaceAssimilation')

# bilinguals with Marathi, Armenian - problem?
#AEWJSYEXHW37F speaks Hebrew
#AMPFH3OAXMTT0 speaks Chinese
english = attentive[~attentive.WorkerID.isin(['AEWJSYEXHW37F',
'AMPFH3OAXMTT0'])]


# learned, unlearned = exclude_inaccurate(test, .8)
annotated = get_accuracy(english)

# print learned
# print '''Number of participants included:'''
# print len(set(learned.WorkerID))
print '''Number of participants that reached criterion:'''
print len(set(annotated[annotated.Accuracy > .7].WorkerID))

test = annotated[annotated.PageType == 'Test']
catch = annotated[annotated.PageType == 'Catch']

test['SelectedViolation'] = test.apply(lambda row: row['Violation'][row['SelectedPosition']], axis = 1)
test['ChoseViolation'] = test.SelectedViolation.apply(lambda x: 1 if x == 'True' else 0)
test['ViolationPosition'] = test.apply(lambda row: row['Violation'].index('True'), axis = 1)
test['TestedOn'] = test.Violates.apply(lambda x: '*DF' if x == 'Voicing' else '*NF')


# include just the right columns
to_analyze = pd.DataFrame({
    'Violates': test.Violates,
    'ChoseViolation': test.ChoseViolation,
    'Permutation': test.Permutation,
    'TrainedOn': test.TrainedOn,
    'TestedOn': test.TestedOn,
    'Segment': test.Segment,
    'Subject': test.WorkerID,
    'Item': test.PageID,
    'Accuracy': test.Accuracy,
    'ViolationPosition': test.ViolationPosition,
    'ReactionTime': test.ReactionTime,
    'TrialNumber': test.TrialNumber})

# write to csv
to_analyze.to_csv('alternations_dataframe.csv')

# doesn't have unlearned removed

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

# write to csv
to_analyze.to_csv('alternations_dataframe_june.csv')

included_workers = set(to_analyze.Subject)
freetext_questions = dedup[dedup.PageID.isin(['573', '575', '577', '579', '581',
    '582'])]
freetext_included = freetext_questions[freetext_questions.WorkerID.isin(included_workers)]
freetext_df = pd.DataFrame({
    'WorkerID': freetext_included.WorkerID,
    'PageID': freetext_included.PageID,
    'SelectedText': freetext_included.SelectedText
})

freetext_df.to_csv('alternations_freetext_june.csv')
