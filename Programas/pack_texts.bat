@echo off

echo Calling inserter.py to pack texts

rem Missão dia 8
xcopy "..\Arquivos Originais\mi\mi\__0001.p2" "..\Arquivos Traduzidos\mi\mi\__0001.p2/" /I /E /Y
pypy inserter.py -m "cakp" -s "../Textos Traduzidos/mi/mi/__0001.p2" -d "../Arquivos Traduzidos/mi/mi/__0001.p2"
REM pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/mi/mi" -d "../ROM Modificada/xpa-khe/data/mi/mi" -fnt
REM exit /b
rem Missão dia 
REM xcopy "..\Arquivos Originais\mi\mi\__0006.p2" "..\Arquivos Traduzidos\mi\mi\__0006.p2/" /I /E /Y
REM pypy inserter.py -m "cakp" -s "../Textos Traduzidos/mi/mi/__0006.p2" -d "../Arquivos Traduzidos/mi/mi/__0006.p2"
rem Pack dos textos sem avatar do salão. Funcional, não mexer
xcopy "..\Arquivos Originais\mi\mi\__10000.p2" "..\Arquivos Traduzidos\mi\mi\__10000.p2/" /I /E /Y
pypy inserter.py -m "cakp" -s "../Textos Traduzidos/mi/mi/__10000.p2" -d "../Arquivos Traduzidos/mi/mi/__10000.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/mi/mi" -d "../ROM Modificada/xpa-khe/data/mi/mi" -fnt



rem Pack do banco de dados. Funcional, não mexer
xcopy "..\Arquivos Originais\db\__db_en.p2" "..\Arquivos Traduzidos\db\__db_en.p2" /I /E /Y
pypy inserter.py -m ".db" -s "../Textos Traduzidos/db/__db_en.p2" -d "../Arquivos Traduzidos/db/__db_en.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/db" -d "../ROM Modificada/xpa-khe/data/db" -ext ".p2"

rem Pack do nome dos locais no mapa. Funcional, não mexer
xcopy "..\Arquivos Originais\UI\btl\en\__map.p2" "..\Arquivos Traduzidos\UI\btl\en\__map.p2" /I /E /Y
pypy inserter.py -m ".map" -s "../Textos Traduzidos/UI/btl/en/__map.p2" -d "../Arquivos Traduzidos/UI/btl/en/__map.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/UI/btl/en" -d "../ROM Modificada/xpa-khe/data/UI/btl/en" -ext ".p2"

rem Pack da UI. Funcional, não mexer
pypy inserter.py -m ".s.z" -s "../Textos Traduzidos/UI" -s1 "../Arquivos Traduzidos/UI" -d "../ROM Modificada/xpa-khe/data/UI"
rem Pack dos títulos. Funcional, não mexer
pypy inserter.py -m ".s.z" -s "../Textos Traduzidos/UI/cal/ttl_en.z.txt" -s1 "../Arquivos Traduzidos/UI/cal" -d "../ROM Modificada/xpa-khe/data/UI/cal"
rem Pack do diário e bestiário. Funcional, não mexer
pypy inserter.py -m ".rpt.z" -s "../Textos Traduzidos/UI/cm/str/rpt_en.z.txt" -s1 "../Arquivos Traduzidos/UI/cm/str" -d "../ROM Modificada/xpa-khe/data/UI/cm/str/"
pypy inserter.py -m ".rpt.z" -s "../Textos Traduzidos/UI/cm/str/enm_en.z.txt" -s1 "../Arquivos Traduzidos/UI/cm/str" -d "../ROM Modificada/xpa-khe/data/UI/cm/str/"
rem Pack dos tutoriais. Funcional, não mexer
pypy inserter.py -m ".dat.z" -s "../Textos Traduzidos/UI/btlttr/ttr_en.dat.z.txt" -s1 "../Arquivos Traduzidos/UI/btlttr" -d "../ROM Modificada/xpa-khe/data/UI/btlttr"

rem Pack dos scripts das legendas dos vídeos. Funcional, não mexer
xcopy "..\Arquivos Originais\UI\thr\__m.p2" "..\Arquivos Traduzidos\UI\thr\__m.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/UI/thr/__m.p2" -d1 "../Arquivos Traduzidos/UI/thr/__m.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/UI/thr" -d "../ROM Modificada/xpa-khe/data/UI/thr" -fnt -ext ".p2"

rem Pack dos scripts da legenda. Funcional, não mexer
xcopy "..\Arquivos Originais\op\scr.z" "..\Arquivos Traduzidos\op\scr.z" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/op/scr.z.txt" -d1 "../Arquivos Traduzidos/op/scr.z"
pypy inserter.py -m ".z" -s "../Arquivos Traduzidos/op" -d "../ROM Modificada/xpa-khe/data/op"
rem Pack dos EVs. Funcional, não mexer
xcopy "..\Arquivos Originais\ev\__EV_AL.p2" "..\Arquivos Traduzidos\ev\__EV_AL.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_AL.p2" -d1 "../Arquivos Traduzidos/ev/__EV_AL.p2"
xcopy "..\Arquivos Originais\ev\__EV_BB.p2" "..\Arquivos Traduzidos\ev\__EV_BB.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_BB.p2" -d1 "../Arquivos Traduzidos/ev/__EV_BB.p2"
xcopy "..\Arquivos Originais\ev\__EV_DP.p2" "..\Arquivos Traduzidos\ev\__EV_DP.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_DP.p2" -d1 "../Arquivos Traduzidos/ev/__EV_DP.p2"
xcopy "..\Arquivos Originais\ev\__EV_HE.p2" "..\Arquivos Traduzidos\ev\__EV_HE.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_HE.p2" -d1 "../Arquivos Traduzidos/ev/__EV_HE.p2"
xcopy "..\Arquivos Originais\ev\__EV_NM.p2" "..\Arquivos Traduzidos\ev\__EV_NM.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_NM.p2" -d1 "../Arquivos Traduzidos/ev/__EV_NM.p2"
xcopy "..\Arquivos Originais\ev\__EV_PP.p2" "..\Arquivos Traduzidos\ev\__EV_PP.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_PP.p2" -d1 "../Arquivos Traduzidos/ev/__EV_PP.p2"
xcopy "..\Arquivos Originais\ev\__EV_S.p2" "..\Arquivos Traduzidos\ev\__EV_S.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_S.p2"  -d1 "../Arquivos Traduzidos/ev/__EV_S.p2"
xcopy "..\Arquivos Originais\ev\__EV_TT.p2" "..\Arquivos Traduzidos\ev\__EV_TT.p2" /I /E /Y
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_TT.p2" -d1 "../Arquivos Traduzidos/ev/__EV_TT.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/ev" -d "../ROM Modificada/xpa-khe/data/ev" -ext ".p2"
