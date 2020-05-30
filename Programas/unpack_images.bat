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