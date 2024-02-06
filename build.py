import os
from subprocess import run
from glob import glob
from sys import argv

def build(dir: str):
    md = dir + '.md' # Markdown(結合済み)のファイル名
    tex = dir + '.tex' # LaTeXのファイル名

    # 複数のmdファイルを一つにまとめる
    wp = open(md, 'w', encoding='utf_8')
    for file in sorted(glob(os.path.join(dir, '*.md'))):
        fp = open(file, 'r', encoding='utf_8')
        wp.write(fp.read())
        wp.write('\n')
        fp.close()
    wp.close()
            
    # pandocの呼び出し(.md -> .tex)
    run([
        'pandoc',
        '-sN',
        '-f', 'markdown',
        '-t', 'latex',
        '--template', 'template.tex',
        md, '-o', os.path.join(dir, tex)
    ])
    os.chdir(dir)
    run(['uplatex', '--shell-escape', tex]) # LaTeX(1回目)
    run(['uplatex', '--shell-escape', tex]) # LaTeX(2回目)
    run(['dvipdfmx', dir]) # dvi -> pdf
    os.chdir('..')

if __name__=="__main__":
    build(argv[1])