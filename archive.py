import zipfile
import glob
from pathlib import Path
from modules.utils import project
from os import path

Path('./archives').mkdir(exist_ok=True)
Path('/archives/*.zip').unlink(missing_ok=True)

for type in project.ModuleType:
  type_name = type.name.lower()
  print('Creating', type.name, 'archive')
  utils_path = path.join('modules', 'utils')
  module_path = path.join('modules', type_name)
  archive_path = path.join('archives', type_name + '.zip')
  with zipfile.ZipFile(archive_path, 'w') as archive:
    for f in glob.glob(utils_path + '/**/*', recursive=True):
      if not f.startswith(path.join(utils_path, '__pycache__')):
        final_path = 'utils/' + path.basename(f)
        archive.write(f, final_path)
        print('Writing', final_path)
    for f in glob.glob(module_path + '/**/*', recursive=True):
      if not f.startswith(path.join(module_path, '.venv')) and not f.startswith(path.join(module_path, '__pycache__')):
        final_path = type_name + '/' + path.basename(f)
        archive.write(f, final_path)
        print('Writing', final_path)
print('Done !')
# TODO Test extracted archive (py led_strip/main.py) to check if it works
