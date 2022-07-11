#!/bin/bash

set -eo pipefail

DATA_URL=${DATA_URL:-https://drive.google.com/drive/folders/1x3cfNL0McMeGHhkQ0yLB51dxaQXthT3J?usp=sharing}

wget \
	-R \
	--no-host-directories --cut-dirs=1 \
	--no-parent \
	--user=arqus \
	--no-verbose \
	--recursive \
	--directory-prefix=data \
	"$DATA_URL"
