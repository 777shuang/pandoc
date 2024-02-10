import os
from datetime import datetime
from glob import glob
from time import sleep
from shutil import copy
from build import build

def get_modified_time(path: str) -> datetime:
    """ファイルの変更時刻を返す"""
    info = os.stat(path)
    modified_time = datetime.fromtimestamp(info.st_mtime)
    return modified_time

dirs = {} # key: ディレクトリ名, value: {key: ファイル名, value: 変更時刻}

for dir in os.listdir(os.getcwd()):
    if dir != '.git' and dir != '.github' and dir != '__pycache__' and os.path.isdir(dir): # Markdownが格納されているディレクトリのみ実行
        print('found: ' + dir)
        files = {} # key: ファイル名, value: 変更時刻
        for file in glob(os.path.join(dir, '*.md')): # Markdownファイルについてループ
            if file != dir + '.md': # 出力ファイルは除外
                files[file] = get_modified_time(file)
                print('  found:' + file)
        dirs[dir] = files

while True:
    for dir, files in dirs.items():
        do = False # コンパイル実行フラグ
        for file, modified_time in files.items():
            if modified_time != get_modified_time(file): # 更新時刻が一致しない(変更された)
                do = True
                files[file] = get_modified_time(file) # 更新時刻の更新
                print('modified: ' + file)
        
        if do: # コンパイル実行フラグが立っていたら実行
            build(dir)

            toc1 = dir + '.toc' # キャッシュ
            toc2 = os.path.join(dir, dir + '.toc') # 元のTOC
            if os.path.isfile(toc2):
                if not os.path.isfile(toc1): # キャッシュがない場合
                    build(dir)
                    copy(toc2, toc1)
                else:
                    file1 = open(toc1, 'r', encoding='utf_8')
                    file2 = open(toc2, 'r', encoding='utf_8')
                    if file1.readlines() != file2.readlines(): # キャッシュと元のTOCが一致しなかったら
                        build(dir) # 再実行
                        copy(toc2, toc1) # キャッシュを再生成
    sleep(1)