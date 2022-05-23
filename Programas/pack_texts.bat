@echo off

echo Calling inserter.py to pack texts

pypy inserter.py -m "z" -s "../Textos Traduzidos/op" -d "../Arquivos Traduzidos/op"
copy "../Arquivos Traduzidos/op/" "../ROM Modificada/xpa-khe/data/op/" /B/Y

REM rem Pack das legendas
REM pypy inserter.py -m "gnrc" -s "../Textos Traduzidos/UI/thr" -s1 "../Arquivos Traduzidos/UI/thr" -d "../ROM Modificada/xpa-khe/data/UI/thr" -ext ".p2" -fnt

REM rem Pack dos scripts dos eventos, com os textos principais (EV)
REM pypy inserter.py -m "gnrc" -s "../Textos Traduzidos/ev" -s1 "../Arquivos Traduzidos/ev" -d "../ROM Modificada/xpa-khe/data/ev" -ext ".p2"

rem Pack dos scripts espalhados, com os textos secundários (mi/mi)
pypy inserter.py -m "cakp" -s "../Textos Traduzidos/mi/mi" -s1 "../Arquivos Traduzidos/mi/mi" -d "../ROM Modificada/xpa-khe/data/mi/mi" -fnt