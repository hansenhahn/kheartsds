@echo off

echo Calling dumper.py to unpack containers

REM Unpack containter
pypy dumper.py -m ".p2" -s "../ROM Original/xpa-khe/data"  -d "../Arquivos Originais"