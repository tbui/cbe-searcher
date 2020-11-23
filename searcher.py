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
        self.words = file_contents.split()

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

        self.matches = []
        self.min_start_idx = None
        self.max_end_idx = None

        if num_context_words > 0:
            # attempt to get match on the full pattern
            pattern = '(\S+\s+){{{1}}}(({0}.)|({0}))(\s+\S+){{{1}}}'.format(query_word, num_context_words)
            self.append_match(self.match(pattern))

            # account for when the query_word occurs at the start of the file
            pattern = '(\S+\s+){{1,{1}}}?(({0}.)|({0}))(\s+\S+){{{1}}}'.format(query_word, num_context_words)
            self.append_match(self.match(pattern))

            # account for when the query_word occurs at the end of the file
            pattern = '(\S+\s+){{{1}}}(({0}.)|({0}))(\s+\S+){{1,{1}}}?'.format(query_word, num_context_words)
            self.append_match(self.match(pattern))
        else:
            for m in self.match(query_word):
                log_info(m.group(), m.start())
                self.matches.append(m.group())

        return self.matches

    def match(self, pattern):
        """
        :param pattern: the pattern to match
        :type pattern: str
        :return: a list of matches
        :rtype: list
        """
        return re.finditer(pattern, self.file_contents, re.IGNORECASE)

    def append_match(self, matches):
        """
        Check if the match should be appended to the result list
        :param matches: Match object returned by re.finditer
        """
        append = False
        for m in matches:
            text = m.group()
            log_info(m.group(), m.start())
            """ 
            Check if the starting index has been recorded; this check is needed
            to verify if the matched pattern occurs at the start of the file.
            """
            if not self.min_start_idx or m.start() < self.min_start_idx:
                self.min_start_idx = m.start()
                append = True
            """ 
            Check if the ending index has been recorded; this check is needed
            to verify whether the matched pattern occurs at the end of the file.
            """
            if not self.max_end_idx or m.end() > self.max_end_idx:
                self.max_end_idx = m.end()
                append = True
            """
            Assumption: seems that if the matched text contains the last word in the file,
            then don't strip the trailing punctuation
            """
            if m.end() != len(self.file_contents):
                text = strip_punctuation_ending(text)

            if append is True:
                self.matches.append(text)
