"""semi manual task

1. update the ontology in versions/X.X.X/ontology.ttl
2. run widoco
3. run this script
"""
import pathlib

__this_dir__ = pathlib.Path(__file__).parent

import shutil


def copy_version_to_docs():
    version_path = __this_dir__ / 'docs/versions' / '1.0.0'
    target_path = __this_dir__ / 'docs_test'

    assert version_path.exists()
    assert version_path.is_dir()

    target_path.mkdir(exist_ok=True, parents=True)

    shutil.copytree(version_path, target_path, dirs_exist_ok=True)
    index_en = target_path / 'index-en.html'
    index_en.rename(target_path / 'index.html')


if __name__ == "__main__":
    copy_version_to_docs()