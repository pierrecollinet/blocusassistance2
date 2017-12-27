from .base import *

print('ok jusquici')
try:
    from .local import *
    live = False

except:
    live = True

if live:
    from .production import *

