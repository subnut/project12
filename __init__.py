from .main import main
from sys import exit

try:
    main()
except Exception in (EOFError, KeyboardInterrupt):
    exit(0)
