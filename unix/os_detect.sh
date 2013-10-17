#!/bin/bash

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

export OS_IS_CYGWIN=0
export OS_IS_MAC=0
export OS_IS_UBUNTU=0
export OS_IS_GENTOO=0

case `uname` in
  "Darwin")
    export OS_IS_MAC=1
    ;;
  "Linux")
    if [ "`uname -a | grep '\<Ubuntu\>' | wc -l`" == "1" ]; then
      export OS_IS_UBUNTU=1
    fi

    if [ "`uname -a | grep -i '\<gentoo\>' | wc -l`" == "1" ]; then
      export OS_IS_GENTOO=1
    fi
    ;;
  *)
    if [ "`uname -o`" == "Cygwin" ]; then
      export OS_IS_CYGWIN=1
    fi
    ;;
esac

