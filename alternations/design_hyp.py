from speriment import *
import glob, itertools, random

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
take their time on these questions actually finish this phase about <b>much
faster</b> than those who rush through the questions. Take your time and pronounce the correct
answers out loud when they're given to help you learn how this language
sounds.'''

test_introduction = '''In this part of the experiment, you will see pairs of new words.
Based on how each word sounds, decide which one is more likely to belong to the
language you just learned.'''

test_question = '''Which of these two words is more likely to be a word of the
language you just learned?'''

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

rows = get_dicts('items_apr28.csv')
item_types = dict([(key, list(val)) for (key, val)
    in itertools.groupby(rows, lambda r: r['language'])])

# exposure
common = item_types['both'] # s and non-alternating pl
train1 = item_types['voice'] # s and pl in -p/-t
train2 = item_types['nasal'] # s and pl in -m
plural = item_types['plural'] # pl in -m and pl in -p/-t
# L1 should show common, train1, train2.singular, plural.singular
# L2 should show common, train2, train1.singular, plural.plural

# training
#for catch, singular is non-alternating, plural is alternating
voice_catch = item_types['pilot_voice']
nasal_catch = item_types['pilot_nasal']
filler_catch = item_types['pilot_filler']

# test
test = item_types['test']
filler = item_types['filler']

##### Structure #####

with make_experiment(IDGenerator()):


    ###### Exposure Phase #######

    def singular_exposure(rows):
        return [Page(
            [exposure_question, row['singular']],
            options = [Option()],
            freetext = True,
            condition = row['language'],
            tags = {'PageType': 'Exposure', 'StimulusType': 'Singular'})
        for row in rows]

    def plural_exposure(rows, lang):
        return [Page(
            [exposure_question, row[lang]],
            options = [Option()],
            freetext = True,
            condition = row['language'],
            tags = {'PageType': 'Exposure', 'StimulusType': 'Plural'})
        for row in rows]

    def dual_exposure(rows):
        return [Page(
            [exposure_question_2, row['singular'], ' - ', row['plural'] ],
            options = [Option()],
            freetext = True,
            condition = row['language'],
            tags = {'PageType': 'Exposure', 'StimulusType': 'Singular-Plural'})
        for row in rows]

    ### Pages ###
    singular_exposure_L1 = singular_exposure(train1)
    singular_exposure_L2 = singular_exposure(train2)
    plural_exposure_m = plural_exposure(plural, 'singular')
    plural_exposure_pt = plural_exposure(plural, 'plural')
    dual_exposure_L1 = dual_exposure(train1)
    dual_exposure_L2 = dual_exposure(train2)
    dual_exposure_both = dual_exposure(common)

    ### Blocks ###
    L1_exposure = Block(pages =
            singular_exposure_L2 +
            plural_exposure_m +
            dual_exposure_both +
            dual_exposure_L1)
    L2_exposure = Block(pages =
            singular_exposure_L1 +
            plural_exposure_pt +
            dual_exposure_both +
            dual_exposure_L2)


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
                        row['plural']], tags = {'PageType': 'Feedback'})
                    ),
                Option(
                    row['plural'],
                    tags = {'Alternates': 'True', 'Segment': row['segment1']},
                    correct = True,
                    feedback = Page(['Correct! <br><br>', row['stem'], ' - ',
                        row['plural']], tags = {'PageType': 'Feedback'})
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
                        row['singular']], tags = {'PageType': 'Feedback'})
                    ),
                Option(
                    row['plural'],
                    tags = {'Alternates': 'True', 'Segment': row['segment1']},
                    correct = False,
                    feedback = Page(['No, the correct pairing is <br><br>', row['stem'], ' - ',
                        row['singular']], tags = {'PageType': 'Feedback'})
                    )
                ],
            keyboard = True,
            tags = {'PageType': 'Wug', 'ShouldAlternate': False}
            ) for row in rows]

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

    test_pages_voice = [Page(
        test_question,
        options = [
            Option(row['singular'], tags = {'Violation': 'True'}), # b or d
            Option(row['voice_satisfying'], tags = {'Violation': 'False'})], # p or t
        keyboard = True,
        condition = 'voice',
        tags = {"PageType": 'Test', "Violates": "Voicing", "Segment": row['segment1']}
        ) for row in test]

    test_pages_place = [Page(
        test_question,
        options = [
            Option(row['plural'], tags = {'Violation': 'True'}), # n or ng
            Option(row['place_satisfying'], tags = {'Violation': 'False'})], # m
        keyboard = True,
        condition = 'place',
        tags = {"PageType": 'Test', "Violates": "Place", "Segment": row['segment2']}
        ) for row in test]

    filler_pages_v = [Page(
        test_question,
        options = [
            Option(row['singular']), #l
            Option(row['plural'])], # s
        keyboard = True,
        condition = 'voice', #just to keep pseudorandomization happy
        tags = {'PageType': 'Filler'}
        ) for row in filler[:len(filler)/2]]

    filler_pages_p = [Page(
        test_question,
        options = [
            Option(row['singular']), #l
            Option(row['plural'])], # s
        keyboard = True,
        condition = 'place', #just to keep pseudorandomization happy
        tags = {'PageType': 'Filler'}
        ) for row in filler[len(filler)/2:]]

    test_block = Block(pages = test_pages_voice + test_pages_place +
            filler_pages_v + filler_pages_p, pseudorandom = True)

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

        treatments = [
            [L1_exposure, L1_training],
            [L2_exposure, L2_training]])

    experiment.install('alternations_experiment_hyp')
