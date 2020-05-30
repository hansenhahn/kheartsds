@echo off

echo "Calling tl_img.py to unpack background"
pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\ttl" -d "..\Arquivos Originais\ttl"
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 0 -nscr 0 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 0 -nscr 1 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 0 -nscr 2 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 1 -nscr 3 -ncgr 1
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 2 -nscr 4 -ncgr 2
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 2 -nscr 5 -ncgr 2
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 2 -nscr 6 -ncgr 2
pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\PK2D_001" -d "..\Imagens Originais\ttl\ttl\PK2D_001" -nclr 3 -nscr 7 -ncgr 3

pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\newgame" -d "..\Arquivos Originais\data\UI\newgame"
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\newgame\res\PK2D_000" -d "..\Imagens Originais\data\UI\newgame\res\PK2D_000" -nclr 0 -nscr 0 -ncgr 0

pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\btl" -d "..\Arquivos Originais\data\UI\btl"
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\btl\map\PK2D_011" -d "..\Imagens Originais\data\UI\btl\map\PK2D_011" -nclr 0 -nscr 0 -ncgr 0

pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\srslt" -d "..\Arquivos Originais\data\UI\srslt"
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 25 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 24 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 24 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 23 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 22 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 21 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 20 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 19 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 18 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 17 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 16 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 15 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 14 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 13 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 12 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 11 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 10 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 1 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 0 -ncgr 0
pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 7 -ncgr 5


