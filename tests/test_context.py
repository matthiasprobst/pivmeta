"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import json
import pathlib
import unittest
import yaml

__this_dir__ = pathlib.Path(__file__).parent


class TestContext(unittest.TestCase):

    def test_sn_individuals(self):
        """The standard names defined in the standard name table YAML file
        are added automatically (see deploy.py) and should appear in the
        context.json file"""

        snt_path = __this_dir__.parent / 'standard_name_table.yaml'

        with open(snt_path, 'r', encoding='utf-8') as f:
            snt_doc = yaml.safe_load(f)
        standard_name_dict = snt_doc['standard_names']

        # read context.jsonld
        potential_sn_data_in_context = []
        with open(__this_dir__.parent / 'pivmeta_context.jsonld',
                  encoding='utf-8') as f:
            context_data = json.load(f)
            for k, v in context_data["@context"].items():
                if isinstance(v, dict):
                    if f"pivmeta:{k}" == v['@id']:
                        potential_sn_data_in_context.append(k)

        # all standard names must be in potential_sn_data_in_context:
        for k in standard_name_dict:
            self.assertIn(k, potential_sn_data_in_context)
