import os
from subprocess import run
from glob import glob
from sys import argv
from shutil import copy, move
import codecs
import yaml

def pandoc(dir: str, settings):
    file = open(settings['type'])
    markdown = yaml.safe_load(file)
    file.close()
    markdown['title'] = settings['title']
    if 'subtitle' in settings:
        markdown['subtitle'] = settings['subtitle']
    if 'author' in settings:
        markdown['author'] = settings['author']
    if 'toc' in settings:
        markdown['toc'] = settings['toc']
    if 'toc-depth' in settings:
        markdown['toc-depth'] = settings['toc-depth']
    if 'usepackage' in settings:
        markdown['usepackage'] = settings['usepackage']
    if 'header-includes' in settings:
        markdown['header-includes'] = settings['header-includes']

    os.chdir(dir)
    files = settings['files']
    for i in range(len(files)):
        copy(files[i], os.path.join('output', str(i) + '.md'))
    os.chdir('output')

    file = open('0.md', 'r')
    md0 = file.read()
    file.close()
    file = open('0.md', 'w')
    file.write('---\n')
    file.write(yaml.dump(markdown, allow_unicode=True))
    file.write('\n---\n')
    file.write(md0)
    file.close()

def latexmk():
    run(['latexmk', '-r', os.path.join('..', '.latexmkrc'), os.path.join('output', 'output.tex')])

def build(dir: str):
    """ディレクトリをビルド"""

    file = open(os.path.join(dir, 'settings.yml'))
    settings = yaml.safe_load(file)
    file.close()
    os.makedirs(os.path.join(dir, 'output'), exist_ok=True)
    command = ['pandoc', '-sN', '--filter', 'pandoc-crossref', '--lua-filter', 'fenced_div.lua', '-f', 'markdown', '-t', 'latex', '--template']

    root = os.getcwd()

    if settings['type'] == 'site':
        file = open('template.yml')
        mkdocs = yaml.safe_load(file)
        file.close()
        mkdocs['site_name'] = settings['title']
        mkdocs['nav'] = settings['files']
        mkdocs['docs_dir'] = dir
        if 'author' in settings:
            mkdocs['site_author'] = ', '.join(settings['author'])
        if 'toc-title' in settings:
            mkdocs['plugins'][0]['with-pdf']['toc_title'] = settings['toc-title']
        if 'toc-depth' in settings:
            mkdocs['plugins'][0]['with-pdf']['toc_level'] = settings['toc-depth']
        with codecs.open('mkdocs.yml', 'w', 'utf-8') as file:
            yaml.dump(mkdocs, file, encoding='utf-8', allow_unicode=True)

        run(['mkdocs', 'build'])

    elif settings['type'] == 'book':
        pandoc(dir, settings)
        
        command += os.path.join(root, 'template.tex')
        command += {'--top-level-division=chapter'}
        command += sorted(glob('*.md'))
        command += ['-o', 'output.tex']
        run(command)

        os.chdir('..')
        latexmk()
        os.chdir('..')

    elif settings['type'] == 'article':
        pandoc(dir, settings)
        
        command += os.path.join(root, 'template.tex')
        command += sorted(glob('*.md'))
        command += ['-o', 'output.tex']
        run(command)

        os.chdir('..')
        latexmk()
        os.chdir('..')
        
    elif settings['type'] == 'report':
        pandoc(dir, settings)
        
        command += os.path.join(root, 'template.tex')
        command += sorted(glob('*.md'))
        command += ['-o', 'output.tex']
        run(command)

        os.chdir('..')
        latexmk()
        os.chdir('..')

if __name__=="__main__":
    if len(argv) == 1:
        dirs = os.listdir()
        dirs.remove('.git')
        dirs.remove('.github')
        dirs.remove('.venv')
        dirs.remove('__pycache__')
        for dir in dirs:
            if os.path.isdir(dir):
                build(dir)
    elif os.path.isdir(argv[1]):
        build(argv[1])