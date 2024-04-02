"""semi manual task

1. update the ontology in versions/X.X.X/ontology.ttl
2. run widoco
3. run this script
"""
import datetime
import logging
import pathlib
import shutil

import requests.exceptions
import yaml

from pivmetalib.qudt.unit import qudt_lookup

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


def copy_version_to_docs():
    """copy the latest version to docs/"""
    version_path = __this_dir__ / 'docs/versions' / '1.0.0'
    target_path = __this_dir__ / 'docs'

    assert version_path.exists()
    assert version_path.is_dir()

    target_path.mkdir(exist_ok=True, parents=True)

    shutil.copytree(version_path, target_path, dirs_exist_ok=True)
    index_en = target_path / 'index-en.html'
    (target_path / 'index.html').unlink()
    index_en.rename(target_path / 'index.html')
    assert index_en.exists() is False


if __name__ == "__main__":
    import sys
    import subprocess
    import configparser

    sys.path.insert(0, '.')
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

    logger.debug(' > update modification data')
    # open widoco config file
    cfg_file = __this_dir__ / 'widoco.cfg'
    config = configparser.ConfigParser()
    with open('widoco.cfg', 'r') as f:
        lines = [l.strip().split('=') for l in f.readlines()]

    cfg_data = {l[0]: l[1] for l in lines if len(l) == 2}
    today = datetime.datetime.today()
    cfg_data['dateModified'] = today.strftime('%Y-%m-%d')
    cfg_data['dateCreated'] = today.strftime('%Y-%m-%d')

    with open(cfg_file, 'w') as f:
        for k, v in cfg_data.items():
            f.write(f'\n{k}={v}')
    script_path = __this_dir__ / 'build_onto_doc.bat'
    logger.debug(f'calling script {script_path.absolute()}')
    subprocess.run(str(script_path.absolute()))

    from generate_context import generate

    logger.debug('Copy version to docs')
    copy_version_to_docs()

    logger.debug('Build context.jsonld')
    try:
        generate()
    except requests.exceptions.ConnectionError as e:
        logger.debug(f'Could not generate context.jsonld ue to missing internet connection: {e}')

    logger.info('Finished building docs')
