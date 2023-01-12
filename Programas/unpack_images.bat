@echo off

echo "Calling tl_img.py to unpack background"
rem pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\ttl" -d "..\Arquivos Originais\ttl"
rem pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI"  -d "..\Arquivos Originais\UI"
REM pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cal\cl_hrt_en.pobj.z" -d "..\Imagens Originais\cal\cl_hrt_en.pobj.z" -img "ani" -img-args 0 0 0

pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\load\lod_b_000.pbg.z" -d "..\Imagens Originais\UI\load\lod_b_000.pbg.z" -img "bg" -img-args 0 0 0
exit /b

rem Sprites do menu . Não mexer
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_000.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_000.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_001.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_001.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_002.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_002.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_003.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_003.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_004.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_004.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_005.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_005.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_006.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_006.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_007.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_007.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_008.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_008.z" -img "ani" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\cm\__cmo_en.p2\cmo_en_009.z" -d "..\Imagens Originais\UI\cm\__cmo_en.p2\cmo_en_009.z" -img "ani" -img-args 0 0 0



REM pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\newgame" -d "..\Arquivos Originais\data\UI\newgame"
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\newgame\res\PK2D_000" -d "..\Imagens Originais\data\UI\newgame\res\PK2D_000" -nclr 0 -nscr 0 -ncgr 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\newgame\__res.p2\res_000.z" -d "..\Imagens Originais\UI\newgame\__res.p2\res_000.z" -img "bg" -img-args 0 0 0

rem Unpack dos tutoriais. Funcional, não mexer!
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_000.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_000.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_001.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_001.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_002.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_002.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_003.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_003.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_004.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_004.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_005.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_005.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_006.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_006.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_007.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_007.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_008.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_008.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_009.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_009.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_010.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_010.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_011.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_011.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_012.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_012.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_013.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_013.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_014.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_014.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_015.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_015.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_016.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_016.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_017.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_017.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_018.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_018.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_019.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_019.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_020.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_020.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_021.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_021.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_022.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_022.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_023.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_023.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_024.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_024.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_025.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_025.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_026.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_026.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_027.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_027.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_028.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_028.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_029.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_029.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_030.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_030.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_031.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_031.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_032.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_032.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_033.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_033.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_034.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_034.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_035.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_035.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_036.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_036.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_037.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_037.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_038.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_038.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_039.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_039.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_040.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_040.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_041.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_041.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_042.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_042.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_043.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_043.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_044.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_044.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_045.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_045.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_046.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_046.z" -img "bg" -img-args 0 0 0
pypy dumper.py -m ".pk2d.z" -s1 "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_047.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2\ttr_en_047.z" -img "bg" -img-args 0 0 0

exit /b

rem Tutoriais de batalha
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_000.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_001.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_002.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_003.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_004.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_005.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_006.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_007.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_008.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_009.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_010.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_011.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_012.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_013.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_014.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_015.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_016.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_017.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_018.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_019.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_020.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_021.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_022.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_023.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_024.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_025.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\__ttr_en.p2\ttr_en_026.z" -d "..\Imagens Originais\UI\btlttr\__ttr_en.p2" -nclr 0 -nscr 0 -ncgr 0
rem pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0027" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0028" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0029" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0030" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0031" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0032" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0033" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0034" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0035" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0036" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0037" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0038" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0039" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0040" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0041" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0042" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0043" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0044" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0045" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0046" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\btlttr\ttr_en\0047" -d "..\Imagens Originais\UI\btlttr\ttr_en" -nclr 0 -nscr 0 -ncgr 0

REM rem Novo Jogo
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\newgame\res\0000" -d "..\Imagens Originais\UI\newgame\res" -nclr 0 -nscr 0 -ncgr 0

