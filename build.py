import os
from subprocess import run
from glob import glob
from sys import argv

def build(dir: str):
    """ディレクトリをビルド"""

    command = ['pandoc', '-sN', '--filter', 'pandoc-crossref', '--lua-filter', 'fenced_div.lua', '-f', 'markdown', '-t', 'latex', '--template', 'template.tex']
    command += sorted(glob(os.path.join(dir, '*.md')))
    tex = dir + '.tex'
    command += ['-o', os.path.join(dir, tex)]
    run(command)
    os.chdir(dir)
    run(['latexmk', '-r', os.path.join('..', '.latexmkrc'), tex])
    os.chdir('..')

if __name__=="__main__" and os.path.isdir(argv[1]):
    build(argv[1])