"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import json
import pathlib
import rdflib
import unittest
import yaml

__this_dir__ = pathlib.Path(__file__).parent


class TestContext(unittest.TestCase):

    def setUp(self) -> None:
        snt_path = __this_dir__.parent / 'standard_name_table.yaml'

        with open(snt_path, 'r', encoding='utf-8') as f:
            snt_doc = yaml.safe_load(f)
        self.standard_name_dict = snt_doc['standard_names']


    def test_sn_in_ttl(self):
        pivmeta_onto_file = __this_dir__.parent / 'pivmeta.ttl'
        g = rdflib.Graph()
        g.parse(pivmeta_onto_file)

        entity = "owl:NamedIndividual"
        query: str = (f"""SELECT ?id ?label ?type# ?description
                WHERE {{
                    ?id rdf:type {entity} .
                    ?id rdf:type pivmeta:StandardName .
                    ?id skos:prefLabel ?label.
                    # ?id skos:description ?description.
                    OPTIONAL {{?id rdfs:range ?type .}}.
                }}
                    """)
        query_result = g.query(query)
        for _id, _label, _type in query_result:
            self.assertIn(str(_label), self.standard_name_dict)
