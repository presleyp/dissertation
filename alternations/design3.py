from speriment import *
import glob, itertools, random

##### Wording #####

instructions = '''During experimental questions, you will not be able to use your mouse. Use
the F key to choose the option on the left, the J key to choose the option
on the right, and the spacebar to move forward.'''

train_introduction = '''In this part of the experiment, you will learn words
from a made-up language. Their meanings will be expressed through pictures.
<br><br>
You will see a picture with two words and be asked to choose which word has the
meaning shown by the picture. At first you will just be guessing, but that's
okay. Try to remember the right answer, and you'll get better with practice.
<br><br>
Remember: in this language, "ng" is always pronounced as in "singer", never
as in "finger".'''

train_question = '''Which word is represented by this picture?'''

test_introduction = '''In this part of the experiment, you will see pairs of new words.
Based on how each word sounds, decide which one is more likely to belong to the
language you just learned.'''

test_question = '''Which of these two words is more likely to be a word of the
language you just learned?'''

catch_intro = '''Good job! Now we'll move onto a new kind of practive. You will
see a singular word and be asked which of two words you think is more likely to
be the plural for that word in the language you learned.'''

catch_question = '''Which of these words do you think is the correct plural for this word? <br><br>'''

native_language = "What is your native language?"

daily_language = "What language do you speak at home?"

where_from = "Where do people typically think you're from?"

age = "How old are you?"

sex = "What is your sex?"

strategy = '''What information or strategies did you use to choose words in the
experimental questions?'''

for_pilot = '''This is a dry run of an experiment I'll run later. Do you have
any feedback for me about how hard it was, how long it was, or anything that
looked weird? Would you like to send me a secret message through the
interwebs?'''

goodbye = "Thank you for participating in this experiment!"


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

#5
common = item_types['both']
#10
train1 = item_types['voice']
#10
train2 = item_types['nasal']
#10
plural = item_types['plural']

test = item_types['test'] + item_types['filler']
voice_catch = item_types['pilot_voice']
nasal_catch = item_types['pilot_nasal']
filler_catch = item_types['pilot_filler']

words1 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train1]
words2 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train2]
common_words = [{'singular': row['singular'], 'plural': row['plural']}
        for row in common]
plural_words = [{'L1': row['singular'], 'L2': row['plural']}
        for row in plural]

##### Structure #####

