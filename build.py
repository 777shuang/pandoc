import os
import re
from subprocess import run
from glob import glob
from sys import argv

def build(dir: str):
    """ディレクトリをビルド"""

    markdown = sorted(glob(os.path.join(dir, '*.md')))
    command = [
        'pandoc', '-sN',
        '--filter', 'pandoc-crossref',
        '--lua-filter', 'fenced_div.lua',
        '-f', 'markdown', '-t', 'html',
        '--toc', '--mathjax',
        '--template', 'template.html'
    ]
    command += markdown
    command += ['-o', os.path.join(dir, dir + '.html')]
    run(command)

    command = [
        'pandoc',
        '-sN',
        '--filter', 'pandoc-crossref',
        '--lua-filter', 'fenced_div.lua',
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
    run(['latexmk', '-r', os.path.join('..', '.latexmkrc'), tex])
    os.chdir('..')

if __name__=="__main__" and os.path.isdir(argv[1]):
    build(argv[1])