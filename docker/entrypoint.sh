#!/bin/bash

<<<<<<< HEAD
set -e
=======
set -euo pipefail

if [ "${1:0:1}" = "-" ]; then
    set -- ccapi "$@"
fi
>>>>>>> template/master

exec "$@"