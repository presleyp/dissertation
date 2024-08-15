from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import copy

#mysql://presley:Qlw6JXnaR5@localhost:3306/Cumulativity


# exclude duplicates
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

# def parse_selected_position(row):
#     if type(row['SelectedPosition']) == list:
#         return row['SelectedPosition'][0]
#     else:
#         return False

def exclude_one_sided(test):
    # test['SelectedPosition'] = test.SelectedPosition.apply(lambda x: x[0])
    worker_groups = test.groupby('WorkerID', as_index = False)
    aggregation = worker_groups.agg({'SelectedIndex': np.mean})
    one_side = set(aggregation[aggregation['SelectedIndex'] > 0.9]['WorkerID'])\
                | set(aggregation[aggregation['SelectedIndex'] < 0.1]['WorkerID'])
    attentive = test[~test.WorkerID.isin(one_side)]
    print "Number of participants dropped for favoring one option position"
    print len(one_side)
    return attentive

def exclude_old(df, version):
    current = df[df.ExperimentVersion == version]
    return current



# read data
data = None
with open('results_june3.json', 'r') as f:
    data = f.read()
js = json.loads(data)
df = pd.DataFrame(js)

df = exclude_old(df, '7')
# pilot person the day before
df = df[~df.WorkerID.isin(['A39E9936894TJR'])]

# add/modify useful columns
df['ReactionTime'] = df.EndTime - df.StartTime
# df['SelectedType'] = df.apply(lambda row: row['type'][row['SelectedIndex']]
        # if type(row['SelectedIndex']) == int and type(row['type']) == list else row['type'], axis = 1)

### Exclusions
workers = exclude_debug(df)
dedup = exclude_duplicates(workers)
print 'initial total'
print len(set(dedup.WorkerID))
# non_minors = exclude_minors(dedup, '461')
non_minors = exclude_minors(dedup, '558')
# non_minors = exclude_minors(dedup, '557')


# catch = non_minors[non_minors.PageType == 'Catch']
# catch['Selected'] = catch.SelectedText.apply(lambda x: x[0])
# missed_catch = set(catch[catch['Selected'] == 'Yes']['WorkerID'])
# print 'Number of participants excluded for missing catch trials'
# print len(missed_catch)

# test = non_minors[non_minors.PageType == 'Test']
# test['SelectedText'] = test.SelectedText.apply(lambda x: x[0])
# test = test[~test.WorkerID.isin(missed_catch)]

test = non_minors[non_minors.PageType.isin(['Catch', 'Test'])]
#TODO catch exclusions
test['SelectedText'] = test.SelectedText.apply(lambda x: x[0])


humans = exclude_bot_speed(test)
humans['SelectedIndex'] = humans.SelectedPosition.apply(lambda x: x[0])
attentive = exclude_one_sided(humans)
# read: language answers, strategy answers
# March 17:
# A12DBV9FNAOFEM speaks Bulgarian
# A3GFDGDJ3UNL18 speaks Spanish
# A3IMQGP6Q6URB6 speaks English and French but native language english
# 'A3FY350Q19GO3H', 'A3DZ85L2U5NU8U', 'A30QRYULPVYZQV', 'A1N35VV9QURKHX' chose best and worst equally
english_speakers = attentive[~attentive.WorkerID.isin(['A12DBV9FNAOFEM',
'A3GFDGDJ3UNL18', 'A3FY350Q19GO3H', 'A3DZ85L2U5NU8U', 'A30QRYULPVYZQV', 'A1N35VV9QURKHX'])]

# where from question is ambiguous, could draw on any information, so I'm
# ignoring it though two answers were India, Russia
# June 3:
# one native language answer was Spanish: AAXYYH9MI3PJM

# June 17:
# A1CXNVK45K3GY0 - Arabic
# A1WCC1EPZRG4TQ - Bengali
# ABB9DYBUWGNNX - Arabic

# english_speakers = attentive[attentive.WorkerID != 'AAXYYH9MI3PJM']
# english_speakers = attentive[~attentive.WorkerID.isin(['A1CXNVK45K3GY0', 'A1WCC1EPZRG4TQ', 'ABB9DYBUWGNNX'])]

print "Number of participants dropped for saying English was not their native language"
print 3
results = english_speakers

print 'Number of included participants'
print len(set(results.WorkerID))

# make useful columns
# results['SelectedTest'] = results.apply(lambda row: row['SelectedType'] == 'test', axis = 1)
results.Response = results.apply(lambda row: row['Response'][row['SelectedIndex']], axis = 1)

results['ItemID'] = results.apply(lambda row: row['ItemID'] if
        type(row['ItemID']) == str else
        row['PageText'].split('>')[-2].rstrip('</b'), axis = 1)
print 'item ids'
print results[results.PageType == 'Catch'].ItemID

def assess_catch(worker_group):
    cond_groups = worker_group.groupby('Condition')
    response_means = cond_groups.aggregate(np.mean)['Response']
    difference = response_means[0] - response_means[1]
    return difference > 0

