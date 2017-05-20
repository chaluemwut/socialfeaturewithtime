# -*- coding: utf-8 -*-

import logging, sys, json, os

log = logging.getLogger('harvest')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = logging.FileHandler("harvest.log")
fh.setFormatter(format)
log.addHandler(fh)