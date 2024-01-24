"""The method generate() is largely taken from https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/1.2.1/ci/generate_context_file.py
and only slightly adjusted. The original code is licensed under the CC-BY-4 license."""
import hashlib
import json
import pathlib
import warnings

import requests
from rdflib import Graph
from rdflib.namespace import NamespaceManager
from rdflib.term import URIRef

__this_dir__ = pathlib.Path(__file__).parent


def download_file(url, known_hash, target=None):
    """Download a file from a URL and check its hash"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        content = response.content

        # Calculate the hash of the downloaded content
        calculated_hash = hashlib.sha256(content).hexdigest()
        if known_hash:
            if not calculated_hash == known_hash:
                raise ValueError('File does not match the expected has')
        else:
            warnings.warn('No hash given!')

        # Save the content to a file
        if target is None:
            target = __this_dir__ / '.tmp_file'
        else:
            target = pathlib.Path(target)
        with open(target, "wb") as f:
            f.write(content)

        return target
    raise RuntimeError(f'Failed to download the file from {url}')


def generate():
    """Download m4i context file, take it as basis and add pivmeta entities to it."""

    # download m4i:
    m4i_context_url = 'https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/raw/master/m4i_context.jsonld'
    m4i_context_file = __this_dir__ / 'm4i_context.jsonld'

    download_file(m4i_context_url, None, m4i_context_file)
    with open(m4i_context_file, 'r', encoding="utf-8") as f:
        m4i_context_data = json.load(f)['@context']
    m4i_context_data.pop('@vocab')

    ssno = __this_dir__ / 'pivmeta.ttl'
    assert ssno.exists()
    context_file = __this_dir__ / 'pivmeta_context.jsonld'

    g = Graph()
    g.parse(str(ssno))

    outfile = str(context_file)
    with open(outfile, "w", encoding="utf-8") as f:
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
            query: str = (f"""SELECT ?id ?label ?type
        WHERE {{
            ?id rdf:type {entity} .
            ?id skos:prefLabel ?label.
            OPTIONAL {{?id rdfs:range ?type .}}.
        }}
            """)
            # query: str = ('SELECT ?id ?label ?type\n'
            #               'WHERE {\n'
            #               f'  ?id rdf:type {entity} .\n'
            #               '  ?id skos:prefLabel ?label.\n'
            #               '  OPTIONAL {?id rdfs:range ?type .}. \n'
            #               '}')
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

    with open(outfile, 'r', encoding="utf-8") as f:
        context = json.load(f)

    # add m4i key-values
    for key, value in m4i_context_data.items():
        if key not in context['@context']:
            context['@context'][key] = value
        else:
            print(f'"{key}" is already used as a label, therefore {value} will be skipped')

    with open(outfile, 'w', encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)

    g.parse(outfile, format='json-ld')

    assert g, f'Error: generated context file has syntax errors'
    m4i_context_file.unlink()


if __name__ == '__main__':
    generate()
