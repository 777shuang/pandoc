from sys import argv
import os

if len(argv) == 3:
    cat = 'cat'
    if os.name == 'nt':
        cat = 'type'
    tmp_dir = 'svg-inkscape'
    os.makedirs(tmp_dir, exist_ok=True)
    svg = os.path.join(tmp_dir, argv[1] + '.svg')
    os.system(cat + ' ' + argv[1] + ' | plantuml -charset UTF-8 -tsvg -pipe > ' + svg)
    os.system('inkscape -z --file=' + svg + ' --export-pdf=' + argv[2])