import os
from subprocess import run
from glob import glob
from sys import argv

def pandoc(dir: str):
    """Pandocの実行(.md -> .tex)"""

    command = ['pandoc', '-sN', '-f', 'markdown', '-t', 'latex', '--template', 'template.tex']
    command += sorted(glob(os.path.join(dir, '*.md')))
    command += ['-o', os.path.join(dir, dir + '.tex')]
    run(command)

def lualatex(dir: str):
    """LuaLaTeXの実行"""

    os.chdir(dir)
    run(['lualatex', '-shell-escape', dir + '.tex'])
    os.chdir('..')

def build(dir: str):
    """ディレクトリをビルド"""

    pandoc(dir)
    lualatex(dir)

if __name__=="__main__" and os.path.isdir(argv[1]):
    build(argv[1])
    lualatex(argv[1])