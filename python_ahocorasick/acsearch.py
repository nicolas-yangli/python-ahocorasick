from .trie import TrieNode


class AcSearch(object):
    def __init__(self, keywords):
        self._trieArray = self._constructTrie(keywords)
        self._fail, self._out = self._calculateFunctions(self._trieArray)
        
    @classmethod
    def _constructTrie(cls, keywords):
        trieArray = list()
        root = TrieNode()
        trieArray.append(root)
        for keyword in keywords:
            node = root
            for c in keyword:
                if c not in node.children:
                    newNode = TrieNode()
                    trieArray.append(newNode)
                    node.children[c] = len(trieArray) - 1
                    node = newNode
            node.out = keyword
        return trieArray
        
    @classmethod
    def _calculateFunctions(cls, trieArray):
        fail = [None] * len(trieArray)
        out = [None] * len(trieArray)
        queue = list()
        root = trieArray[0]
        fail[0] = 0
        for qIndex in root.children.values():
            fail[qIndex] = 0
            queue.append(qIndex)
        while len(queue) > 0:
            rIndex = queue.pop(0)
            r = trieArray[rIndex]
            for c, uIndex in r.children.items():
                u = trieArray[uIndex]
                queue.append(uIndex)
                vIndex = fail[rIndex]
                v = trieArray[vIndex]
                while c not in v.children:
                    if vIndex == 0:
                        break;
                    vIndex = fail[vIndex]
                    v = trieArray[vIndex]
                try:
                    fail[uIndex] = v.children[c]
                except KeyError:
                    assert vIndex == 0
                    fail[uIndex] = 0
                out[uIndex] = u.out
                if out[uIndex] is None:
                    out[uIndex] = out[fail[uIndex]]
        return fail, out
        
    def search(self, data):
        trieArray = self._trieArray
        fail = self._fail
        out = self._out
        qIndex = 0
        q = trieArray[qIndex]
        for i, c in enumerate(data):
            while c not in q.children:
                if qIndex == 0:
                    break;
                qIndex = fail[qIndex]
                q = trieArray[qIndex]
            try:
                qIndex = q.children[c]
            except KeyError:
                assert qIndex == 0
            q = trieArray[qIndex]
            out_keyword = out[qIndex]
            if out_keyword is not None:
                yield out_keyword, i+1-len(out_keyword)