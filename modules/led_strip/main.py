import re
import time
from guirlande_hub_client_package import ghc
from modules.utils import color, project

module = ghc.Module(project.ModuleType.LED_STRIP.value)
current_color = color.Color(0, 0, 0)
loop_run = False

def set_color(color):
  current_color.set_color(color)
  # TODO PWM write here

@module.listening('color')
def color_listener(data):
  global loop_run
  loop_run = False
  set_color(color.Color(data['red'], data['green'], data['blue']))

@module.listening('loop')
def loop_listener(data):
  global loop_run
  loop_run = False
  print('Stopped loop')
  if 'loop' in data:
    loop = load_loop(data['loop'])
    loop_run = True
    print('Started loop')
    run_loop(loop)

def load_loop(loop_data):
  loop = []
  for part in loop_data.split('|'):
    if re.match('c\(\d{1,3},\d{1,3},\d{1,3}\)', part):
      loop.append({ 'type': 'c', 'data': list(map(int, re.findall('\d+', part))) })
    elif re.match('w\(\d+\)', part):
      loop.append({ 'type': 'w', 'data': list(map(int, re.findall('\d+', part))) })
    elif re.match('t\(\d{1,3},\d{1,3},\d{1,3},\d+\)', part):
      loop.append({ 'type': 't', 'data': list(map(int, re.findall('\d+', part))) })
    else:
      print('Invalid part :', part)
  return loop

def run_loop(loop):
  while loop_run:
    for part in loop:
      if not loop_run:
        return
      match part['type']:
        case 'c':
          set_color(color.Color(part['data'][0], part['data'][1], part['data'][2]))
        case 'w':
          time.sleep(part['data'][0] / 1000)
        case 't':
          now = time.time() * 1000
          next = now + part['data'][3]
          start_color = current_color.copy()
          end_color = color.Color(part['data'][0], part['data'][1], part['data'][2])
          while now < next:
            if not loop_run:
              return
            now = time.time() * 1000
            mix = abs(((next - now) / part['data'][3]) - 1)
            set_color(start_color.mix(end_color, mix))

try:
  module.connect(project.Paths.WEBSOCKET_URL.value)
  module.register()
except KeyboardInterrupt:
  module.disconnect()
  print('Disconnected')
