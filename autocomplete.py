from collections import defaultdict
import heapq

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.sentence_count = defaultdict(int)

class AutocompleteSystem:
    def __init__(self, sentences: [str], times: [int]):
        self.root = TrieNode()
        self.input_string = ""
        self.curr_node = self.root
        for sentence, time in zip(sentences, times):
            self._add_sentence(sentence, time)

    def _add_sentence(self, sentence: str, time: int):
        node = self.root
        for char in sentence:
            node = node.children[char]
        node.sentence_count[sentence] += time

    def input(self, c: str) -> [str]:
        results = []
        if c == '#':
            self._add_sentence(self.input_string, 1)
            self.input_string = ""
            self.curr_node = self.root
            return results
        self.input_string += c
        if self.curr_node:
            self.curr_node = self.curr_node.children.get(c)
        if not self.curr_node:
            return results
        return self._search()

    def _search(self):
        node = self.curr_node
        heap = []
        for sentence, count in node.sentence_count.items():
            heapq.heappush(heap, (-count, sentence))
        top_results = []
        for _ in range(3):
            if heap:
                top_results.append(heapq.heappop(heap)[1])
        return top_results