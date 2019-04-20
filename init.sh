#!/usr/bin/env bash

if [[ -d /opt/init ]]
then
  (cd /opt/init; for i in *;do if [[ -x "$i" ]]; then ./$i;fi;done;)
fi

prog=$1
shift
exec $prog "$@"