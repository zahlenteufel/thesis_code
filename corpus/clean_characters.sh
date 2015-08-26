#!/usr/bin/env bash

sed -e "s/ – //g" $1 |
	sed -e "s/ ρ //g" |
	sed -e "s/γη/\n/g" |
	sed -e "s/ \/ /\n/g" |
	python clean_characters.py > $2