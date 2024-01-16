import sys

from rdflib import Graph

sys.path.insert(0, '.')
from utils import merge_jsonld_files


def get_datasets(json_filename):
    g = Graph()
    g.parse(json_filename, format='json-ld')
    g.serialize(
        json_filename, format='json-ld',
        context={
            "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld"
        }
    )

    query_str = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX pivm: <https://matthiasprobst.github.io/pivmeta#>

        SELECT ?ds ?distribution ?creator ?mbox ?url ?mediatype
        WHERE {
            ?ds a dcat:Dataset .
            ?ds dcat:creator ?creator .
            ?ds dcat:distribution ?distribution .
            ?distribution dcat:mediaType ?mediatype .
            ?distribution dcat:downloadURL ?url .
            OPTIONAL { ?creator foaf:mbox ?mbox . }
            FILTER regex(?mediatype, "application/zip", "i")
    }
    """  # https://jena.apache.org/tutorials/sparql_filters.html

    return [(str(row.ds), str(row.mbox), str(row.url)) for row in g.query(query_str)]


# def get_distribution(dataset_id):
#     assert pathlib.Path('sample_piv.json').exists()
#     g = Graph()
#     g.parse('piv_challenge_data.json', format='json-ld')
#     g.serialize(json_filename, format='json-ld',
#                 context={
#                     "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld"
#                 }
#                 )
#
#     query_str = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
#         PREFIX pivm: <https://matthiasprobst.github.io/piv-convention#>
#
#         SELECT ?distribution
#         WHERE {
#             ?distribution a dcat:Distribution ;
#                 dcat:Dataset """ + dataset_id + """ .
#
#     }
#     """
#
#     return [str(row.distribution) for row in g.query(query_str)]
#
#     # g = Graph()
#     # g.parse('sample_piv.json', format='json-ld')
#     #
#     # g.serialize('sample_piv_out.json', format='json-ld',
#     #             context={"dct": "http://purl.org/dc/terms/",
#     #                      "dcat": "http://www.w3.org/ns/dcat#",
#     #                      "obo": "http://purl.obolibrary.org/obo/",
#     #                      "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld"
#     #                      }
#     #             )
#     #


if __name__ == '__main__':
    merge_jsonld_files(
        ['piv_challenge/piv_challenge_1A.json',
         'piv_challenge/piv_challenge_1B.json',
         'piv_challenge/piv_challenge_1C.json',
         'piv_challenge/piv_challenge_1E.json'],
        'piv_challenge/piv_challenge_data.json')
    datasets = get_datasets('piv_challenge/piv_challenge_data.json')
    for ds in datasets:
        print(ds)

    # print(get_distribution(datasets[0]))
