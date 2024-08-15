from speriment import *

with make_experiment(IDGenerator()):
    p = Page('''This HIT is for paying workers who attempted HIT
    3TC2K6WK9G2I8R2JNQZTU4MD3IY28E, and could not finish it. Please write your
    Worker ID below and if you were among the workers who attempted it, I will
    give you a bonus of $2.25, which was supposed to be the payment for the
    other HIT. If you were not one of those workers, please return this HIT,
    or I will have to reject your submission.''', options = [Option()])
    b = Block(pages = [p])
    e = Experiment(blocks = [b])
    e.install('alternations_repayment')
