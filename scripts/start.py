from modules.utils import project

def start(raw_type):
  """Starts the script."""
  print('#----- Launching module -----#')
  type = project.ModuleType[raw_type.upper()]
  print('Module type :', type.name)
  print('------------------------------')
  try:
    match type:
      case project.ModuleType.LED_STRIP:
        from modules.led_strip import main
      case _:
        print('Unknown type', type.name)
  except Exception as err:
    print('Uncaught error while running module :', err)
  print('#----- Shutting down module -----#')
