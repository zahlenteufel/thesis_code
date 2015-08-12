#!/usr/bin/env bash

if [ ! $# -eq 3 ]; then
	echo "Usage $0 folder regex output_file"
	echo "concatenates many files together"
	exit 1
fi

folder=$1
regex=$2
output_file=$3

find $folder -type f -print0 -name "$regex" | sort -z | xargs -0 cat -- > $output_file
