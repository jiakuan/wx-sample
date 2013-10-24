#!/bin/bash
# Copyright (C) 2013 WiseTime Pty Ltd, Inc. All Rights Reserved.

export LANG=en_US.UTF-8

SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script path: $SCRIPTPATH"

cd $SCRIPTPATH/
rm -rf $SCRIPTPATH/build
rm -rf $SCRIPTPATH/dist
rm -rf $SCRIPTPATH/*.spec
rm -rf $SCRIPTPATH/setup.py

#pyinstaller test_event_only.py --onefile --windowed
#pyinstaller test_wx_and_event.py --onefile --windowed
#pyinstaller test_wx_only.py --onefile --windowed

#/System/Library/Frameworks/Python.framework/Versions/Current/Extras/bin/py2applet --make-setup test_wx_only.py
/System/Library/Frameworks/Python.framework/Versions/Current/Extras/bin/py2applet --make-setup test_wx_and_event.py

python setup.py py2app
