import os
from subprocess import run
from glob import glob
from sys import argv

def build(dir: str):
    """ディレクトリをビルド"""

    tex = dir + '.tex' # LaTeXのファイル名

    # pandocの呼び出し(.md -> .tex)
    command = ['pandoc', '-sN', '-f', 'markdown', '-t', 'latex', '--template', 'template.tex']
    command += sorted(glob(os.path.join(dir, '*.md')))
    command += ['-o', os.path.join(dir, tex)]
    run(command)
    os.chdir(dir)
    run(['lualatex', '-shell-escape', tex])
    os.chdir('..')

if __name__=="__main__":
    build(argv[1])