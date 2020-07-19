#!/bin/sh

cd `dirname $0`

. ./venvsetting

create(){
    [ ! -z "${VIRTUAL_ENV}" ] && exit 1
    if [ ! -d "$AIM" ]; then python3 -m virtualenv -p $(command -v python3) --no-download $AIM; fi
}

update(){
    . $AIM/bin/activate
    pip install -U pip wheel setuptools $DEV $BACKEND $API $LIBS
    if [ -d "libs" ]; then
        venvlib=$(realpath .venv/lib/python3.*/site-packages)
        for py in libs/*.py
        do
            ln -rvsf $py ${venvlib}/
        done
    fi
    deactivate
}

del(){
    [ ! -z "${VIRTUAL_ENV}" ] && exit 1
    rm -r $AIM
}


COMMAND=${1:-'create'}
AIM=${2:-'.venv'}

case $COMMAND in
    'create')
        create
        update
    ;;
    'update')
        update
    ;;
    'recreate')
        del
        create
        update
    ;;
esac