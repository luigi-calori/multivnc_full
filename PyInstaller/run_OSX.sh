#!/bin/bash

SCRIPT_PATH="${BASH_SOURCE[0]}";
if([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
pushd . > /dev/null
cd `dirname ${SCRIPT_PATH}` > /dev/null
SCRIPT_PATH=`pwd`;
popd  > /dev/null

cd ${SCRIPT_PATH}
export VERSIONER_PYTHON_PREFER_32_BIT=yes
unzip pyinstaller-1.5.1.zip
arch -i386 python ${SCRIPT_PATH}/pyinstaller-1.5.1/Configure.py 
