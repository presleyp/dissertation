from speriment import *
import glob, itertools, random

#TODO some fillers violate constraints

# 10 own rule s, 10 own rule pl
# 10 other rule s
# 10 other rule pl

# training

# own rule vs no rule
# filler with change vs filler without change
# 

# testing

# own rule yes/no

##### Wording #####

keyboard_instructions = '''For these questions, you will not be able to use your mouse. Use
the F key to choose the option on the left, the J key to choose the option
on the right, and the spacebar to move forward.'''

exposure_introduction = '''In this part of the experiment, you will learn words
from a made-up language.
<br><br>
Sometimes you'll see one word, and sometimes you'll see two: the
singular version of the word first, and then the plural version.
<br><br>
To help yourself catch on to this new language, type the words you see into the
text box. We recommend pronouncing them out loud, too. In this
language, "ng" is always pronounced as in "singer", never as in "finger".'''

exposure_question = '''Please write this word in the text box and pronounce it
to yourself:
<br><br>'''

exposure_question_2 = '''Please write these words in the text box and pronounce
them to yourself:
<br><br>'''

training_introduction = '''Now we'll focus on learning singulars and plurals a bit
more. You'll see the singular version of a word and two possible plurals. Choose
the one you think is correct for this language. Sometimes you'll then be given
the correct answer afterwards, to help you learn. Other times you won't see how
you did.
<br><br>
The length of this phase depends on your accuracy. We've found that people who
take their time on these questions actually finish this phase about <b>twice as
fast</b> as those who rush through the questions. Take your time and pronounce the correct
answers out loud when they're given to help you learn how this language
sounds.'''

catch_intro = '''In this phase, you'll see the singular version of a word and
two possible plurals. Choose the one you think is correct for this language.'''

# test_introduction = '''In this part of the experiment, you will see pairs of new words.
# Based on how each word sounds, decide which one is more likely to belong to the
# language you just learned.'''
test_introduction = '''In this part of the experiment, you will see new words
and be asked whether they sound like they could belong to the language you just
learned.
<br><br>
For instance, if the language you had just learned was English, you might say
"yes" to "strabe", which is not English but sounds like it could be, and "no" to
"gzat", which sounds weird as an English word.
<br><br>
Don't feel like you need to say "yes" and "no" an equal number of times.
The number of acceptable words you see can vary.'''

# test_question = '''Which of these two words is more likely to be a word of the
# language you just learned?'''
test_question = '''Based on how it sounds, do you think this word could belong to the language you just
learned?'''

training_question = '''Which of these words do you think is the correct plural for this word? <br><br>'''

mouse_instructions = '''Now you can use your mouse again.'''

native_language = "What is your native language?"

daily_language = "What language do you speak at home?"

age = "How old are you?"

sex = "What is your sex?"

strategy = '''What information or strategies did you use to choose between words in the
last section? What did you use in the singular-plural section?'''

goodbye = '''Thank you for participating in this experiment! Remember to click
Complete HIT on the next page.'''


##### Materials #####

all_pictures = glob.glob('static/images/stim/*.png')
plural_pictures = set(glob.glob('static/images/stim/*-pl.png'))
singular_pictures = sorted([pic for pic in all_pictures if pic not in plural_pictures])
plural_pictures = sorted(list(plural_pictures))
pictures = [{'singular': sing, 'plural': pl} for (sing, pl) in
        zip(singular_pictures, plural_pictures)]

rows = get_dicts('items_apr10.csv')
item_types = dict([(key, list(val)) for (key, val)
    in itertools.groupby(rows, lambda r: r['language'])])

##### rows ######
#5
common = item_types['both'] # s and non-alternating pl
#10
train1 = item_types['voice'] # s and pl in -p/-t
#10
train2 = item_types['nasal'] # s and pl in -m
#10
plural = item_types['plural'] # pl in -m and pl in -p/-t
# L1 should show common, train1, train2.singular, plural.singular
# L2 should show common, train2, train1.singular, plural.plural

