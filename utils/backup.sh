#!/usr/bin/env bash

filename="$(date).c"
dir=backups

cat generated.c > "$dir/$filename"
ls -l "$dir/$filename"
