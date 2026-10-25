import doctest
import os


# 11.11.1 - Break larger problems into small functions, test those functions,
# and then combine them. The exercises below use that strategy.


# 11.11.2 - A tuple may contain lists that can be changed, but then that
# tuple cannot be used as a dictionary key (its contents are not hashable).
def tuple_with_mutable_lists():
    """Append 6 to the second list inside a tuple.

    >>> tuple_with_mutable_lists()
    ([1, 2, 3], [4, 5, 6])
    """
    first = [1, 2, 3]
    second = [4, 5]
    t = (first, second)
    t[1].append(6)
    return t


def unhashable_tuple_example():
    """Show that a tuple containing lists cannot be a dictionary key.

    >>> unhashable_tuple_example()
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'list'
    """
    t = ([1, 2, 3], [4, 5, 6])
    return {t: 'this tuple contains two lists'}


# 11.11.3 - Caesar cipher: map alphabet letters to indices with zip().
alphabet = 'abcdefghijklmnopqrstuvwxyz'
letter_map = dict(zip(alphabet, range(len(alphabet))))


def shift_word(word, shift):
    """Shift alphabetic letters, wrapping around; keep other characters.

    >>> shift_word('cheer', 7)
    'jolly'
    >>> shift_word('melon', 16)
    'cubed'
    >>> shift_word('xyz', 3)
    'abc'
    >>> shift_word('Hello!', 1)
    'Ifmmp!'
    >>> shift_word('ABC', -1)
    'ZAB'
    """
    shifted_letters = []
    for letter in word:
        lower_letter = letter.lower()
        if lower_letter in letter_map:
            old_index = letter_map[lower_letter]
            new_index = (old_index + shift) % len(alphabet)
            new_letter = alphabet[new_index]
            if letter.isupper():
                new_letter = new_letter.upper()
            shifted_letters.append(new_letter)
        else:
            shifted_letters.append(letter)
    return ''.join(shifted_letters)


# 11.11.4 - Count characters and print them in decreasing frequency order.
def value_counts(text):
    """Count the letters in text, ignoring case and nonletters.

    >>> value_counts('Banana!')
    {'b': 1, 'a': 3, 'n': 2}
    """
    counts = {}
    for letter in text.lower():
        if letter.isalpha():
            counts[letter] = counts.get(letter, 0) + 1
    return counts


def frequency(item):
    """Return the count from a (letter, count) pair."""
    return item[1]


def most_frequent_letters(text):
    """Print letters and their counts, highest count first.

    >>> most_frequent_letters('banana')
    a: 3
    n: 2
    b: 1
    """
    counts = value_counts(text)
    ordered = sorted(counts.items(), key=frequency, reverse=True)
    for letter, count in ordered:
        print(f'{letter}: {count}')


# 11.11.5 - Group words by their letters in alphabetical order.
def find_anagram_groups(words):
    """Return groups containing at least two anagram words.

    >>> find_anagram_groups(['stop', 'pots', 'tops', 'tame', 'meat', 'apple'])
    [['stop', 'pots', 'tops'], ['tame', 'meat']]
    >>> find_anagram_groups(['cat', 'dog'])
    []
    """
    grouped = {}
    for word in words:
        signature = ''.join(sorted(word.lower()))
        if signature not in grouped:
            grouped[signature] = []
        grouped[signature].append(word)

    matches = []
    for group in grouped.values():
        if len(group) > 1:
            matches.append(group)
    return matches


def print_anagram_groups(groups):
    """Print all anagram groups, one list per line."""
    for group in groups:
        print(group)


# 11.11.6 - Zip matching positions and count the differences.
def word_distance(word1, word2):
    """Return the number of mismatched positions in equal-length words.

    >>> word_distance('cat', 'car')
    1
    >>> word_distance('converse', 'conserve')
    2
    >>> word_distance('same', 'same')
    0
    >>> word_distance('cat', 'cats')
    Traceback (most recent call last):
    ...
    ValueError: Both words must be the same length.
    """
    if len(word1) != len(word2):
        raise ValueError('Both words must be the same length.')
    differences = 0
    for first, second in zip(word1, word2):
        if first != second:
            differences += 1
    return differences


# 11.11.7 - Metathesis pairs are anagrams differing in exactly 2 places.
def find_metathesis_pairs(anagram_groups):
    """Find pairs that differ by one swap of two letters.

    >>> find_metathesis_pairs([['stop', 'spot', 'pots'], ['converse', 'conserve']])
    [('stop', 'spot'), ('converse', 'conserve')]
    >>> find_metathesis_pairs([['abc', 'bca']])
    []
    """
    pairs = []
    for group in anagram_groups:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if word_distance(group[i], group[j]) == 2:
                    pairs.append((group[i], group[j]))
    return pairs


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
    print(f'Chapter 11 doctests: {results.attempted} run, {results.failed} failed')
    print('Tuple containing modified list:', tuple_with_mutable_lists())
    try:
        unhashable_tuple_example()
    except TypeError as error:
        print('Tuple used as dictionary key:', type(error).__name__, '-', error)
    print('Caesar cipher: cheer + 7 =', shift_word('cheer', 7))
    print('Caesar cipher: melon + 16 =', shift_word('melon', 16))
    print('Letter frequencies for banana:')
    most_frequent_letters('banana')
    print('Word distance, converse/conserve:', word_distance('converse', 'conserve'))
    print('Simple metathesis example:',
          find_metathesis_pairs([['converse', 'conserve']]))

    if os.path.isfile('words.txt'):
        words = load_words('words.txt')
        groups = find_anagram_groups(words)
        metathesis_pairs = find_metathesis_pairs(groups)
        print('Words loaded:', len(words))
        print('Anagram groups (2 or more words):', len(groups))
        print('First 10 anagram groups:', groups[:10])
        print('Metathesis pairs:', len(metathesis_pairs))
        print('First 10 metathesis pairs:', metathesis_pairs[:10])
        # The book asks to print ALL anagram groups. Uncomment the next line
        # to see every group (the complete word list creates lots of output).
        # print_anagram_groups(groups)
    else:
        print('Place words.txt in this project for full anagram searches.')


if __name__ == '__main__':
    main()
