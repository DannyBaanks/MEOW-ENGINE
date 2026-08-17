#!/usr/bin/env python3
"""Genera un gatito ASCII aleatorio y lo guarda en cat.txt"""
import random
import sys

CATS = [
    r"""      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  '-' 
    '---''(_/--'  `-\_)""",
    r"""      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  '-' 
    '---''(_/--'  \_-')""",
    r"""      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  '-' 
    '---''(_/--'  \_\')""",
    r"""      |
   / \__
  (    @\___
  /         O
 /   (_____/
/_____/   U""",
    r"""      |
    \   /
     |  |
    /   \
   |     |
   |  .  |
    \___/
    ___|___"""
]

def main():
    cat = random.SystemRandom().choice(CATS)
    with open("cat.txt", "w", encoding="utf-8") as f:
        f.write(cat)
    print(cat)

if __name__ == "__main__":
    main()
