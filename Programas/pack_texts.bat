@echo off

echo Calling inserter.py to pack texts

rem Pack dos textos sem avatar do salão. Funcional, não mexer
xcopy "../Arquivos Originais/mi/mi/__10000.p2" "../Arquivos Traduzidos/mi/mi/__10000.p2/" /S /I /Q /Y /F
pypy inserter.py -m "cakp" -s "../Textos Traduzidos/mi/mi/__10000.p2" -d "../Arquivos Traduzidos/mi/mi/__10000.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/mi/mi" -d "../ROM Modificada/xpa-khe/data/mi/mi" -fnt

rem Pack do nome dos locais no mapa. Funcional, não mexer
xcopy "../Arquivos Originais/UI/btl/en/__map.p2" "../Arquivos Traduzidos/UI/btl/en/__map.p2" /I /D
pypy inserter.py -m ".map" -s "../Textos Traduzidos/UI/btl/en/__map.p2" -d "../Arquivos Traduzidos/UI/btl/en/__map.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/UI/btl/en" -d "../ROM Modificada/xpa-khe/data/UI/btl/en" -ext ".p2"

rem Pack da UI. Funcional, não mexer
pypy inserter.py -m ".s.z" -s "../Textos Traduzidos/UI" -s1 "../Arquivos Traduzidos/UI" -d "../ROM Modificada/xpa-khe/data/UI"

rem Pack dos scripts das legendas dos vídeos. Funcional, não mexer
xcopy "../Arquivos Originais/UI/thr/__m.p2" "../Arquivos Traduzidos/UI/thr/__m.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/UI/thr/__m.p2" -d1 "../Arquivos Traduzidos/UI/thr/__m.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/UI/thr" -d "../ROM Modificada/xpa-khe/data/UI/thr" -fnt -ext ".p2"

rem Pack dos scripts da legenda. Funcional, não mexer
xcopy "../Arquivos Originais/op/scr.z" "../Arquivos Traduzidos/op/scr.z" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/op/scr.z.txt" -d1 "../Arquivos Traduzidos/op/scr.z"
pypy inserter.py -m ".z" -s "../Arquivos Traduzidos/op" -d "../ROM Modificada/xpa-khe/data/op"

rem Pack dos EVs. Funcional, não mexer
xcopy "../Arquivos Originais/ev/__EV_AL.p2" "../Arquivos Traduzidos/ev/__EV_AL.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_AL.p2" -d1 "../Arquivos Traduzidos/ev/__EV_AL.p2"
xcopy "../Arquivos Originais/ev/__EV_BB.p2" "../Arquivos Traduzidos/ev/__EV_BB.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_BB.p2" -d1 "../Arquivos Traduzidos/ev/__EV_BB.p2"
xcopy "../Arquivos Originais/ev/__EV_DP.p2" "../Arquivos Traduzidos/ev/__EV_DP.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_DP.p2" -d1 "../Arquivos Traduzidos/ev/__EV_DP.p2"
xcopy "../Arquivos Originais/ev/__EV_HE.p2" "../Arquivos Traduzidos/ev/__EV_HE.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_HE.p2" -d1 "../Arquivos Traduzidos/ev/__EV_HE.p2"
xcopy "../Arquivos Originais/ev/__EV_NM.p2" "../Arquivos Traduzidos/ev/__EV_NM.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_NM.p2" -d1 "../Arquivos Traduzidos/ev/__EV_NM.p2"
xcopy "../Arquivos Originais/ev/__EV_PP.p2" "../Arquivos Traduzidos/ev/__EV_PP.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_PP.p2" -d1 "../Arquivos Traduzidos/ev/__EV_PP.p2"
xcopy "../Arquivos Originais/ev/__EV_S.p2" "../Arquivos Traduzidos/ev/__EV_S.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_S.p2"  -d1 "../Arquivos Traduzidos/ev/__EV_S.p2"
xcopy "../Arquivos Originais/ev/__EV_TT.p2" "../Arquivos Traduzidos/ev/__EV_TT.p2" /I /D
pypy inserter.py -m ".noext" -s "../Textos Traduzidos/ev/__EV_TT.p2" -d1 "../Arquivos Traduzidos/ev/__EV_TT.p2"
pypy inserter.py -m ".p2" -s "../Arquivos Traduzidos/ev" -d "../ROM Modificada/xpa-khe/data/ev" -ext ".p2"























