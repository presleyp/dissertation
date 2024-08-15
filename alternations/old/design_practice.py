from speriment import *
import glob, itertools, random

#TODO fix tags
##### Wording #####

train_introduction = '''In this part of the experiment, you will learn words
from a made-up language. Their meanings will be expressed through pictures. You
will see a picture with two words and be asked to choose which word has the
meaning shown by the picture. At first you will just be guessing, but that's
okay. Try to remember the right answer, and you'll get better with practice.'''

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

daily_language = "What language do you speak most often?"

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

rows = get_dicts('/Users/presley/dissertation/alternations/alternations_practice.csv') #TODO
item_types = dict([(key, list(val)) for (key, val)
    in itertools.groupby(rows, lambda r: r['language'])])

common = item_types['both'][:5] #TODO
lang1 = item_types['1'][:3]
lang2 = item_types['2'][:3]
test = item_types['voice'] + item_types['nasal'] + item_types['filler'] #TODO need sing and pl for filler

train1 = lang1 + common
train2 = lang2 + common

words1 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train1]
words2 = [{'singular': row['singular'], 'plural': row['plural']}
        for row in train2]


##### Structure #####

with make_experiment(IDGenerator()):

    ##### Training #####

    def make_train_pages(rows):
        wordbank = 'words1' if rows[0]['language'] == '1' else 'words2'
        pagelist = []
        for number in ('singular', 'plural'):
            other = 'plural' if number == 'singular' else 'singular'
            pagelist += [Page(
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
            pagelist += [Page(
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
        random.shuffle(pagelist)
        l = len(pagelist)/2
        return (pagelist[:l], pagelist[l:])

    (lang1_training_a, lang1_training_b) = make_train_pages(train1)

    (lang2_training_a, lang2_training_b) = make_train_pages(train2)

    lang1_block = Block(blocks = [
        Block(pages = lang1_training_a, criterion = 0.8),
        Block(pages = lang1_training_b, criterion = 0.8)])
    lang2_block = Block(blocks = [
        Block(pages = lang2_training_a, criterion = 0.8),
        Block(pages = lang2_training_b, criterion = 0.8)])

    ###### Testing ######

    test_pages = [Page(
        test_question,
        options = [Option(row['singular']), Option(row['plural'])],
        keyboard = True,
        ) for row in test]

    test_block = Block(pages = test_pages)

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
        demographics_block,
        outro_block],
        treatments = [[lang1_block], [lang2_block]],
        banks = {'words1': words1,
            'words2': words2,
            'pictures': pictures})
    experiment.install('alternations_experiment')
