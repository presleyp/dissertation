from speriment import *
import glob, itertools, random

##### Wording #####

train_introduction = '''In this part of the experiment, you will learn words
from a made-up language. Their meanings will be expressed through pictures.

You will see a picture with two words and be asked to choose which word has the
meaning shown by the picture. At first you will just be guessing, but that's
okay. Try to remember the right answer, and you'll get better with practice.

Remember: in this language, "ng" is always pronounced as in "singer", never
as in "finger".'''

train_question = '''Which word is represented by this picture?'''

test_question = '''Which of these two words is more likely to be a word of the
language you just learned?'''

test_introduction = '''In this part of the experiment, you will see pairs of new words.
Based on how each word sounds, decide which one is more likely to belong to the
language you just learned.'''

instructions = '''During experimental questions, you will not be able to use your mouse. Use
the F key to choose the option on the left, the J key to choose the option
on the right, and the spacebar to move forward.'''

native_language = "What is your native language?"

daily_language = "What language do you speak at home?"

where_from = "Where do people typically think you're from?"

age = "How old are you?"

sex = "What is your sex?"

strategy = '''What information or strategies did you use to choose words in the
experimental questions?'''

goodbye = "Thank you for participating in this experiment!"


##### Materials #####

all_pictures = glob.glob('static/images/stim/*.png')
plural_pictures = set(glob.glob('static/images/stim/*-pl.png'))
singular_pictures = sorted([pic for pic in all_pictures if pic not in plural_pictures])
plural_pictures = sorted(list(plural_pictures))
pictures = [{'singular': sing, 'plural': pl} for (sing, pl) in
        zip(singular_pictures, plural_pictures)]

rows = get_dicts('/Users/presley/dissertation/alternations/items_feb23.csv')
item_types = dict([(key, list(val)) for (key, val)
    in itertools.groupby(rows, lambda r: r['language'])])

common = item_types['both']
train1 = item_types['voice']
train2 = item_types['nasal']
test = item_types['test'] + item_types['filler']
pilot = item_types['pilot_voice'] + item_types['pilot_nasal']

words1 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train1]
words2 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train2]
common_words = [{'singular': row['singular'], 'plural': row['plural']}
        for row in common]

##### Structure #####

with make_experiment(IDGenerator()):

    ##### Training #####

    def lexical_choice(rows, number, wordbank):
        return [Page(
                train_question,
                options = [
                    Option(SampleFrom(wordbank, variable = row['stem'], field =
                        number), correct = True),
                    Option(SampleFrom(wordbank, not_variable = row['stem'], field =
                        number), correct = False)
                ],
                resources = [SampleFrom('pictures', variable = row['stem'], field =
                    number)],
                feedback = Page([SampleFrom(wordbank, variable = row['stem'], field = number),
                    " means:"],
                    resources = [SampleFrom('pictures', variable = row['stem'], field =
                    number)]),
                condition = row['language'],
                keyboard = True)
            for row in rows]

    def number_choice(rows, number, wordbank):
        other = 'singular' if number == 'plural' else 'plural'
        return [Page(
                train_question,
                options = [
                    Option(SampleFrom(wordbank, variable = row['stem'], field =
                        number), correct = True),
                    Option(SampleFrom(wordbank, variable = row['stem'], field =
                        other), correct = False)
                ],
                resources = [SampleFrom('pictures', variable = row['stem'], field =
                    number)],
                feedback = Page([SampleFrom(wordbank, variable = row['stem'], field =
                    number), " means: "],
                    resources = [SampleFrom('pictures', variable = row['stem'], field =
                    number)]),
                condition = row['language'],
                keyboard = True)
            for row in rows]

    L1_singular_lexical = lexical_choice(train1, 'singular', 'words1')
    L1_singular_number = number_choice(train1, 'singular', 'words1')
    L1_plural_lexical = lexical_choice(train1, 'plural', 'words1')
    L1_plural_number = number_choice(train1, 'plural', 'words1')
    L2_singular_lexical = lexical_choice(train2, 'singular', 'words2')
    L2_singular_number = number_choice(train2, 'singular', 'words2')
    L2_plural_lexical = lexical_choice(train2, 'plural', 'words2')
    L2_plural_number = number_choice(train2, 'plural', 'words2')
    training_fillers = lexical_choice(common, 'singular', 'common_words') + \
        number_choice(common, 'singular', 'common_words') + \
        lexical_choice(common, 'plural', 'common_words') + \
        number_choice(common, 'plural', 'common_words')

    def make_inner_blocks(singular_lexical, singular_number,
            other_singular_lexical, plural_lexical, plural_number, training_filler):
        stimuli_n = 5
        filler_n = 2
        block1 = Block(pages =
                singular_lexical[:stimuli_n] +
                singular_number[:stimuli_n] +
                other_singular_lexical[:stimuli_n] +
                plural_lexical[:stimuli_n] +
                plural_number[:stimuli_n] +
                training_filler[:filler_n],
            criterion = 0.8)
        block2 = Block(pages = singular_lexical[stimuli_n:] +
                singular_number[stimuli_n:] +
                other_singular_lexical[stimuli_n:] +
                other_singular_lexical[stimuli_n:] +
                plural_lexical[stimuli_n:] +
                plural_number[stimuli_n:] +
                training_filler[filler_n:],
            criterion = 0.8)
        return [block1, block2]

    lang1_block = Block(blocks = make_inner_blocks(L1_singular_lexical,
        L1_singular_number, L2_singular_lexical, L1_plural_lexical,
        L1_plural_number, training_fillers))

    lang2_block = Block(blocks = make_inner_blocks(L2_singular_lexical,
        L2_singular_number, L1_singular_lexical, L2_plural_lexical,
        L2_plural_number, training_fillers))

    ###### Testing ######

    test_pages = [Page(
        test_question,
        options = [Option(row['singular']), Option(row['plural'])],
        keyboard = True,
        tags = {'voice_segment': row['segment1'],
            'nasal_segment': row['segment2']}
        ) for row in test]

    test_block = Block(pages = test_pages)


    ###### Piloting #####

    prepilot = Block(pages = [Page('''Now you will see a singular word and be asked
    which of two words you think is more likely to be the plural for that word
    in the language you learned.''')])
    pilot_pages = [Page(
        ["Which of these words do you think is the correct plural for this word? <br><br>",
            row['stem']],
        options = [Option(row['singular'], tags = {'alternates': 'F', 'segment':
            row['segment1']}),
            Option(row['plural'], tags = {'alternates': 'T', 'segment': row['segment1']})],
        condition = row['language'],
        keyboard = True
        ) for row in pilot]

    pilot_block = Block(pages = pilot_pages)

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
        Page(strategy, options = [Option()], freetext = True)
    ])

    ##### Experiment #####

    experiment = Experiment([
        intro_block,
        train_intro,
        lang1_block,
        lang2_block,
        test_intro,
        test_block,
        prepilot,
        pilot_block,
        demographics_block,
        outro_block],
        treatments = [[lang1_block], [lang2_block]],
        banks = {
            'words1': words1,
            'words2': words2,
            'common_words': common_words,
            'pictures': pictures
        })
    experiment.install('alternations_experiment')
