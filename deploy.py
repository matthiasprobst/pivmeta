"""semi manual task

Running this script will create a the documentation for a new version of the ontology.

So first change the ttl file with Protege (https://protege.stanford.edu/), then change the version string in this script
(see in bottom of the script) and then run the script.
"""

import datetime
import logging
import pathlib
import shutil
import subprocess
import sys

import yaml
from pivmetalib.qudt.unit import qudt_lookup

sys.path.insert(0, '.')

DEFAULT_LOGGING_LEVEL = logging.DEBUG
_formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S')

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(DEFAULT_LOGGING_LEVEL)
_stream_handler.setFormatter(_formatter)

logger = logging.getLogger('pivmeta')
logger.addHandler(_stream_handler)
logger.setLevel(DEFAULT_LOGGING_LEVEL)

__this_dir__ = pathlib.Path(__file__).parent

ONTOLOGY_NAME = 'pivmeta'


def copy_version_to_docs(version_string):
    version_path = __this_dir__ / 'docs' / version_string.strip('v')
    target_path = __this_dir__ / 'docs'
    version_path.mkdir(exist_ok=True, parents=True)
    assert version_path.exists()
    assert version_path.is_dir()

    target_path.mkdir(exist_ok=True, parents=True)

    logger.debug(f'copying version to docs {version_path} -> {target_path}')
    shutil.copytree(version_path, target_path, dirs_exist_ok=True)
    index_en = target_path / 'index-en.html'

    (target_path / 'index.html').unlink(missing_ok=True)
    index_en.rename(target_path / 'index.html')

    (target_path / f'{ONTOLOGY_NAME}.jsonld').unlink(missing_ok=True)
    (target_path / f'{ONTOLOGY_NAME}.nt').unlink(missing_ok=True)
    (target_path / f'{ONTOLOGY_NAME}.ttl').unlink(missing_ok=True)
    (target_path / f'{ONTOLOGY_NAME}.owl').unlink(missing_ok=True)
    (target_path / 'ontology.jsonld').rename(target_path / f'{ONTOLOGY_NAME}.jsonld')
    (target_path / 'ontology.nt').rename(target_path / f'{ONTOLOGY_NAME}.nt')
    (target_path / 'ontology.ttl').rename(target_path / f'{ONTOLOGY_NAME}.ttl')
    (target_path / 'ontology.owl').rename(target_path / f'{ONTOLOGY_NAME}.owl')

    vers_index_en = version_path / 'index-en.html'
    assert vers_index_en.exists()
    vers_index_en.with_name('index.html').unlink(missing_ok=True)
    vers_index_en.rename(vers_index_en.with_name('index.html'))

    (version_path / f'{ONTOLOGY_NAME}.jsonld').unlink(missing_ok=True)
    (version_path / f'{ONTOLOGY_NAME}.nt').unlink(missing_ok=True)
    (version_path / f'{ONTOLOGY_NAME}.ttl').unlink(missing_ok=True)
    (version_path / f'{ONTOLOGY_NAME}.owl').unlink(missing_ok=True)
    (version_path / 'ontology.jsonld').rename(version_path / f'{ONTOLOGY_NAME}.jsonld')
    (version_path / 'ontology.nt').rename(version_path / f'{ONTOLOGY_NAME}.nt')
    (version_path / 'ontology.ttl').rename(version_path / f'{ONTOLOGY_NAME}.ttl')
    (version_path / 'ontology.owl').rename(version_path / f'{ONTOLOGY_NAME}.owl')

    assert index_en.exists() is False
    logger.debug('done copying version to docs')


