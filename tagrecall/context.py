import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../vcore/')))
import vcore

logging.basicConfig(level=logging.INFO)