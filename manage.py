import os
import datetime as dt
from glob import glob

def rtn_modified_time(path: str) -> dt.datetime:
    """ファイルの変更時刻を返す"""
    info = os.stat(path)
    modified_time = dt.datetime.fromtimestamp(info.st_mtime)
    return modified_time

dirs = {} # key: ディレクトリ名, value: {key: ファイル名, value: 変更時刻}

for dir in os.listdir(os.getcwd()):
    if dir != '.git' and dir != '.github' and os.path.isdir(dir):
        print('found: ' + dir)
        files = {} # key: ファイル名, value: 変更時刻
        for file in glob(os.path.join(dir, "*.md")):
            if file != dir + '.md': # 出力ファイルは除外
                print('  found: ' + file)
                files[file] = rtn_modified_time(file)
        dirs[dir] = files

while True:
    for dir, files in dirs.items():
        do = False
        for file, modified_time in files.items():
            if modified_time != rtn_modified_time(file):
                do = True
                files[file] = rtn_modified_time(file) # 更新時刻の更新
                print('modified: ' + file)
        
        if do:
            from subprocess import run

            md = dir + '.md'
            tex = dir + '.tex'

            # 複数のmdファイルを一つにまとめる        
            wp = open(md, 'w')
            for file in files:
                fp = open(file, 'r')
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
                md, '-o', tex
            ])
            run(['uplatex', tex]) # LaTeX(1回目)
            run(['uplatex', tex]) # LaTeX(2回目)
            run(['dvipdfmx', dir]) # dvi -> pdf

    from time import sleep
    sleep(1)