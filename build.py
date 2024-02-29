import os
import re
from subprocess import run
from glob import glob
from sys import argv

def build(dir: str):
    """ディレクトリをビルド"""

    command = [
        'pandoc', '-sN',
        '--filter', 'pandoc-crossref',
        '--lua-filter', 'fenced_div_html.lua',
        '-f', 'markdown', '-t', 'html',
        '--toc', '--mathjax',
        '--template', 'template.html'
    ]
    command += sorted(glob(os.path.join(dir, '*.md')))
    command += ['-o', os.path.join(dir, dir + '.html')]
    run(command)

    command = [
        'pandoc',
        '-sN',
        '--filter', 'pandoc-crossref',
        '--lua-filter', 'fenced_div_latex.lua',
        '-f', 'markdown-auto_identifiers', '-t', 'latex',
        '--template', 'template.tex'
    ]

    metadata = os.path.join(dir, dir + '.yml')
    run([
        'pandoc',
        '--lua-filter', 'extract_yaml.lua',
        '-t', 'markdown',
        '--standalone',
        glob(os.path.join(dir, '*.md'))[0], '-o', metadata
    ])
    with open(metadata) as file:
        metadata = file.read()
    top_level_division = re.search(r'top-level-division:\s+.+\s', metadata).group()
    if top_level_division != '':
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