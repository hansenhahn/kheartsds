@echo off

echo "KHDays by DiegoHH"

rem Copia os arquivos originais, onde serão inseridos os novos textos
rem Temporário, até corrigir o inserter desse tipo de arquivo, que está impedindo a criação do arquivo do 0
rem xcopy /s/Y "Arquivos\Unpacked ev" "Arquivos PT-BR\Unpacked ev\"
rem xcopy /s/Y "Arquivos\Unpacked st" "Arquivos PT-BR\Unpacked st\"
rem xcopy /S/Y "Arquivos\Unpacked mi" "Arquivos PT-BR\Unpacked mi\"

rem Cria os overlays
REM cd Asm
REM call gen_overlay.bat
REM cd ..

rem Executa os packers de overlay, imagem e texto
cd Programas
REM call pack_overlays.bat
REM call pack_images.bat
call pack_texts.bat
cd ..

rem Executa o gerador de splash
rem copy "Splash\arm9.bin" "ROM Modificada\PLAYTON" /B/Y

rem Monta a ROM nova e gera um patch
cd ROM Modificada
call pack_rom.bat
rem call do_patch.bat
cd ..