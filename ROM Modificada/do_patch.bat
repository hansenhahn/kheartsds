@echo off

rem Foi necessário aumentar a janela do xdelta para que fosse possível comparar as duas roms e gerar um patch com 
rem tamanho aceitável.
xdelta.exe -B 268435456 -e -9 -S djw -vfs "..\ROM Original\xpa-khe.nds" "xpa-khe.nds" "khdays.xdelta"