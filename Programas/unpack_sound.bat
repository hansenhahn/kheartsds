@echo off

echo "Calling tl_sound.py to unpack sound"
pypy tl_sound.py -m e -s "..\ROM Original\xpa-khe\data\mv" -d "..\Som Original"
rem pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI"  -d "..\Arquivos Originais\UI"