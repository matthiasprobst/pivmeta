"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import rdflib
import unittest
from pathlib import Path
from rdflib import Graph


class TestClasses(unittest.TestCase):

    def test_graph(self):
        print('Start testing graph')
        m4i = Path(__file__).parent.parent / 'pivmeta.ttl'

        onto_purl = str(m4i)

        g = Graph()
        g.parse(onto_purl, format="ttl")
        for s, p, o in g:
            print(s, p, o)
            assert isinstance(s, rdflib.URIRef), f'Error: {s} is not a URIRef'
            assert isinstance(p, rdflib.URIRef), f'Error: {s} is not a URIRef'
            assert isinstance(p, str), f'Error: {s} is not a str'
        assert len(g) > 0, f'Error: No triples found in {onto_purl}.'
        assert g, f'Error: {onto_purl} is not a graph'
