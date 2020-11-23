#!/usr/bin/env python
import re

PUNCTUATIONS = '.,;?!'


def log_info(match, index):
    print("Found matching pattern: '{0}', at index {1}".format(match, index))


def strip_punctuation_ending(text):
    """ strip the trailing punctuation """
    stripped = text
    if text[-1] in PUNCTUATIONS:
        stripped = text[:(len(text) - 1)]
    return stripped


class TextSearcher:
    '''
    TextSearcher implements a search interface to an underlying text file
    consisting of the single method search(str, int).
    '''

    def __init__(self, file_name):
        '''
        Initializes the text searcher with the contents of a text file. The
        current implementation just reads the contents into a string and passes
        them to initialize(file_contents).
        
        You may modify this implementation if you need to.
        '''
        with open(file_name) as f:
            self.initialize(f.read())
            f.close()

    def initialize(self, file_contents):
        '''
        Initializes any internal data structures that are needed for this class
        to implement search efficiently.
        
        :param file_contents: The full scope of the content to be searched
        :type file_contents: str
        '''
        self.file_contents = file_contents

    def search(self, query_word, num_context_words):
        '''
        Searches for instances of the given word with surrounding context.
        
        :param query_word: The word to search for in the file contents
        :type query_word: str
        :param num_context_words: The number of words of context to provide on each side of the query word
        :type num_context_words: int
        :return: One context string for each time the query word appears in the file
        :rtype: list
        '''

        # sanity check
        if len(query_word) > len(self.file_contents):
            return []

        matches = []

        if num_context_words > 0:

            # Split the matching into the preceding pattern before the query word and the following pattern after
            # the query word

            preceding_pattern = '(\S+\s+){{0,{1}}}((?:\S+)?{0}(?:\S+)?)'.format(query_word, num_context_words)
            preceding_match_indices = self.get_indexes(self.match(preceding_pattern))
            following_pattern = '((?:\S+)?{0}(?:.)?(?:,)?(?:)?(?:\'\w)?)((?:\s+)?\S+){{0,{1}}}'.format(query_word,
                                                                                                       num_context_words)
            following_match_indices = self.get_indexes(self.match(following_pattern))

            # get the merged overlapping matches
            matches = self.get_merged_matches(preceding_match_indices, following_match_indices, query_word)
        else:
            for m in self.match(query_word):
                log_info(m.group(), m.start())
                matches.append(m.group())

        return matches

    def match(self, pattern):
        """
        Perform regex matching
        :param pattern: the pattern to match
        :type pattern: str
        :return: a list of matches
        :rtype: list
        """
        return re.finditer(pattern, self.file_contents, re.IGNORECASE)

    def get_indexes(self, matches):
        """
        Return a list of that contains the starting and ending indices for the matched pattern
        :param matches: iterable match object
        :return: list containing (starting index, ending index) of the matched pattern
        """
        indices = []
        for m in matches:
            index = (m.start(), m.end())
            if index not in indices:
                indices.append(index)
        return indices

    def get_merged_matches(self, preceding_match_indices, following_match_indices, query_word):
        """
        Take the indices from the preceding and following matched patterns and form a
        full matching pattern by slicing the text from the start of the preceding pattern and
        the end of the following pattern
        :param preceding_match_indices:
        :param following_match_indices:
        :param query_word:
        :return:
        """
        matches = []

        # Determine if the preceding pattern and the following pattern overlap, merge if they do
        # and record the full  pattern in the matches list
        for (preceding_match_start, preceding_match_end) in preceding_match_indices:
            for (following_match_start, following_match_end) in following_match_indices:
                if preceding_match_start < following_match_start - len(query_word) < preceding_match_end:
                    text = self.file_contents[slice(preceding_match_start, following_match_end)]
                    # Making the assumption that if the last word has a trailing punctuation,
                    # then remove. Exception is if the last word is the end of the file, then don't
                    # remove.
                    if following_match_end != len(self.file_contents):
                        text = strip_punctuation_ending(text)
                    matches.append(text)

        return matches
