'''indent a file: save old data in .bak file. This function was needed in development'''
import shutil
from misc import *

shift_width = 4

if len(args) < 3:
    err('indent [file name] [shift width e.g. 2 or 4]# prefix file with tab')

in_fn = args[1]

if not os.path.exists(in_fn):
    err('could not find input file: ' + in_fn)

try:
    shift_width = int(args[2])
except Exception:
    err('failed to parse shiftwidth parameter')

shutil.copyfile(in_fn, in_fn + '.bak')
print('+w', in_fn + '.bak')

in_f = open(in_fn, 'rb')
lines = in_f.readlines()
in_f.close()

lines = [((' ' * shift_width) + line.decode('utf-8').rstrip()) for line in lines]

open(in_fn, 'wb').write(('\n'.join(lines)).encode())
