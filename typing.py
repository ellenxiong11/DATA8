"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    i=0
    while i<len(paragraphs):
        if select(paragraphs[i]):
            i+=1
        else:
            paragraphs.remove(paragraphs[i])
    if len(paragraphs)<=k:
        return ""
    return paragraphs[k]



    # END PROBLEM 1"""


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def helper(x):
        x=remove_punctuation(x)
        x=lower(x)
        x=split(x)
        for i in x:
            if i in topic:
                return True
        return False
    return lambda x: helper(x)
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    counter=0
    if len(typed_words)==0:
        return 0.0
    for i in range(min(len(typed_words),len(reference_words))):
        if typed_words[i]==reference_words[i]:
            counter+=1
    return 100*counter/len(typed_words)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return len(typed)*(60/elapsed)/5
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    diffs=[]
    for i in valid_words:
        diffs+=[[i,diff_function(user_word,i,limit)]]
    diffs.sort(key = lambda x: x[1])
    if diffs[0][1]>limit:
        return user_word
    else:
        return diffs[0][0]
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    letters=abs(len(start)-len(goal))
    if len(start)>len(goal):
        start=start[:len(goal)]
    if len(goal)>len(start):
        goal=goal[:len(start)]
    def helpme(start,goal,diff):
        if diff>limit:
            return limit+1
        if start==goal:
            return diff
        else:
            if start[len(start)-1:]!=goal[len(goal)-1:]:
                diff+=1
        return helpme(start[:len(start)-1],goal[:len(goal)-1],diff)
    return helpme(start,goal,letters)



    # END PROBLEM 6

def edit_diff(start, goal, limit):
    def helper(start,goal,edits):
        if edits>limit:
            return limit+1
        if start==goal:
            return edits
        if start[:1]!=goal[:1]:
            if start[1:2]==goal[1:2]:
                return helper(start[1:],goal[1:],edits+1)
            elif start[:1]==goal[1:2]:
                return helper(start,goal[1:],edits+1)
            elif start[1:2]==goal[:1]:
                return helper(start[1:],goal,edits+1)
            elif len(start)<len(goal):
                return helper(start,goal[1:],edits+1)
            elif len(start)>len(goal):
                return helper(start[1:],goal,edits+1)
            else:
                return helper(start[1:],goal[1:],edits+1)
        else:# start[:1]==goal[:1]
            return helper(start[1:],goal[1:],edits)
    return helper(start,goal,0)



        # BEGIN

        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    numerator=0
    for i in range(len(typed)):
        if typed[i]==prompt[i]:
            numerator+=1
        else:
            break
    progress=numerator/len(prompt)
    dict={'id': id, 'progress': progress}
    send(dict)
    return progress
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    def time_spent_typing_word(i, player):
        return elapsed_time(word_times[player][i])-elapsed_time(word_times[player][i-1])
    def fastest_time_for_word(i):
        return min([time_spent_typing_word(i, player) for player in range(n_players)])
    all_times=[] #list of all times of all words of all players
    for v in range(n_players):
        all_times+=[[time_spent_typing_word(i, v) for i in range(1,n_words+1)]]
    min_times=[fastest_time_for_word(i) for i in range(1,n_words+1)] #list of all min times
    min_times=[margin+min_times[i] for i in range(len(min_times))]
    res=[]
    for u in range(n_players):
        playern=[]
        for w in range(n_words):
            if all_times[u][w]<=min_times[w]:
                playern+=[word(word_times[u][w+1])]
        res+=[playern]
    return res




    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
