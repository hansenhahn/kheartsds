#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def rename( root ):
    f = os.listdir( root )
    for p in f:
        src = os.path.join( root, p )
        dst = src.replace( ".z", "" )
        os.rename( src,dst )

rename( "ev/EV_AL" )
rename( "ev/EV_AW" )
rename( "ev/EV_BB" )
rename( "ev/EV_DP" )
rename( "ev/EV_HE" )
rename( "ev/EV_NM" )
rename( "ev/EV_PP" )
rename( "ev/EV_S" )
rename( "ev/EV_TT" )