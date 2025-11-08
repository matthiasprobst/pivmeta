"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import unittest
from pathlib import Path

import rdflib
from rdflib import Graph


class TestGraph(unittest.TestCase):

    def test_standard_names(self):
        rdflib.Graph()
        m4i = Path(__file__).parent.parent / 'pivmeta.ttl'
        onto_purl = str(m4i)

        g = Graph()
        g.parse(onto_purl, format="ttl")
        sparql_query = """
        PREFIX ssno: <https://matthiasprobst.github.io/ssno#>
        PREFIX piv: <https://matthiasprobst.github.io/pivmeta#>
        
        SELECT ?standard_name ?description ?unit
        WHERE {
            ?standard_name a ssno:StandardName ;
                <http://purl.org/dc/terms/description> ?description ;
                ssno:standardName ?standard_name ;
                ssno:canonicalUnits ?unit .
        }
        """
        qres = g.query(sparql_query)
        for row in qres:
            assert len(row) == 3, f'Error: {row} is not a tuple of length 3'
            assert isinstance(row[0], rdflib.URIRef), f'Error: {row[0]} is not a URIRef'
            assert isinstance(row[1], rdflib.Literal), f'Error: {row[1]} is not a Literal'
            assert isinstance(row[2], rdflib.URIRef), f'Error: {row[2]} is not a URIRef'

    def test_graph(self):
        print('Start testing graph')
        m4i = Path(__file__).parent.parent / 'pivmeta.ttl'

        onto_purl = str(m4i)

        g = Graph()
        g.parse(onto_purl, format="ttl")
        for s, p, o in g:
            print(s, p, o)

            assert isinstance(p, rdflib.URIRef), f'Error: {s} is not a URIRef'
            if (p not in (rdflib.RDF.first, rdflib.RDF.rest,
                         rdflib.OWL.members,
                         rdflib.OWL.onClass,
                         rdflib.OWL.onDataRange,
                         rdflib.OWL.cardinality,
                         rdflib.OWL.hasValue,
                         rdflib.OWL.qualifiedCardinality,
                         rdflib.URIRef("http://www.w3.org/2002/07/owl#minQualifiedCardinality"),
                         rdflib.OWL.unionOf) and o != rdflib.OWL.Class
                    and o != rdflib.OWL.Restriction
                    and o != rdflib.RDFS.Datatype
                    and p != rdflib.OWL.onProperty
                    and p != rdflib.OWL.inverseOf
                    and p != rdflib.OWL.someValuesFrom
                    and p != rdflib.OWL.allValuesFrom):
                if o not in rdflib.OWL.AllDisjointClasses:
                    assert isinstance(s, rdflib.URIRef), f'Error: {s} is not a URIRef ({s}, {p}, {o})'
        assert len(g) > 0, f'Error: No triples found in {onto_purl}.'
        assert g, f'Error: {onto_purl} is not a graph'
