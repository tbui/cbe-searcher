#!/usr/bin/env python

import unittest
from searcher import TextSearcher
from tokenizer import TextTokenizer


class TextSearcherTest(unittest.TestCase):
    '''
    Unit tests for TextSearcher. Don't modify this file.
    '''

    def testOneHitNoContext(self):
        '''
        Simplest possible case, no context and the word occurs exactly once.
        '''
        expected = ["sketch"]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("sketch", 0)
        self.assertEqual(expected, results)

    def testMultipleHitsNoContext(self):
        '''
        Next simplest case, no context and multiple hits.
        '''
        expected = ["naturalists", "naturalists"]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("naturalists", 0)
        self.assertEqual(expected, results)

    def testBasicSearch(self):
        '''
        This is the example from the document.
        '''
        expected = [
                "great majority of naturalists believed that species",
                "authors.  Some few naturalists, on the other" ]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("naturalists", 3)
        self.assertEqual(expected, results)

    def testBasicMoreContext(self):
        '''
        Same as basic search but a little more context.
        '''
        expected = [
                "Until recently the great majority of naturalists believed that species were immutable productions",
                "maintained by many authors.  Some few naturalists, on the other hand, have believed" ]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("naturalists", 6)
        self.assertEqual(expected, results)

    def testApostropheQuery(self):
        '''
        Tests query word with apostrophe.
        '''
        expected = [
                "not indeed to the animal's or plant's own good",
                "habitually speak of an animal's organisation as\nsomething plastic" ]
        searcher = TextSearcher("files/long_excerpt.txt")
        results = searcher.search("animal's", 4)
        self.assertEqual(expected, results)

    def testNumericQuery(self):
        '''
        Tests numeric query word.
        '''
        expected = [
                "enlarged in 1844 into a",
                "sketch of 1844--honoured me" ]
        searcher = TextSearcher("files/long_excerpt.txt")
        results = searcher.search("1844", 2)
        self.assertEqual(expected, results)

    def testMixedQuery(self):
        '''
        Tests mixed alphanumeric query word.
        '''
        expected = [ "date first edition [xxxxx10x.xxx] please check" ]
        searcher = TextSearcher("files/long_excerpt.txt")
        results = searcher.search("xxxxx10x", 3)
        self.assertEqual(expected, results)

    def testCaseInsensitiveSearch(self):
        '''
        Should get same results regardless of case.
        '''
        expected = [
                "on the Origin of Species.  Until recently the great",
                "of naturalists believed that species were immutable productions, and",
                "hand, have believed that species undergo modification, and that" ]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("species", 4)
        self.assertEqual(expected, results)
        
        results = searcher.search("SPECIES", 4)
        self.assertEqual(expected, results)
        
        results = searcher.search("SpEcIeS", 4)
        self.assertEqual(expected, results)

    def testNearBeginning(self):
        '''
        Hit that overlaps file start should still work.
        '''
        expected = [ "I will here give a brief sketch" ]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("here", 4)
        self.assertEqual(expected, results)

    def testNearEnd(self):
        '''
        Hit that overlaps file end should still work.
        '''
        expected = [
                "and that the existing forms of life",
                "generation of pre existing forms." ]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("existing", 3)
        self.assertEqual(expected, results)

    def testMultipleSearches(self):
        '''
        Searcher can execute multiple searches after initialization.
        '''
        searcher = TextSearcher("files/short_excerpt.txt")

        # Just runs the same queries as other tests, but on a single TextSearcher instance:
        expected = [
                "on the Origin of Species.  Until recently the great",
                "of naturalists believed that species were immutable productions, and",
                "hand, have believed that species undergo modification, and that" ]
        results = searcher.search("species", 4)
        self.assertEqual(expected, results)
        
        expected = [ "I will here give a brief sketch" ]
        results = searcher.search("here", 4)
        self.assertEqual(expected, results)

        expected = [
                "and that the existing forms of life",
                "generation of pre existing forms." ]
        results = searcher.search("existing", 3)
        self.assertEqual(expected, results)

    def testOverlappingHits(self):
        '''
        Overlapping hits should just come back as separate hits.
        '''
        expected = [
                "of naturalists believed that species were immutable",
                "hand, have believed that species undergo modification",
                "undergo modification, and that the existing forms" ]
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("that", 3)
        self.assertEqual(expected, results)

    def testNoHits(self):
        '''
        If no hits, get back an empty array.
        '''
        searcher = TextSearcher("files/short_excerpt.txt")
        results = searcher.search("slejrlskejrlkajlsklejrlksjekl", 3)
        self.assertEqual(0, len(results))

    def testTokenizer(self):
        '''
        Verify the tokenizer. This should always pass.
        '''
        file_contents = "123, 789: def"
        # In this test we define words to be strings of digits
        expected = [ "123", ", ", "789", ": def" ]
        tokenizer = TextTokenizer(file_contents, "[0-9]+")
        results = list()
        for token in tokenizer:
            results.append(token)
        self.assertEqual(expected, results)
        
        self.assertTrue(tokenizer.is_word("1029384"))
        self.assertTrue(tokenizer.is_word("1029388 "))
        self.assertTrue(tokenizer.is_word("123,456"))
