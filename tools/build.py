# Regenere toutes les pages du site dans les deux langues (gabarit commun
# tools/layout.py), puis sitemap.xml et robots.txt.
# Usage : python tools/build.py
import os
import runpy

import layout

HERE = os.path.dirname(os.path.abspath(__file__))

for script in ('gen_home.py', 'gen_pages.py', 'gen_roadmap.py', 'gen_static.py'):
    runpy.run_path(os.path.join(HERE, script), run_name='__main__')

layout.write_seo_files()
