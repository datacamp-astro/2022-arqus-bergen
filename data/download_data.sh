#!/bin/bash

set -eo pipefail

DATA_URL=${DATA_URL:-https://userswww.pd.infn.it/~mdoro/arqus/data}

wget \
	-R "index.html*,robots*"\
	--no-host-directories --cut-dirs=1 \
	--no-parent \
	--no-verbose \
	--recursive \
	--directory-prefix=. \
	"$DATA_URL"

mv arqus/data/* .
rm -rf arqus/data
