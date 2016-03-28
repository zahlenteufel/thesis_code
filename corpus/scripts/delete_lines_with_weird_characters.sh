#!/usr/bin/env bash

sed -e "s/[¡\!¿\?\.,:;—]/\n/g" < $1 |
	sed -e "/[^A-Za-záéíóúÁÉÍÓÚñÑüÜ0-9 ]/d" |
	sed -e "s/^\s*//" |                    # delete trailing spaces
	sed -e "s/\s*$//" |                    # delete leading spaces
	sed -e "/^[0-9]+$/d" |                 # delete only number line
	sed -E "s/\s+/ /g" |                   # collapse multiple spaces
	sed -e "/^$/d" > $2                    # delete empty lines
