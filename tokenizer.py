#!/usr/bin/env python

import re
import sys


class TextTokenizer:
    '''
    Iterator class which returns token strings from the input string.
    It must be initialized with a regular expression representing a word.
    Returned tokens will alternate between words (i.e. that match the regular expression)
    and intervening strings that are not words.
    
    The method is_word(str) can be used to check whether a given token is a word
    or an intervening token.
    
    To learn what regular expression syntax is supported by the Python platform,
    see the documentation for the 're' package.
    '''

    def __init__(self, input, regex_str):
        '''
        Initializes the tokenizer with an input string and a regular expression
        representing a word.
        '''
        self.input = input
        self.regex = re.compile(regex_str)
        self.matching_iterator = self.regex.finditer(self.input)
        self.next_punctuation = None
        self.next_word = None
        self.previous_word_end = 0

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        '''
        Returns the next token if any more tokens are available.
        Otherwise raises StopIteration.
        '''
        if self.next_word is None and self.next_punctuation is None:
            self.retrieve_next()
        
        if self.next_punctuation is not None:
            ret = self.next_punctuation
            self.next_punctuation = None
            return ret
        
        if self.next_word is not None:
            ret = self.next_word
            self.next_word = None
            return ret
        
        raise StopIteration

    def retrieve_next(self):
        try:
            if sys.version_info > (3, 0):
                match = self.matching_iterator.__next__()
            else:
                match = self.matching_iterator.next()
            match_start = match.start()
            match_end = match.end()
            
            self.next_word = match.group()
            if match_start > self.previous_word_end:
                self.next_punctuation = self.input[self.previous_word_end:match_start]
            
            self.previous_word_end = match_end
        except StopIteration:
            if self.previous_word_end < len(self.input):
                self.next_punctuation = self.input[self.previous_word_end:len(self.input)]
                self.previous_word_end = len(self.input)

    def is_word(self, s):
        '''
        Returns true if the string matches this tokenizer's regular expression,
        otherwise returns false.
        '''
        return self.regex.match(s)

