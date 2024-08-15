from speriment import *
#TODO pilot page, catch trials

##### Wording #####

introduction = '''In this experiment, you will be shown made-up words.
Based on how they sound, decide if they could become a new English word or not.
'''

instructions = '''During experimental questions, you will not be able to use your mouse. Use
the F key to choose the option on the left, the J key to choose the option
on the right, and the spacebar to move forward.'''

def question(word):
    return '''Based on how it sounds, could this be a word of
English?
<br><br>
{0}'''.format(word)

native_language = "What is your native language?"

daily_language = "What language do you speak at home?"

where_from = "Where do people typically think you're from?"

age = "How old are you?"

sex = "What is your sex?"

strategy = '''What information or strategies did you use to choose words in the
experimental questions?'''

pilot = '''This is a pilot for an experiment I'll run on people later. Do you
have any feedback for me about the length or difficulty of the experiment, or
any bugs or typos you saw? Thanks for your help!'''

goodbye = "Thank you for participating in this experiment!"


##### Stimuli #####

rows = get_dicts('items_oct8.csv')

# fillers = [row['filler'] for row in rows]

test_conditions = [('GG', False, False),
        ('GB', False, True),
        ('BG', True, False),
        ('BB', True, True)]

##### Experiment structure #####

with make_experiment(IDGenerator()):

    intro_block = Block(pages = [Page(introduction)])
    instruction_block = Block(pages = [Page(instructions)])

    #TODO latin square still?

    # There's an interesting SampleFrom issue here. For a given participant,
    # only one Page per group will ever show. Yet four are constructed, and so
    # four SampleFrom's are constructed. If I don't give them variables, I am
    # asking for 4 * the number of fillers' worth of fillers, and the experiment
    # will break. So I tell each Page in the same group to use the same filler,
    # which doesn't actually create any correlations in the displayed Pages.
    # The tag 'ItemID' will be used as a random effect in the model.
    test_page_groups = [
        [Page(
            question(row[test_condition]),
            options = [
                Option('Yes'),
                Option('No')
            ],
            tags = {'ItemID': str(i), 'OnsetViolation': onset, 'CodaViolation':
                coda, 'Vowel': row['vowel']},
            condition = test_condition,
            keyboard = True
        ) for (test_condition, onset, coda) in test_conditions]
    for (i, row) in enumerate(rows)]

    # A Latin Square issue comes up here. Latin Squares only work if the number
    # of items (groups) is a multiple of the number of conditions. I'm making
    # fake groups (four of the same page) for catch trials so I can mix them
    # into my test items. I have to make four of these groups (or a multiple thereof) to
    # avoid messing up the Latin Square. It probably wouldn't hurt since I add
    # them at the end of the block, but better to be safe.
    # catch_word_pairs = [('lbifth', 'slan'), ('krlisg', 'felp'), ('psatr',
    #     'lunt'), ('tmozb', 'velk')]
    # catch_trials = [Page(
    #             question,
    #             options = [
    #                 Option(bad_word, tags = {'type': 'catch-bad'}),
    #                 Option(good_word, tags = {'type': 'catch-good'})
    #             ],
    #             keyboard = True
    #         )
    #         for (bad_word, good_word) in catch_word_pairs]

    # When duplicating these catch trial Pages, I use the `new` method to give
    # them unique IDs. The conditions are not actually necessary because Latin
    # Squares use position in groups rather than the condition attribute to
    # choose pages from groups, but it can help me check that the Latin Square
    # was done correctly.
    # def make_catch_groups(catch_trial):
    #     catch_group = [catch_trial]
    #     for i in range(1, 4):
    #         new_trial = catch_trial.new()
    #         catch_group.append(new_trial)
    #     return catch_group

    # catch_groups = [make_catch_groups(catch_trial)
    #         for catch_trial in catch_trials]

    test_block = Block(
        groups = test_page_groups,
        latin_square = True,
    )

    demographics_block = Block(pages = [
        Page(age, options = [Option(i) for i in range(120)], ordered = True),
        Page(sex, options = [Option('male'), Option('female'), Option('other')]),
        Page(native_language, options = [Option()], freetext = True),
        Page(daily_language, options = [Option()], freetext = True),
        Page(where_from, options = [Option()], freetext = True),
        Page(strategy, options = [Option()], freetext = True),
        Page(pilot, options = [Option()], freetext = True)
    ])

    thanks_block = Block(pages = [Page(goodbye)])

    experiment = Experiment([
        intro_block,
        instruction_block,
        test_block,
        demographics_block,
        thanks_block
    ])
    experiment.install('cumulativity_experiment_time')
