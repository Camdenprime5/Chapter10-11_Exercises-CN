import doctest
import os


# 10.11.1 - Research notes
# Dictionary keys must be hashable because Python uses their hash values to
# look them up efficiently. A key's hash must not change while it is stored.
# Strings and integers work as keys; mutable lists and dictionaries do not.
# To make a set from a list of words: word_set = set(word_list)
# To check for a word: 'banana' in word_set


# 10.11.2 - Use get() to count characters without an if statement.
def value_counts(sequence):
    """Return the number of times each element appears.

    >>> value_counts('banana')
    {'b': 1, 'a': 3, 'n': 2}
    >>> value_counts('')
    {}
    >>> value_counts('aabb')
    {'a': 2, 'b': 2}
    >>> value_counts([1, 2, 1])
    {1: 2, 2: 1}
    """
    counter = {}
    for item in sequence:
        counter[item] = counter.get(item, 0) + 1
    return counter


# 10.11.3 - Detect whether a sequence has a repeated element.
def has_duplicates(sequence):
    """Return True if an element appears more than once.

    >>> has_duplicates('banana')
    True
    >>> has_duplicates('unpredictably')
    False
    >>> has_duplicates([1, 2, 3, 2])
    True
    >>> has_duplicates([])
    False
    >>> has_duplicates('')
    False
    """
    seen = {}
    for item in sequence:
        if item in seen:
            return True
        seen[item] = True
    return False


def longest_unique_letter_words(words):
    """Find the longest words whose letters never repeat.

    >>> longest_unique_letter_words(['cat', 'banana', 'stop', 'tops'])
    ['stop', 'tops']
    >>> longest_unique_letter_words([])
    []
    """
    longest = []
    longest_length = 0
    for word in words:
        if not has_duplicates(word.lower()):
            if len(word) > longest_length:
                longest_length = len(word)
                longest = [word]
            elif len(word) == longest_length:
                longest.append(word)
    return longest


# 10.11.4 - Find keys whose counts are greater than one.
def find_repeats(counter):
    """Return keys whose counts are above 1.

    >>> find_repeats({'b': 1, 'a': 3, 'n': 2})
    ['a', 'n']
    >>> find_repeats({'x': 1, 'y': 1})
    []
    >>> find_repeats({})
    []
    """
    repeated = []
    for key in counter:
        if counter[key] > 1:
            repeated.append(key)
    return repeated


# 10.11.5 - Add two dictionaries of counts into a new dictionary.
def add_counters(counter1, counter2):
    """Add the counts without changing the original dictionaries.

    >>> add_counters({'a': 2, 'b': 1}, {'a': 1, 'c': 3})
    {'a': 3, 'b': 1, 'c': 3}
    >>> add_counters({}, {'x': 2})
    {'x': 2}
    >>> add_counters({'x': 1}, {})
    {'x': 1}
    """
    combined = {}
    for key in counter1:
        combined[key] = counter1[key]
    for key in counter2:
        combined[key] = combined.get(key, 0) + counter2[key]
    return combined


# 10.11.6 - Split a word into alternating letters and check both halves.
# Once words.txt has been loaded, this dictionary lets is_interlocking(word)
# work with only the one argument the textbook requests.
word_dictionary = {}


def is_interlocking(word, lookup=None):
    """Return True if alternating letters form two words in lookup.

    >>> is_interlocking('schooled', {'shoe': True, 'cold': True})
    True
    >>> is_interlocking('schooled', {'shoe': True})
    False
    >>> is_interlocking('abcdef', {})
    False
    """
    if lookup is None:
        lookup = word_dictionary
    first = word[::2]
    second = word[1::2]
    return first in lookup and second in lookup


def find_interlocking_words(words, lookup):
    """Return interlocking words with at least eight letters and their halves.

    >>> find_interlocking_words(['schooled', 'cat'], {'shoe': 1, 'cold': 1})
    [('schooled', 'shoe', 'cold')]
    """
    matches = []
    for word in words:
        if len(word) >= 8 and is_interlocking(word, lookup):
            matches.append((word, word[::2], word[1::2]))
    return matches


def load_words(filename):
    """Load one word per line into a list."""
    words = []
    reader = open(filename, encoding='utf-8')
    for line in reader:
        word = line.strip().lower()
        if word:
            words.append(word)
    reader.close()
    return words


def main():
    results = doctest.testmod()
    print(f'Chapter 10 doctests: {results.attempted} run, {results.failed} failed')
    print('Counts for banana:', value_counts('banana'))
    print('Repeated letters in banana:', find_repeats(value_counts('banana')))
    print('Unpredictably has duplicates:', has_duplicates('unpredictably'))
    print('Counts for banana + apple:',
          add_counters(value_counts('banana'), value_counts('apple')))
    print('Schooled = shoe + cold:',
          is_interlocking('schooled', {'shoe': 1, 'cold': 1}))

    if os.path.isfile('words.txt'):
        words = load_words('words.txt')
        for word in words:
            word_dictionary[word] = True
        matches = find_interlocking_words(words, word_dictionary)
        print('Words loaded:', len(words))
        print('Longest words with no repeated letters:',
              longest_unique_letter_words(words))
        print('Interlocking words of at least 8 letters:', len(matches))
        print('First 10 interlocking words:', matches[:10])
    else:
        print('Place words.txt in this project to run the full word searches.')


if __name__ == '__main__':
    main()
