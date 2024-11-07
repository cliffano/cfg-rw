#!/bin/sh

export CFGRW_HANDLERS="stream,file"
export CFGRW_DATEFMT="%Y-%m-%d %H:%M:%S"
export CFGRW_FILENAME="stage/test-integration/test-yaml-conf.log"
export CFGRW_FILEMODE="w"
export CFGRW_FORMAT="%(levelname)s %(message)s"
export CFGRW_LEVEL="info"

python3 _cfgrw.py