with make_experiment(IDGenerator()):

    ##### Training #####

    def lexical_choice(rows, number, wordbank):
        num = 'plural' if number in ['L1', 'L2'] else number
        return [Page(
                train_question,
                options = [
                    Option(SampleFrom(wordbank, variable = row['stem'], field =
                        number), correct = True, tags = {'Number': num,
                            'Wordbank': wordbank}),
                    Option(SampleFrom(wordbank, not_variable = row['stem'], field =
                        number), correct = False, tags = {'Number': num,
                            'Wordbank': wordbank})
                ],
                resources = [SampleFrom('pictures', variable = row['stem'], field =
                    num)],
                feedback = Page([SampleFrom(wordbank, variable = row['stem'], field = number),
                    " means:"],
                    resources = [SampleFrom('pictures', variable = row['stem'], field =
                    num)]),
                condition = row['language'],
                keyboard = True,
                tags = {"PageType": "Lexical"})
            for row in rows]

    def number_choice(rows, number, wordbank):
        other = 'singular' if number == 'plural' else 'plural'
        return [Page(
                train_question,
                options = [
                    Option(SampleFrom(wordbank, variable = row['stem'], field =
                        number), correct = True, tags = {'Number': number,
                            'Wordbank': wordbank}),
                    Option(SampleFrom(wordbank, variable = row['stem'], field =
                        other), correct = False, tags = {'Number': other,
                            'Wordbank': wordbank})
                ],
                resources = [SampleFrom('pictures', variable = row['stem'], field =
                    number)],
                feedback = Page([SampleFrom(wordbank, variable = row['stem'], field =
                    number), " means: "],
                    resources = [SampleFrom('pictures', variable = row['stem'], field =
                    number)]),
                condition = row['language'],
                keyboard = True,
                tags = {"PageType": "Number"})
            for row in rows]

    L1_singular_lexical = lexical_choice(train1, 'singular', 'words1')
    L1_singular_number = number_choice(train1, 'singular', 'words1')
    L1_plural_lexical = lexical_choice(train1, 'plural', 'words1')
    L1_plural_number = number_choice(train1, 'plural', 'words1')
    L1_extra_plural_lexical = lexical_choice(plural, 'L1', 'plural_words')
    L2_singular_lexical = lexical_choice(train2, 'singular', 'words2')
    L2_singular_number = number_choice(train2, 'singular', 'words2')
    L2_plural_lexical = lexical_choice(train2, 'plural', 'words2')
    L2_plural_number = number_choice(train2, 'plural', 'words2')
    L2_extra_plural_lexical = lexical_choice(plural, 'L2', 'plural_words')
    training_fillers = lexical_choice(common, 'singular', 'common_words') + \
        number_choice(common, 'singular', 'common_words') + \
        lexical_choice(common, 'plural', 'common_words') + \
        number_choice(common, 'plural', 'common_words')

    def make_inner_blocks(singular_lexical,
            singular_number,
            other_singular_lexical,
            plural_lexical,
            plural_number,
            extra_plural,
            training_filler):
        stimuli_n = 5
        filler_n = 2
        block1 = Block(pages =
                singular_lexical[:stimuli_n] +
                singular_number[:stimuli_n] +
                other_singular_lexical[:stimuli_n] +
                plural_lexical[:stimuli_n] +
                plural_number[:stimuli_n] +
                extra_plural[:stimuli_n] +
                training_filler[:filler_n],
            criterion = 0.8)
        block2 = Block(pages =
                singular_lexical[stimuli_n:] +
                singular_number[stimuli_n:] +
                other_singular_lexical[stimuli_n:] +
                plural_lexical[stimuli_n:] +
                plural_number[stimuli_n:] +
                extra_plural[:stimuli_n] +
                training_filler[filler_n:],
            criterion = 0.8)
        return [block1, block2]

    lang1_block = Block(blocks = make_inner_blocks(
        L1_singular_lexical,
        L1_singular_number,
        L2_singular_lexical,
        L1_plural_lexical,
        L1_plural_number,
        L1_extra_plural_lexical,
        training_fillers))

    lang2_block = Block(blocks = make_inner_blocks(
        L2_singular_lexical,
        L2_singular_number,
        L1_singular_lexical,
        L2_plural_lexical,
        L2_plural_number,
        L2_extra_plural_lexical,
        training_fillers))

    ###### Testing ######

    test_pages = [Page(
        test_question,
        options = [
            Option(row['singular'], tags = {'Violates': 'voicing',
                'Segment': row['segment1']}),
            Option(row['plural'], tags = {'Violates': 'place', 'Segment':
                row['segment2']})],
        keyboard = True,
        tags = {"PageType": "Test"}
        ) for row in test]

    test_block = Block(pages = test_pages)


    ###### Test if they learned rules #####

    precatch = Block(pages = [Page(catch_intro)])

    def make_wug_training(rows, should_alternate):
        first = False if should_alternate else True
        second = True if should_alternate else False
        return [Page(
            [catch_question, row['stem']],
            options = [
                Option(
                    row['singular'],
                    tags = {
                        'Alternates': 'F',
                        'Segment': row['segment1']},
                    correct = first),
                Option(
                    row['plural'],
                    tags = {
                        'Alternates': 'T',
                        'Segment': row['segment1']},
                    correct = second)],
            feedback = Page(['The plural of ' + row['stem'] + ' is ' +
                row['plural']]),
            condition = row['language'],
            keyboard = True,
            tags = {"PageType": "Wug"}
            ) for row in rows]

    def make_catch(rows):
        return [Page(
            [catch_question, row['stem']],
            options = [
                Option(
                    row['singular'],
                    tags = {
                        'Alternates': 'F',
                        'Segment': row['segment1']},
                    ),
                Option(
                    row['plural'],
                    tags = {
                        'Alternates': 'T',
                        'Segment': row['segment1']},
                    )],
            condition = row['language'],
            keyboard = True,
            tags = {"PageType": "Catch"}
            ) for row in rows]


    # train to alternate voice
    voice_wug_block = Block(pages = make_wug_training(voice_catch, True) +
            make_wug_training(filler_catch, False), criterion =
            0.8)
    # train to alternate place
    nasal_wug_block = Block(pages = make_wug_training(nasal_catch, True) +
            make_wug_training(filler_catch, False), criterion =
            0.8)
    # gather information - if not trained to alternate voice, do you?
    voice_catch_block = Block(pages = make_catch(voice_catch))
    # gather information - if not trained to alternate place, do you?
    nasal_catch_block = Block(pages = make_catch(nasal_catch))

    ##### Niceties #####

    intro_block = Block(pages = [Page(instructions)])
    train_intro = Block(pages = [Page(train_introduction)])
    test_intro = Block(pages = [Page(test_introduction)])
    outro_block = Block(pages = [Page(goodbye)])
    demographics_block = Block(pages = [
        Page(age, options = [Option(i) for i in range(120)], ordered = True),
        Page(sex, options = [Option('male'), Option('female'), Option('other')]),
        Page(native_language, options = [Option()], freetext = True),
        Page(daily_language, options = [Option()], freetext = True),
        Page(where_from, options = [Option()], freetext = True),
        Page(strategy, options = [Option()], freetext = True),
        # Page(for_pilot, options = [Option()], freetext = True)
    ])

    ##### Experiment #####

    experiment = Experiment([
        intro_block,
        train_intro,
        lang1_block,
        lang2_block,
        precatch,
        voice_wug_block,
        nasal_wug_block,
        test_intro,
        test_block,
        nasal_catch_block,
        voice_catch_block,
        demographics_block,
        outro_block],
        treatments = [[lang1_block, voice_wug_block, nasal_catch_block],
            [lang2_block, nasal_wug_block, voice_catch_block]],
        banks = {
            'words1': words1,
            'words2': words2,
            'common_words': common_words,
            'plural_words': plural_words,
            'pictures': pictures
        })
    experiment.install('alternations_experiment_2')
