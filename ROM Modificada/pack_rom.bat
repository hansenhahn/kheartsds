@echo off

del xpa-khe.nds
cd xpa-khe
..\ndstool -c "..\xpa-khe.nds" -9 arm9.bin -7 arm7.bin -y9 y9.bin -y7 y7.bin -d data -y overlay -t banner.bin -h header.bin
cd ..