catch = results[results.PageType == 'Catch']
# worker_groups = catch.groupby('WorkerID')
# catch_agg = worker_groups.aggregate(assess_catch)
# print catch_agg
catch_groups = catch.groupby(['PageID'])
catch_means = catch_groups.aggregate(np.mean)
catch_means.to_csv('response_means.csv')
# print 'catch means'
# print catch_means['Response']
# catch_means['negative'] = catch_means.apply(lambda row: -row['Response'] if
#         row['Condition'] == 'worst' else row['Response'], axis = 1)
# print catch_means['negative']
# catch_means['balance'] = catch_means['negative'] + catch_means['positive']
# print catch_means[catch_means.balance < 0]


# def get_filler(row):
#     filler_index = row['type'].index('filler')
#     return row['OptionTexts'][filler_index]

# results['Filler'] = results.apply(get_filler, axis = 1)

def get_yes_position(row):
    return row['OptionTexts'].index('Yes')

results['YesPosition'] = results.apply(get_yes_position, axis = 1)

def to_boolean(row):
    return 0 if row == False else 1

# include just the right columns
to_analyze = pd.DataFrame({
    # 'SelectedTest': results.SelectedTest.apply(to_boolean),
    'Response': results.Response,
    'OnsetViolation': results.OnsetViolation.apply(to_boolean),
    'CodaViolation': results.CodaViolation.apply(to_boolean),
    'Condition': results.Condition,
    'Subject': results.WorkerID,
    'Item': results.ItemID,
    # 'Filler': results.Filler,
    'PageType': results.PageType,
    'Vowel': results.Vowel,
    'ReactionTime': results.ReactionTime,
    'TrialNumber': results.TrialNumber,
    'Version': results.Version,
    'YesPosition': results.YesPosition})

# print to_analyze[to_analyze.Condition == 'BB'].groupby('Item').agg(np.mean)['Response']
# print to_analyze[to_analyze.Condition == 'BG'].groupby('Item').agg(np.mean)['Response']
# print to_analyze[to_analyze.Condition == 'GB'].groupby('Item').agg(np.mean)['Response']


# make graphs
# cond_groups = to_analyze.groupby(['Condition', 'Response'])
# cond_groups.count()['Response'].plot(kind = 'bar')
# plt.show()

cond_groups2 = to_analyze.groupby('Condition')
cond_means = cond_groups2.aggregate(np.mean)['Response']
# print cond_means
cond_means.plot(kind = 'bar')
# plt.show()


# number where test was chosen for each condition
# chose_test = to_analyze[to_analyze.SelectedTest == True]
# test_groups = chose_test.groupby(['Condition', 'Response'])
# test_counts = test_groups.count()
# total_groups = to_analyze.groupby('Condition')
# total_counts = total_groups.count()

# reorder
# conds = {'BB': 0, 'GB': 1, 'BG': 2, 'GG': 3}
# key = chosen_counts['Condition'].map(conds)
# chosen_counts = chosen_counts.iloc[key.argsort()]

# ind = np.arange(4)
# wid = 0.8
# # total = sum(chosen_counts.Condition)
# gg = 100 * test_counts.Condition[3]/total_counts.Condition[3]
# bg = 100 * test_counts.Condition[1]/total_counts.Condition[1]
# gb = 100 * test_counts.Condition[2]/total_counts.Condition[2]
# bb = 100* test_counts.Condition[0]/total_counts.Condition[0]
# plt.bar(ind, [gg, bg, gb, bb], width = wid)
# # plt.bar(ind + wid, [np.exp(0), np.exp(-1), np.exp(-2), np.exp(-3)], width = wid)
# # plt.bar(ind + 2 * wid, [0.5, 1/3., 1/6., 0], width = wid)
# plt.title('Percent of Times Test Word Chosen')
# plt.xlabel('Condition of Test Word')
# plt.ylabel('Experiment-Wide Percentage')
# plt.xticks(ind+wid/2., ('Good-Good', 'Bad-Good', 'Good-Bad', 'Bad-Bad') )
# plt.show()

# check distribution of versions
worker_set = to_analyze.drop_duplicates('Subject')
worker_set.groupby('Version').count()['Version'].plot(kind = 'bar')
# plt.show()

# mean reaction time for each condition/selection
time_groups = to_analyze.groupby(['Condition', 'Response'])
mean_times = time_groups['ReactionTime'].aggregate(np.mean)
# sd_times = time_groups['ReactionTime'].aggregate(np.sd)
# outlier_times = time_groups[time_groups['ReactionTime'] > (mean_times + 2 *
#     sd_times)]
mean_times.plot(kind = 'bar')
# plt.show()

included_workers = set(to_analyze.Subject)
freetext_questions = df[df.PageType == 'Demographics']
freetext_included = freetext_questions[freetext_questions.WorkerID.isin(included_workers)]
freetext_df = pd.DataFrame({
    'WorkerID': freetext_included.WorkerID,
    'PageID': freetext_included.PageID,
    'SelectedText': freetext_included.SelectedText
})

# write to csv
# to_analyze.to_csv('cumulativity_june3_dataframe.csv')

# freetext_df.to_csv('cumulativity_june3_freetext.csv')
