import re
import time
from modules.utils import ghc, color, project
try:
  import RPi.GPIO as GPIO
  is_gpio = True
except Exception:
  is_gpio = False
  print('Running module without GPIO')

module = ghc.Module(project.ModuleType.LED_STRIP, project.Paths.API_URL.value, project.Paths.WEBSOCKET_URL.value)
current_color = color.Color(0, 0, 0)
current_loop = []

if is_gpio:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(24, GPIO.OUT)
  GPIO.setup(27, GPIO.OUT)
  GPIO.setup(10, GPIO.OUT)
  pwm_r = GPIO.PWM(24, 100)
  pwm_g = GPIO.PWM(27, 100)
  pwm_b = GPIO.PWM(10, 100)
  pwm_r.start(0)
  pwm_g.start(0)
  pwm_b.start(0)

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
  while current_loop and module.connected:
    for part in current_loop:
      if not current_loop or not module.connected:
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
            if not current_loop or not module.connected:
              break
            now = time.time() * 1000
            mix = abs(((next - now) / part['data'][3]) - 1)
            set_color(start_color.mix(end_color, mix))

def set_color(color):
  current_color.set_color(color)
  # print(color.to_array())
  if is_gpio:
    pwm_r.ChangeDutyCycle(color.r * (100 / 255))
    pwm_g.ChangeDutyCycle(color.g * (100 / 255))
    pwm_b.ChangeDutyCycle(color.b * (100 / 255))

module.connect()
module.wait()

if is_gpio:
  pwm_r.stop()
  pwm_g.stop()
  pwm_b.stop()
  GPIO.cleanup()
