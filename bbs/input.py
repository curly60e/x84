from curses.ascii import isprint
from session import getsession, logger
from output import echo

def getch(timeout=None):
  event, data = getsession().read_event(events=['input'], timeout=timeout)
  return data

def getpos(timeout=None):
  """Return current terminal position as (y,x). (Blocking)"""
  logger.debug ("query ('pos', %f)", float('inf') if timeout is None else timeout)
  getsession().send_event('pos', timeout,) # ask for cursor position
  event, data = getsession().read_event(events=['pos'], timeout=timeout)
  return (None, None) \
      if (None, None) == (event, data) \
      else data

def readline(width, value = '', hidden = '', paddchar = ' ', events = [
    'input'], timeout = None, interactive = False, silent = False):
    (value, event, data) = readlineevent(width, value, hidden, paddchar, events, timeout, interactive, silent)
    return value

def readlineevent(width, value = '', hidden = '', paddchar = ' ', events = [
    'input'], timeout = None, interactive = False, silent = False):
  term = getsession().terminal

  if not hidden and value:
    echo (value)
  elif value:
    echo (hidden *len(value))

  while 1:
    event, char = getsession().read_event(events, timeout)

    # pass-through non-input data
    if event != 'input':
      data = char
      return (value, event, data)

    data = None
    if char == term.KEY_EXIT:
      return (None, 'input', data)

    elif char == term.KEY_ENTER:
      return (value, 'input', '\n')

    elif char == term.KEY_BACKSPACE:
      if len(value) > 0:
        value = value [:-1]
        echo ('\b' + paddchar + '\b')

    elif isinstance(char, int):
      pass # unhandled keycode ...

    elif len(value) < width and isprint(ord(char)):
      value += char
      if hidden:
        echo (hidden)
      else:
        echo (char)
    elif not silent:
      echo ('\a')
    if interactive:
      return (value, 'input', None)

