import os
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
        '--top-level-division=chapter',
        '--template', 'template.tex'
    ]
    command += sorted(glob(os.path.join(dir, '*.md')))
    tex = dir + '.tex'
    command += ['-o', os.path.join(dir, tex)]
    run(command)
    os.chdir(dir)
    run(['latexmk', '-r', os.path.join('..', '.latexmkrc'), tex])
    os.chdir('..')

if __name__=="__main__" and os.path.isdir(argv[1]):
    build(argv[1])