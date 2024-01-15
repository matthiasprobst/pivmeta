"""This code is taken from https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/1.2.1/ci/generate_context_file.py
and only slightly adjusted. The original code is licensed under the CC-BY-4 license."""
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import NamespaceManager
from rdflib.term import URIRef

__this_dir__ = Path(__file__).parent


def generate():
    ssno = __this_dir__ / 'pivmeta.ttl'
    assert ssno.exists()
    context_file = __this_dir__ / 'pivmeta_context.jsonld'

    g = Graph()
    g.parse(str(ssno))

    outfile = str(context_file)
    f = open(outfile, "w", encoding="utf-8")
    f.write("{\n  \"@context\": {\n")

    nm = NamespaceManager(g)

    vocab_query = """
    SELECT ?id 
    WHERE {
    ?id rdf:type owl:Ontology .
    }"""

    query_result = g.query(vocab_query)

    for row in query_result:
        f.write(f'    "@vocab": "{row.id}"')

    for ns_prefix, namespace in g.namespaces():
        if ns_prefix.strip() != "":
            f.write(f',\n    "{ns_prefix}" : "{namespace}"')

    entities = [
        "owl:Class",
        "owl:AnnotationProperty",
        "rdfs:Datatype",
        "owl:ObjectProperty",
        "owl:DatatypeProperty",
        "owl:NamedIndividual"]

    ids = []

    for entity in entities:
        query: str = ('SELECT ?id ?label ?type\n'
                      'WHERE {\n'
                      f'  ?id rdf:type {entity} .\n'
                      '  ?id skos:prefLabel ?label.\n'
                      '  OPTIONAL {?id rdfs:range ?type .}. \n'
                      '}')
        print(f'*** Adding entities of type "{entity}" to the context file ***')
        query_result = g.query(query)

        print(f'Total: {len(query_result)}')
        for row in query_result:
            typestr = ""
            if type(row.type) == URIRef:
                typestr = f', "@type" : "{nm.normalizeUri(row.type)}"'
            #            print(row.id, row.type, type(row.type))
            if row.label not in ids:
                print(row.label)
                f.write(f',\n    "{row.label}" : {{"@id" : "{nm.normalizeUri(row.id)}"{typestr}}}')
                ids.append(row.label.lower())
            else:
                print(f'"{row.label}" is already used as a label, therefore {row.id} will be skipped')

    f.write("\n  }\n}")
    f.close()

    g.parse(outfile, format='json-ld')

    assert g, f'Error: generated context file has syntax errors'


if __name__ == '__main__':
    generate()