REM rem Créditos
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 1 -nscr 1 -ncgr 1
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 2 -nscr 2 -ncgr 2
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 3 -nscr 3 -ncgr 3
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 4 -nscr 4 -ncgr 4
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 5 -nscr 5 -ncgr 5
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 6 -nscr 6 -ncgr 6
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0000" -d "..\Imagens Originais\UI\sf\sf" -nclr 7 -nscr 7 -ncgr 7
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 1 -nscr 1 -ncgr 1
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 2 -nscr 2 -ncgr 2
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 3 -nscr 3 -ncgr 3
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 4 -nscr 4 -ncgr 4
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 5 -nscr 5 -ncgr 5
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 6 -nscr 6 -ncgr 6
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0001" -d "..\Imagens Originais\UI\sf\sf" -nclr 7 -nscr 7 -ncgr 7
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 1 -nscr 1 -ncgr 1
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 2 -nscr 2 -ncgr 2
REM rem pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 3 -nscr 3 -ncgr 3
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 4 -nscr 4 -ncgr 4
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 5 -nscr 5 -ncgr 5
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 6 -nscr 6 -ncgr 6
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 7 -nscr 7 -ncgr 7
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 8 -nscr 8 -ncgr 8
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 9 -nscr 9 -ncgr 9
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 10 -nscr 10 -ncgr 10
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 11 -nscr 11 -ncgr 11
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 12 -nscr 12 -ncgr 12
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 13 -nscr 13 -ncgr 13
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0002" -d "..\Imagens Originais\UI\sf\sf" -nclr 14 -nscr 14 -ncgr 14
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 1 -nscr 1 -ncgr 1
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 2 -nscr 2 -ncgr 2
REM rem pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 3 -nscr 3 -ncgr 3
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 4 -nscr 4 -ncgr 4
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 5 -nscr 5 -ncgr 5
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 6 -nscr 6 -ncgr 6
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 7 -nscr 7 -ncgr 7
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 8 -nscr 8 -ncgr 8
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 9 -nscr 9 -ncgr 9
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 10 -nscr 10 -ncgr 10
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 11 -nscr 11 -ncgr 11
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 12 -nscr 12 -ncgr 12
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 13 -nscr 13 -ncgr 13
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0003" -d "..\Imagens Originais\UI\sf\sf" -nclr 14 -nscr 14 -ncgr 14
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0004" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0005" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0005" -d "..\Imagens Originais\UI\sf\sf" -nclr 1 -nscr 1 -ncgr 1
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0006" -d "..\Imagens Originais\UI\sf\sf" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\UI\sf\sf\0006" -d "..\Imagens Originais\UI\sf\sf" -nclr 1 -nscr 1 -ncgr 1

REM rem Splash
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 0 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 0 -nscr 1 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 0 -nscr 2 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 1 -nscr 3 -ncgr 1
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 2 -nscr 4 -ncgr 2
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 2 -nscr 5 -ncgr 2
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 2 -nscr 6 -ncgr 2
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\ttl\ttl\0001" -d "..\Imagens Originais\ttl\ttl" -nclr 3 -nscr 7 -ncgr 3


REM pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\newgame" -d "..\Arquivos Originais\data\UI\newgame"
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\newgame\res\PK2D_000" -d "..\Imagens Originais\data\UI\newgame\res\PK2D_000" -nclr 0 -nscr 0 -ncgr 0

REM pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\btl" -d "..\Arquivos Originais\data\UI\btl"
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\btl\map\PK2D_011" -d "..\Imagens Originais\data\UI\btl\map\PK2D_011" -nclr 0 -nscr 0 -ncgr 0

REM pypy tl_unpacker.py -s "..\ROM Original\xpa-khe\data\UI\srslt" -d "..\Arquivos Originais\data\UI\srslt"
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 25 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 24 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 24 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 23 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 22 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 21 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 20 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 19 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 18 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 17 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 16 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 15 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 14 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 13 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 12 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 11 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 10 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 1 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 0 -ncgr 0
REM pypy tl_img.py -m e0 -s "..\Arquivos Originais\data\UI\srslt\res\PK2D_000" -d "..\Imagens Originais\data\UI\srslt\res\PK2D_000" -nclr 1 -nscr 7 -ncgr 5


