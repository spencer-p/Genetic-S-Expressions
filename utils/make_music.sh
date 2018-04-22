#!/usr/bin/env bash

INTERMEDIATE=generated.c
COMPILED=music

echo -n "Generating expression: "
exp=$(python main.py)
echo $exp

echo "Writing the file:"
echo '#include <stdio.h>
int _g(int t) {' > $INTERMEDIATE
echo "return $exp;" >> $INTERMEDIATE
echo '}
int main() { for (int t=0;;t++) putchar(_g(t)); }' >> $INTERMEDIATE

cat $INTERMEDIATE

echo "Compiling..."
cc $INTERMEDIATE -o $COMPILED

pacat --rate 8000 --format u8 <(./$COMPILED)
