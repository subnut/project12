from .main import main
from sys import exit

try:
    main()
except (EOFError, KeyboardInterrupt):
    print()
    exit(0)
