# Regenere toutes les pages du site (gabarit commun tools/layout.py).
# Usage : python tools/build.py
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))

for script in ('gen_home.py', 'gen_pages.py', 'gen_roadmap.py', 'gen_static.py'):
    runpy.run_path(os.path.join(HERE, script), run_name='__main__')
