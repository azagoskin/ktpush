#!/usr/bin/python3
import sys

from tw_kaiten.app import app

if __name__ == "__main__":
    app(sys.stdin.read())
