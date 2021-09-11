#!/bin/bash
# TODO use arguments to make use of xargs's -P n option
find . -name "*.json" -print0 | xargs -0 -L 1 tools/json_formatter.cgi
