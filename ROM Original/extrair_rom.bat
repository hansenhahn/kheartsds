@echo off

md xpa-khe
cd xpa-khe
..\ndstool -x "..\xpa-khe.nds" -9 arm9.bin -7 arm7.bin -y9 y9.bin -y7 y7.bin -d data -y overlay -t banner.bin -h header.bin

