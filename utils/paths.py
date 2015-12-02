import os
import sys


def experiments_data_path(file):
    PATH = "EXPERIMENTS_DATA_PATH"
    if PATH not in os.environ:
        print "Environment variable '%s' not set." % PATH
        sys.exit(1)
    return os.environ[PATH].rstrip("/") + "/" + file
