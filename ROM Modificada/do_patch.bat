@echo off

rem Foi necess�rio aumentar a janela do xdelta para que fosse poss�vel comparar as duas roms e gerar um patch com 
rem tamanho aceit�vel.
xdelta.exe -B 268435456 -e -9 -S djw -vfs "..\ROM Original\xpa-khe.nds" "xpa-khe.nds" "khdays.xdelta"