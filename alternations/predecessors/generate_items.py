import random, copy, csv

vowels = ['a', 'e', 'i', 'o', 'u']
voice_consonants_bad = ['b', 'd']
voice_consonants_good = ['p', 't']
nasal_consonants_bad = ['n', 'ng']
nasal_consonants_good = ['m']
other_consonants = ['f', 's', 'l']
space = [' ']
cons = voice_consonants_bad + voice_consonants_good + nasal_consonants_bad + \
        nasal_consonants_good + other_consonants #10


num_training_fillers = 5
num_training_stimuli = 10
num_testing_fillers = 10
num_testing_stimuli = 20

def training_fillers(itemfile):
    random.shuffle(cons)
    c1 = copy.deepcopy(cons[:5])
    c2 = copy.deepcopy(cons[5:])
    random.shuffle(vowels)
    v1 = copy.deepcopy(vowels)
    random.shuffle(vowels)
    v2 = copy.deepcopy(vowels)
    c3 = voice_consonants_good + nasal_consonants_good + ['s', 'l']
    random.shuffle(c3)
    c3 = copy.deepcopy(c3)
    c4 = space * 5

    training_fillers = zip(c1, v1, c2, c4, v2, c3)
    for tf in training_fillers:
        itemfile.writerow(tf + ('both',))

def training_languages(itemfile):
    random.shuffle(cons)
    c1 = copy.deepcopy(cons)
    random.shuffle(cons)
    c2 = copy.deepcopy(cons)
    vow = vowels * 2
    random.shuffle(vow)
    v1 = copy.deepcopy(vow)
    random.shuffle(vow)
    v2 = copy.deepcopy(vow)
    c4 = space * 10

    voice_c3 = voice_singulars()
    voice_sing = zip(c1, v1, c2, c4, v2, voice_c3)
    for vs in voice_sing:
        itemfile.writerow(vs + ('voice',))

    nasal_c3 = nasal_singulars()
    nasal_sing = zip(c1, v1, c2, c4, v2, nasal_c3)
    for ns in nasal_sing:
        itemfile.writerow(ns + ('nasal',))

def voice_singulars():
    c3 = 5 * voice_consonants_bad
    random.shuffle(c3)
    cons3 = copy.deepcopy(c3)
    return cons3

def nasal_singulars():
    c3 = 5 * nasal_consonants_bad
    random.shuffle(c3)
    cons3 = copy.deepcopy(c3)
    return cons3


# test

def test(itemfile):
    consonants = cons * 2
    random.shuffle(consonants)
    c1 = copy.deepcopy(consonants)
    random.shuffle(consonants)
    c3 = copy.deepcopy(consonants)
    c2 = voice_consonants_bad * 10
    random.shuffle(c2)
    c2 = copy.deepcopy(c2)
    vow = vowels * 4
    random.shuffle(vow)
    v1 = copy.deepcopy(vow)
    random.shuffle(vow)
    v2 = copy.deepcopy(vow)
    c4 = nasal_consonants_bad * 10
    random.shuffle(c4)
    c4 = copy.deepcopy(c4)

    test = zip(c1, v1, c2, c4, v2, c3)
    for t in test:
        itemfile.writerow(t + ('test',))

# testing fillers

def testing_fillers(itemfile):
    random.shuffle(cons)
    c1 = copy.deepcopy(cons)
    random.shuffle(cons)
    c2 = copy.deepcopy(cons)
    random.shuffle(cons)
    c3 = copy.deepcopy(cons)
    random.shuffle(cons)
    c4 = copy.deepcopy(cons)
    vow = vowels * 2
    random.shuffle(vow)
    v1 = copy.deepcopy(vow)
    random.shuffle(vow)
    v2 = copy.deepcopy(vow)

    fillers = zip(c1, v1, c2, c3, v2, c4)
    for f in fillers:
        itemfile.writerow(f + ('filler',))

def pilot_test(itemfile):
    random.shuffle(cons)
    c1 = copy.deepcopy(cons)
    random.shuffle(cons)
    c2 = copy.deepcopy(cons)
    vow = vowels * 2
    random.shuffle(vow)
    v1 = copy.deepcopy(vow)
    random.shuffle(vow)
    v2 = copy.deepcopy(vow)
    c4 = space * 10

    voice_c3 = voice_singulars()
    voice_sing = zip(c1, v1, c2, c4, v2, voice_c3)
    for vs in voice_sing:
        itemfile.writerow(vs + ('pilot_voice',))

    nasal_c3 = nasal_singulars()
    nasal_sing = zip(c1, v1, c2, c4, v2, nasal_c3)
    for ns in nasal_sing:
        itemfile.writerow(ns + ('pilot_nasal',))

if __name__ == '__main__':
    itemfile = 'items_feb7.csv'
    with open(itemfile, 'w') as f:
        g = csv.writer(f)
        g.writerow(['C1', 'V1', 'C2', 'C3', 'V2', 'C4', 'Language'])
        training_fillers(g)
        training_languages(g)
        test(g)
        testing_fillers(g)
        pilot_test(g)

        # concatenate and code by hand
        # fix: no ng word initially
        # no geminates
        # some word medial clusters - none that violate C1 or C2
        # no real words
        # fix by moving characters around vertically in their own class

        # features not controlled for
