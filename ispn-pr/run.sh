#!/bin/bash

# make sure our master is up to date
git pull origin master
# git checkout the branch
git branch merge master

( python ../handle_pull_request.py $1 $2 merge \
  && mvn clean install "${@:3}") || /bin/bash