def create_version(version_folder, version_string, previousVersionURI: str = None):
    assert version_string.startswith('v')
    # call batch script build.bat
    logger.info('Start building docs')

    logger.debug('Running tests...')
    subprocess.run(['python', 'tests/test_graph.py'])
    subprocess.run(['python', 'tests/test_context.py'])

    logger.debug('update modification data')
    # open widoco config file
    widico_cfg_filename = version_folder / 'widoco.cfg'
    assert widico_cfg_filename.exists()

    with open(widico_cfg_filename, 'r', encoding='utf-8') as f:
        lines = [l.strip().split('=') for l in f.readlines()]

    cfg_data = {l[0]: l[1] for l in lines if len(l) == 2}
    today = datetime.datetime.today()
    # cfg_data['dateCreated'] = today.strftime('%Y-%m-%d')
    cfg_data['dateModified'] = today.strftime('%Y-%m-%d')
    cfg_data['ontologyRevisionNumber'] = version_string
    if previousVersionURI:
        cfg_data['previousVersionURI'] = previousVersionURI

    def read_lines(filename) -> str:
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
            return '<br>'.join([l.strip() for l in lines])

    cfg_data['abstract'] = read_lines(__this_dir__ / 'documentation' / 'Abstract.md')
    cfg_data['introduction'] = read_lines(__this_dir__ / 'documentation' / 'Introduction.md')
    cfg_data['description'] = read_lines(__this_dir__ / 'documentation' / 'Description.md')
    cfg_data['thisVersionURI'] = f'https://matthiasprobst.github.io/{ONTOLOGY_NAME}/{version_string.strip("v")}'
    cfg_data['authors'] = 'Matthias Probst (https://orcid.org/0000-0001-8729-0482), Karlsruhe Institute ' \
                          'of Technology, Institute of Thermal Turbomachinery'

    cfg_data['citeAs'] = 'Matthias Probst (https://orcid.org/0000-0001-8729-0482), Karlsruher Institute ' \
                         f'of Technology, Institute of Thermal Turbomachinery. {ONTOLOGY_NAME}: A simple Standard ' \
                         f'Name Ontology. Revision: {version_string}. Retrieved from: ' \
                         f'https://matthiasprobst.github.io/{ONTOLOGY_NAME}/{version_string.strip("v")}'

    with open(widico_cfg_filename, 'w', encoding='utf-8') as f:
        for k, v in cfg_data.items():
            f.write(f'\n{k}={v}')

    script_path = __this_dir__ / 'build_onto_doc.bat'
    logger.debug(f'calling script {script_path.absolute()}')
    # open script and replace <version> with version_string
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.replace('<version>', version_string.strip('v')) for l in lines]

    # write script to file
    script_path_vers = __this_dir__ / 'build_onto_doc_tmp.bat'
    with open(script_path_vers, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    subprocess.run(str(script_path_vers.absolute()))

    from generate_context import generate

    generate(version_folder / f'{ONTOLOGY_NAME}.ttl')

    copy_version_to_docs(version_string)

    script_path_vers.unlink(missing_ok=True)
    logger.info('Finished building docs')


if __name__ == "__main__":

    version_string = 'v1.0.0'

    # call batch script build.bat
    logger.info('Start building docs')

    logger.debug('Adding standard names to .ttl file from table')
    orig_ttl = __this_dir__ / 'pivmeta_orig.ttl'
    pub_ttl = __this_dir__ / 'pivmeta.ttl'
    snt_path = __this_dir__ / 'standard_name_table.yaml'

    logger.debug(' > copy original ttl file')
    shutil.copy(orig_ttl, pub_ttl)

    logger.debug(' > read standard name table')
    with open(snt_path, 'r') as f:
        snt_doc = yaml.safe_load(f)

    standard_names = snt_doc['standard_names']

    logger.debug(' > add standard names')
    with open(pub_ttl, 'a') as f:
        f.write(f'\n\n### Standard Names automatically added by pivmeta repo script')
        for k, v in standard_names.items():
            desc = v['description']
            units = v['units']
            qudt_units = None
            if units.strip() != '':
                qudt_units = qudt_lookup.get(units, None)
                if qudt_units is None:
                    raise KeyError(f'Cannot determine qudt unit from "{units}"')
            f.write(f'\n\n### https://matthiasprobst.github.io/pivmeta#{k}')
            f.write(f'\npivmeta:{k} rdf:type owl:NamedIndividual ,')
            f.write(f'\n             <https://matthiasprobst.github.io/pivmeta#StandardName> ;')
            f.write(f'\n             <http://purl.org/dc/terms/description> "{desc}"@en ;')
            f.write(f'\n             <https://matthiasprobst.github.io/ssno#standardName> "{k}" ;')
            if qudt_units:
                f.write(f'\n             <https://matthiasprobst.github.io/ssno#unit> <{qudt_units}> ;')
            f.write(f'\n             <http://www.w3.org/2004/02/skos/core#prefLabel> "{k}"@en .\n')

    force = True
    version_dir = __this_dir__ / 'docs' / version_string.strip('v')
    if version_dir.exists() and not force:
        raise ValueError(f'Version {version_dir} already exists. You might be about to create '
                         f'a new version. Please provide a new version number if something has changed!.')

    create_version(__this_dir__, version_string, previousVersionURI=None)
    # create_version(__this_dir__, 'v1.1.0',
    #                previousVersionURI=f'https://matthiasprobst.github.io/{ONTOLOGY_NAME}/1.0.0')
