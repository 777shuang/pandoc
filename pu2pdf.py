from sys import argv
import os

if len(argv) == 3:
    cat = 'cat'
    if os.name == 'nt':
        cat = 'type'
    tmp_dir = os.path.join(os.path.dirname(argv[1]), 'svg-inkscape')
    os.makedirs(tmp_dir, exist_ok=True)
    svg = os.path.join(tmp_dir, os.path.basename(argv[1]) + '.svg')
    os.system(cat + ' ' + argv[1] + ' | java -jar ' + os.path.join('..', 'plantuml.jar') + ' -charset UTF-8 -tsvg -pipe > ' + svg)
    os.system('inkscape -z --file=' + svg + ' --export-pdf=' + argv[2])