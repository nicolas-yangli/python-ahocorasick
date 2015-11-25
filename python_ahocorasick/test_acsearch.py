import unittest

from python_ahocorasick.acsearch import AcSearch


class TestAcSearch(unittest.TestCase):
    def test_search_unicode(self):
        content = u'我能吞下玻璃而不伤身体'
        keywords = (u'伤身体', u'玻璃')
        acSearch = AcSearch(keywords)
        result =  list(acSearch.search(content))
        self.assertEqual(2, len(result))
        self.assertEqual((u'玻璃', 4), result[0])
        self.assertEqual((u'伤身体', 8), result[1])
        
    def test_search_bytes(self):
        content = u'我能吞下玻璃而不伤身体'.encode('utf-8')
        keywords = (u'伤身体', u'玻璃')
        acSearch = AcSearch((keyword.encode('utf-8') for keyword in keywords))
        result =  list(acSearch.search(content))
        self.assertEqual(2, len(result))
        self.assertEqual(u'玻璃'.encode('utf-8'), result[0][0])
        self.assertEqual(u'伤身体'.encode('utf-8'), result[1][0])
        
    def test_multiple_appearance(self):
        content = 'abcabca'
        keywords = ('bc',)
        acSearch = AcSearch(keywords)
        result =  list(acSearch.search(content))
        self.assertEqual(2, len(result))
        self.assertEqual(('bc', 1), result[0])
        self.assertEqual(('bc', 4), result[1])
        
    def test_fail_function(self):
        content = 'ababacbbacb'
        keywords = ('abac',)
        acSearch = AcSearch(keywords)
        result =  list(acSearch.search(content))
        self.assertEqual(1, len(result))
        self.assertEqual(('abac', 2), result[0])
        
    def test_appearance_overlap(self):
        content = 'ababacb'
        keywords = ('abac','bacb')
        acSearch = AcSearch(keywords)
        result =  list(acSearch.search(content))
        self.assertEqual(2, len(result))
        self.assertEqual(('abac', 2), result[0])
        self.assertEqual(('bacb', 3), result[1])
        
    def test_keyword_prefix(self):
        content = 'abcdef'
        keywords = ('ab', 'abc')
        acSearch = AcSearch(keywords)
        result =  list(acSearch.search(content))
        self.assertEqual(2, len(result))
        self.assertEqual(('ab', 0), result[0])
        self.assertEqual(('abc', 0), result[1])
        
    def test_keyword_suffix(self):
        content = 'abcdef'
        keywords = ('bc', 'abc')
        acSearch = AcSearch(keywords)
        result =  list(acSearch.search(content))
        self.assertEqual(1, len(result))
        self.assertEqual(('abc', 0), result[0])
        
    def test_search_minibatch(self):
        batchs = ('我能吞', '下玻璃', '而不伤', '身体')
        keywords = ('吞下', '伤身体', '玻璃')
        acSearch = AcSearch(keywords)
        result = list(acSearch.search_minibatch(batchs))
        self.assertEqual(3, len(result))
        self.assertEqual('吞下', result[0])
        self.assertEqual('玻璃', result[1])
        self.assertEqual('伤身体', result[2])