rem Pack das legendas
REM pypy inserter.py -m "z" -s "../Textos Traduzidos/UI/cm/str" -s1 "../Arquivos Traduzidos/UI/cm/str" -d "../ROM Modificada/xpa-khe/data/UI/cm/str" -ext ".z"

REM pypy inserter.py -m "z" -s "../Textos Traduzidos/op" -d "../Arquivos Traduzidos/op"
REM copy "../Arquivos Traduzidos/op/" "../ROM Modificada/xpa-khe/data/op/" /B/Y

REM rem Pack das legendas
rem pypy inserter.py -m ".noext" -s "../Textos Traduzidos/UI/thr/m" -s1 "../Arquivos Traduzidos/UI/thr/m" -d "../ROM Modificada/xpa-khe/data/UI/thr/m" -ext ".p2" -fnt
rem pypy inserter.py -m "gnrc" -s "../Textos Traduzidos/UI/thr/m" -s1 "../Arquivos Traduzidos/UI/thr/m" -d "../ROM Modificada/xpa-khe/data/UI/thr/m" -ext ".p2" -fnt

REM rem Pack dos scripts dos eventos, com os textos principais (EV)
REM pypy inserter.py -m "gnrc" -s "../Textos Traduzidos/ev" -s1 "../Arquivos Traduzidos/ev" -d "../ROM Modificada/xpa-khe/data/ev" -ext ".p2"

REM REM rem Pack dos scripts espalhados, com os textos secundários (mi/mi)
REM pypy inserter.py -m "cakp" -s "../Textos Traduzidos/mi/mi" -s1 "../Arquivos Traduzidos/mi/mi" -d "../ROM Modificada/xpa-khe/data/mi/mi" -fnt

REM REM rem Pack dos scripts da legenda
REM pypy inserter.py -m ".noext" -s "../Textos Traduzidos/op" -s1 "../Arquivos Traduzidos/op" -d "../ROM Modificada/xpa-khe/data/op"

REM REM rem Pack dos scripts da interface
REM pypy inserter.py -m ".s.z" -s "../Textos Traduzidos/UI" -s1 "../Arquivos Traduzidos/UI" -d "../ROM Modificada/xpa-khe/data/UI"

rem Unpack dos scripts da interface
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/chara.s.z" -d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/cmd.s.z" -d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/enemy.s.z" -d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/info.s.z"	-d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/item.s.z"	-d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/magic.s.z" -d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/btl/en/text.s.z"	-d "../Textos Originais/UI/btl/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/cfg_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/enm_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/panel_en.s.z"	-d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/root_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/rpt_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/sav_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/select_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/status_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/ttl_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/cm/str/world_id_en.s.z" -d "../Textos Originais/UI/cm/str"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/load/lrd_en.s.z"	-d "../Textos Originais/UI/load"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/load/str/en/lrd.s.z"	-d "../Textos Originais/UI/load/str/en"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/mlt/mlt_en.s.z" -d "../Textos Originais/UI/mlt"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/mnl/mnl_en.s.z" -d "../Textos Originais/UI/mnl"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/newgame/ngm_en.s.z" -d "../Textos Originais/UI/newgame"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/shop/shp_en.s.z"	-d "../Textos Originais/UI/shop"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/srslt/res_en.s.z" -d "../Textos Originais/UI/srslt"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/sys/sys_en.s.z" -d "../Textos Originais/UI/sys"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/thr/thr_en.s.z" -d "../Textos Originais/UI/thr"
REM pypy dumper.py -m ".s.z" -s1 "../Arquivos Originais/UI/tutorial/root_en.s.z" -d "../Textos Originais/UI/tutorial"