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