test = item_types['test'] + item_types['filler']
#for catch, singular is non-alternating, plural is alternating
voice_catch = item_types['pilot_voice']
nasal_catch = item_types['pilot_nasal']
filler_catch = item_types['pilot_filler']


##### wordbanks ######

words1 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train1]
words2 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train2]
common_words = [{'singular': row['singular'], 'plural': row['plural']}
        for row in common]
plural_words = [{'m': row['singular'], 'pt': row['plural']}
        for row in plural]

##### Structure #####

with make_experiment(IDGenerator()):


    ###### Exposure Phase #######

    def singular_exposure(rows, wordbank):
        return [Page(
            [exposure_question, SampleFrom(wordbank, variable = row['stem'], field = 'singular')],
            options = [Option()],
            freetext = True,
            condition = row['language'],
            keyboard = False,
            tags = {'PageType': 'Exposure', 'StimulusType': 'Singular'})
        for row in rows]

    def plural_exposure(rows, wordbank, lang):
        return [Page(
            [exposure_question, SampleFrom(wordbank, variable = row['stem'], field = lang)],
            options = [Option()],
            freetext = True,
            condition = row['language'],
            keyboard = False,
            tags = {'PageType': 'Exposure', 'StimulusType': 'Plural'})
        for row in rows]

    def dual_exposure(rows, wordbank):
        return [Page(
            [exposure_question_2,
                SampleFrom(wordbank, variable = row['stem'], field = 'singular'),
                ' - ',
                SampleFrom(wordbank, variable = row['stem'], field = 'plural')
                ],
            options = [Option()],
            freetext = True,
            condition = row['language'],
            keyboard = False,
            tags = {'PageType': 'Exposure', 'StimulusType': 'Singular-Plural'})
        for row in rows]

    ### Pages ###
    singular_exposure_L1 = singular_exposure(train1, 'words1')
    singular_exposure_L2 = singular_exposure(train2, 'words2')
    plural_exposure_m = plural_exposure(plural, 'plural_words', 'm')
    plural_exposure_pt = plural_exposure(plural, 'plural_words', 'pt')
    dual_exposure_L1 = dual_exposure(train1, 'words1')
    dual_exposure_L2 = dual_exposure(train2, 'words2')
    dual_exposure_both = dual_exposure(common, 'common_words')

    ### Blocks ###
    L1_exposure = Block(pages = singular_exposure_L2 + plural_exposure_m +
            dual_exposure_both + dual_exposure_L1)
    L2_exposure = Block(pages = singular_exposure_L1 + plural_exposure_pt +
            dual_exposure_both + dual_exposure_L2)


    ###### Training Phase ######

    def alternating_training(rows):
        return [Page(
            [training_question, row['stem']],
            options = [
                Option(
                    row['singular'],
                    tags = {'Alternates': 'False', 'Segment': row['segment1']},
                    correct = False,
                    feedback = Page(['No, the correct pairing is <br><br>', row['stem'], ' - ',
                        row['plural']])
                    ),
                Option(
                    row['plural'],
                    tags = {'Alternates': 'True', 'Segment': row['segment1']},
                    correct = True,
                    feedback = Page(['Correct! <br><br>', row['stem'], ' - ',
                        row['plural']])
                    )
                ],
            keyboard = True,
            tags = {'PageType': 'Wug', 'ShouldAlternate': True}
            ) for row in rows]

    def non_alternating_training(rows):
        return [Page(
            [training_question, row['stem']],
            options = [
                Option(
                    row['singular'],
                    tags = {'Alternates': 'False', 'Segment': row['segment1']},
                    correct = True,
                    feedback = Page(['Correct! <br><br>', row['stem'], ' - ',
                        row['singular']])
                    ),
                Option(
                    row['plural'],
                    tags = {'Alternates': 'True', 'Segment': row['segment1']},
                    correct = False,
                    feedback = Page(['No, the correct pairing is <br><br>', row['stem'], ' - ',
                        row['singular']])
                    )
                ],
            keyboard = True,
            tags = {'PageType': 'Wug', 'ShouldAlternate': False}
            ) for row in rows]

    # def make_wug_training(rows, should_alternate):
    #     first = False if should_alternate else True
    #     second = True if should_alternate else False
    #     pl = 'plural' if should_alternate else 'singular'
    #     return [Page(
    #         [training_question, row['stem']],
    #         options = [
    #             Option(
    #                 row['singular'],
    #                 tags = {
    #                     'Alternates': 'F',
    #                     'Segment': row['segment1']},
    #                 correct = first,
    #                 feedback = Page(['Correct! <br><br>', row['stem'], ' - ',
    #                     row[pl]])
    #                 ),
    #             Option(
    #                 row['plural'],
    #                 tags = {
    #                     'Alternates': 'T',
    #                     'Segment': row['segment1']},
    #                 correct = second)],
    #         feedback = Page(['The plural of ' + row['stem'] + ' is <b>' +
    #             row[pl], '</b>']),
    #         condition = row['language'],
    #         keyboard = True,
    #         tags = {"PageType": "Wug"}
            # ) for row in rows]

    def make_wug_exposure(rows):
        return [Page(
            [training_question, row['stem']],
            options = [
                Option(
                    row['singular'],
                    tags = {
                        'Alternates': 'False',
                        'Segment': row['segment1']},
                    ),
                Option(
                    row['plural'],
                    tags = {
                        'Alternates': 'True',
                        'Segment': row['segment1']},
                    )],
            keyboard = True,
            tags = {"PageType": "Catch"}
            ) for row in rows]

    ### Pages ###
    filler_training = non_alternating_training(filler_catch)
    L1_training_pages = alternating_training(voice_catch) + filler_training + make_wug_exposure(nasal_catch)
    L2_training_pages = alternating_training(nasal_catch) + filler_training + make_wug_exposure(voice_catch)

    ### Blocks ###
    L1_training = Block(pages = L1_training_pages, criterion = 0.8, cutoff = 5)
    L2_training = Block(pages = L2_training_pages, criterion = 0.8, cutoff = 5)

    ###### Testing Phase ######

    test_pages_s = [Page(
        [test_question, '<br><br>', row['singular']],
        options = [
            Option('Yes'),
            Option('No')],
        keyboard = True,
        tags = {"PageType": "Test", "Violates": "Voicing", "Segment": row['segment1']}
        ) for row in test]

    test_pages_pl = [Page(
        [test_question, '<br><br>', row['plural']],
        options = [
            Option('Yes'),
            Option('No')],
        keyboard = True,
        tags = {"PageType": "Test", "Violates": "Place", "Segment": row['segment2']}
        ) for row in test]

    test_block = Block(pages = test_pages_s + test_pages_pl)

    ###### Test if they learned rules #####

    precatch = Block(pages = [Page(catch_intro)])

    ##### Niceties #####

    exposure_intro = Block(pages = [Page(exposure_introduction)])
    train_intro = Block(pages = [Page(training_introduction)])
    test_intro = Block(pages = [Page(test_introduction)])
    outro_block = Block(pages = [Page(goodbye)])
    keyboard_block = Block(pages = [Page(keyboard_instructions)])
    mouse_block = Block(pages = [Page(mouse_instructions)])
    demographics_block = Block(pages = [
        Page(age, options = [Option(i) for i in range(120)], ordered = True),
        Page(sex, options = [Option('male'), Option('female'), Option('other')]),
        Page(native_language, options = [Option()], freetext = True),
        Page(daily_language, options = [Option()], freetext = True),
        Page(strategy, options = [Option()], freetext = True),
        # Page(for_pilot, options = [Option()], freetext = True)
    ])

    ##### Experiment #####

    experiment = Experiment([
        exposure_intro,
        L1_exposure, L2_exposure,

        keyboard_block,

        train_intro,
        L1_training, L2_training,

        test_intro,
        test_block,

        mouse_block,

        demographics_block,
        outro_block],
        treatments = [[L1_exposure, L1_training],
            [L2_exposure, L2_training]],
        banks = {
            'words1': words1,
            'words2': words2,
            'common_words': common_words,
            'plural_words': plural_words,
            'pictures': pictures
        })
    experiment.install('alternations_experiment_may')
