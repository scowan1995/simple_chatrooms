import socket
import sys
import os
import threading
import queue
from server import server


def main():
    my_server = server("", 3002)


if __name__ == "__main__":
    main()
