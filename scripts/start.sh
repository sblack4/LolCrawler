#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd ${DIR}
cd ..

nohup python MatchCrawler.py > logger.log 2>&1 &