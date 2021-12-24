"""Module package script.

Running this script will package all modules into an archive per module in the `archives` directory (auto created if not exists).
"""
import zipfile
import glob
from pathlib import Path
from modules.utils import project
from os import path

def start():
  """Starts the script."""
  print('#----- Starting modules packaging -----#\n')

  Path('./archives').mkdir(exist_ok=True)
  for f in glob.glob('./archives/*.zip'):
    Path(f).unlink(missing_ok=True)

  for type in project.ModuleType:
    type_name = type.name.lower()
    utils_path = path.join('modules', 'utils')
    module_path = path.join('modules', type_name)
    archive_path = path.join('archives', type_name + '.zip')

    print('Creating', type.name, 'archive')
    with zipfile.ZipFile(archive_path, 'x', zipfile.ZIP_STORED) as archive:
      __write_utils_module(archive, utils_path)
      __write_current_module(archive, type_name, module_path)
      __write_main_file(archive, type_name, 'main.py')
      __test_archive(archive)
      print('Created', type.name, 'archive in', archive.filename)
  print('#----- Modules packaging finished ! -----#')

def __write_utils_module(archive, utils_path):
  """Writes utils module in archive."""
  for f in glob.glob(utils_path + '/**/*', recursive=True):
    if not f.startswith(path.join(utils_path, '__pycache__')):
      final_path = 'utils/' + path.basename(f)
      archive.write(f, final_path)
      print('  Writing', final_path)

def __write_current_module(archive, type_name, module_path):
  """Writes current module in archive."""
  for f in glob.glob(module_path + '/**/*', recursive=True):
    if not f.startswith(path.join(module_path, '.venv')) and not f.startswith(path.join(module_path, '__pycache__')):
      final_path = type_name + '/' + path.basename(f)
      archive.write(f, final_path)
      print('  Writing', final_path)

def __write_main_file(archive, type_name, main_path):
  """Writes main file in archive."""
  archive.writestr(main_path, 'from ' + type_name + ' import main\n')
  print('  Writing', main_path)

def __test_archive(archive):
  """Tests archive."""
  print('  Testing archive')
  test_result = archive.testzip()
  if test_result:
    print('    Test archive failed :', test_result)
  else:
    print('    Test archive success')
