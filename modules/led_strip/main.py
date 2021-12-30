import re
import time
from modules.utils import ghc, color, project

module = ghc.Module(project.ModuleType.LED_STRIP.value, project.Paths.API_URL.value, project.Paths.WEBSOCKET_URL.value)
current_color = color.Color(0, 0, 0)
current_loop = []

@module.listening('color')
def color_listener(data):
  global current_loop
  current_loop = []
  c = color.Color(data['red'], data['green'], data['blue'])
  print(' > Event "color" received :', c.to_array())
  set_color(c)

@module.listening('loop')
def loop_listener(data):
  global current_loop
  current_loop = []
  if 'loop' in data:
    current_loop = load_loop(data['loop'])
    print(' > Event "loop" received :', current_loop)
    loop()

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

def loop():
  while current_loop:
    for part in current_loop:
      if not current_loop:
        break
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
            if not current_loop:
              break
            now = time.time() * 1000
            mix = abs(((next - now) / part['data'][3]) - 1)
            set_color(start_color.mix(end_color, mix))

def set_color(color):
  current_color.set_color(color)
  print(color.to_array())
  # TODO PWM write here

module.connect()
module.wait()
