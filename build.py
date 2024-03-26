import os
import re
from subprocess import run
from glob import glob
from sys import argv
from requests import get

def build(dir: str):
    """ディレクトリをビルド"""

    markdown = sorted(glob(os.path.join(dir, '*.md')))

    basedir = os.path.dirname(__file__)

    command = [
        'pandoc',
        '-sN',
        '--filter', 'pandoc-crossref',
        '--lua-filter', os.path.join(basedir, '.filters', 'filters.lua'),
        '-f', 'markdown-auto_identifiers', '-t', 'latex',
        '--template', 'template.tex'
    ]

    file = open(markdown[0])
    top_level_division = re.search(r'---(.|\s)+---', file.read()).group()
    file.close()
    top_level_division = re.search(r'\stop-level-division:\s+.+\s', top_level_division)
    if top_level_division is not None:
        top_level_division = top_level_division.group().strip()
        top_level_division = top_level_division.lstrip('top-level-division:')
        top_level_division = top_level_division.strip()
        command += ['--top-level-division=' + top_level_division]

    command += sorted(glob(os.path.join(dir, '*.md')))
    tex = dir + '.tex'
    command += ['-o', os.path.join(dir, tex)]
    run(command)
    os.chdir(dir)
    run(['latexmk', '-r', os.path.join(basedir, '.latexmkrc'), tex])

if __name__=="__main__" and os.path.isdir(argv[1]):
    plantuml = 'plantuml.jar'
    if not os.path.isfile(plantuml):
        print(plantuml + ' is not found.')
        print('Downloading...')
        content = get('http://sourceforge.net/projects/plantuml/files/plantuml.jar/download').content
        file = open(plantuml, 'wb')
        file.write(content)
        file.close()
        print('Done.')

    os.environ['LUA_PATH'] = os.path.join(os.getcwd(), '.filters', '?.lua') + ';;'
    os.environ['PLANTUML'] = os.path.join(os.getcwd(), plantuml)

    for dir in argv[1:]:
        build(dir)