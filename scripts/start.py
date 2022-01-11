from modules.utils import project

start_count = 0

def start(raw_type, watch=False):
  """Starts the script."""
  global start_count
  print('#----- Launching module -----#\n')
  
  type = project.ModuleType[raw_type.upper()]
  start_count += 1

  print('<---- Module informations --->')
  print('  Type :', type.name)
  if watch:
    print('  Start count :', start_count)
  print('<---------------------------->')

  try:
    __run(type)
  except KeyboardInterrupt:
    print('Manual stopping') # TODO Don't work on module.wait() and background tasks
  except Exception as err:
    print('Uncaught error while running module :', err)
    if watch:
      start(type.name, True) # FIXME Calling this function will freezes current call and may causes RAM overflow because the call stack gets bigger at every call
      return

  print('\n#----- Shutting down module -----#')
  exit(0)

def __run(type):
  match type:
    case project.ModuleType.TEST:
      from modules.test import main
    case project.ModuleType.LED_STRIP:
      from modules.led_strip import main
    case project.ModuleType.MAGASIN:
      from modules.magasin import main
    case _:
      print('Unknown type', type.name)
