import pathlib

from rdflib import Graph

__this_dir__ = pathlib.Path(__file__).parent


def merge_jsonld_files(list_of_filenames, output_filename):
    """merges list of json ld files into one json ld file"""
    g = Graph()
    for filename in list_of_filenames:
        g.parse(filename, format='json-ld')
    g.serialize(
        output_filename, format='json-ld',
        context={
            "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld"
        }
    )
