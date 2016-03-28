#!/usr/bin/env bash
sed -E "/(www|http|@|©|®)/d" $1 |         # delete lines with links, emails, copyroghts
	sed -e "s/^\s*//" |                   # delete trailing spaces
	sed -e "s/\s*$//" |                   # delete leading spaces
	sed -e "/^[0-9]+$/d" |                # delete only number line
	sed -E "s/\s+/ /g" |                  # collapse multiple spaces
	sed -e "/^$/d" |                      # delete empty lines
	sed -e "s/“/«/g" |                    # unify characters for easier processing later
	sed -e "s/”/»/g" |
	sed -E "s/\"([^\"]*)\"/«\1»/g" > $2
