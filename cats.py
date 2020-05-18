"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    
    counter = 0
    for i in range(len(paragraphs)):
    	if select(paragraphs [i]):
    		if counter == k:
    			return paragraphs [i]
    		counter = counter + 1
    return ''
    



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
 
    def return_func(input_paragraph):
    	input_paragraph = remove_punctuation(input_paragraph)
    	input_paragraph = split(input_paragraph)
    	input_paragraph = [lower(x) for x in input_paragraph]
    	for i in range(len(topic)):
    		for j in range(len(input_paragraph)):
    			if topic[i] == input_paragraph[j]:
    				return True
    	return False

    return return_func





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
    correct = 0
    incorrect = 0

    if len(typed_words) == 0:
    	return 0.0

    if len(typed_words) > len(reference_words):
    	incorrect += len(typed_words) - len(reference_words)
    	typed_words = typed_words[:len(reference_words)]


    for i in range(len(typed_words)):
    	if typed_words[i] == reference_words[i]:
    		correct += 1
    	else:
    		incorrect += 1

    return (correct / (correct + incorrect)) * 100 




def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    return (len(typed) / 5) / (elapsed / 60)



def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """

    least_diff_word = ''
    prev_lowest_diff = 11
    index_corresponding_to_lowest_diff = -1

    for i in range(len(valid_words)):
    	if user_word == valid_words[i]:
    		return user_word
    	else:
    		new_diff = diff_function(user_word, valid_words[i], limit)
    		if new_diff < prev_lowest_diff:
    			prev_lowest_diff = new_diff
    			index_corresponding_to_lowest_diff = i

    if prev_lowest_diff > limit:
    	return user_word

    else:
    	return valid_words[index_corresponding_to_lowest_diff]



def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """

    if limit < 0:
        return 103297846123784012478362109478390124827

    if len(start) == len(goal) == 0:
   	    return 0

    if len(start) != len(goal):
   	    if len(start) > len(goal):
   	        return len(start) - len(goal) + sphinx_swap(start[:len(goal)], goal, limit - len(start) + len(goal))
   	    else:
   	        return len(goal) - len(start) + sphinx_swap(start, goal[:len(start)], limit - len(goal) + len(start))

    if start[0] == goal[0]:
        return sphinx_swap(start[1:], goal[1:], limit)

    else:
        return 1 + sphinx_swap(start[1:], goal[1:], limit - 1)




def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if limit < 0:

	    return limit + 1 


    elif len(start) == 0 or len(goal) == 0:
	    return max(len(start), len(goal))

    elif start[0] == goal[0]:
        return feline_fixes(start[1: len(start)], goal[1: len(goal)], limit)

    elif start == goal: 

        return 0


    else:
        add_diff = feline_fixes(goal[0] + start, goal, limit - 1) + 1  # Fill in these lines
        remove_diff = feline_fixes(start[1:len(start)], goal, limit - 1) + 1
        substitute_diff = feline_fixes(goal[0] + start[1: len(start)], goal, limit - 1) + 1 

        return min(add_diff, remove_diff, substitute_diff)



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""

    correct = 0
    for i in range(len(typed)):
    	if typed[i] == prompt[i]:
    		correct += 1
    	else:
    		send({'id': id, 'progress': correct / len(prompt)})
    		return correct / len(prompt)

    send({'id': id, 'progress': correct / len(prompt)})
    return correct / len(prompt)



def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """

    k = len(times_per_player[0])

    manipulated_times_per_player = []
    
    for i in range(len(times_per_player)):
    	list_for_the_iteration = []
    	for j in range (k - 1):
    		list_for_the_iteration.append(times_per_player[i][j + 1] - times_per_player[i][j])
    	manipulated_times_per_player.append(list_for_the_iteration)



    return game(words, manipulated_times_per_player)



def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word

    return_list = []
    
    for i in players:
    	return_list.append([])

    for j in words:
    	initialised_fastest_time = time(game, 0, j)
    	corresponding_index = 0
    	for k in players[1:]:
    		time_being_considered_right_now = time(game, k, j)
    		if time_being_considered_right_now < initialised_fastest_time:
    			corresponding_index = k
    			initialised_fastest_time = time_being_considered_right_now
    	return_list[corresponding_index].append(word_at(game, j))

    return return_list



def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  



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
