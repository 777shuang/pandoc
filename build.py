import os
import re
from glob import glob
from sys import argv
import pypandoc
import yaml

def build(dir: str):
    """ディレクトリをビルド"""

    markdown = sorted(glob(os.path.join(dir, '*.md')))

    basedir = os.path.dirname(__file__)

    extra_args = ['--template', os.path.join(basedir, 'template.tex'), '--pdf-engine=latexmk']

    meta = pypandoc.convert_text(markdown[0], 'markdown', 'markdown', filters=['deletebody.lua'])
    meta_yaml = yaml.safe_load(re.search(r'---((.|\s)+)---', meta))
    if 'top-level-division' in meta_yaml:
        extra_args += ['--top-level-division', meta_yaml['top-level-division']]

    os.chdir(dir)
    pypandoc.convert_file(
        sorted(glob(os.path.join(dir, '*.md'))),
        'latex',
        format='markdown-auto_identifiers',
        outputfile=dir + 'tex',
        filters=[os.path.join(basedir, '.filters', 'filters.lua'), 'pandoc-crossref', 'mermaid-filter'],
        extra_args=extra_args
    )
    os.chdir(basedir)