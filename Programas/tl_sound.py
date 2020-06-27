#!/usr/bin/env python
# -*- coding: windows-1252 -*-

# author: diego.hahn
#
''' Baseado no Moflex Player, by Gericom'''

import traceback
import wave
import struct
import array
import sys
import glob
import os


__title__ = "KHDAYS Sound Extractor"
__version__ = "2.0"

SHORT_MAX = 32767
SHORT_MIN = -32768


STEP_SIZE_TABLE = [ 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34,
   37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143,
   157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494,
   544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552,
   1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026,
   4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442,
   11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623,
   27086, 29794, 32767 ]

SIZEOF_STEP_SIZE_TABLE = len( STEP_SIZE_TABLE )

INDEX_ADJUST_TABLE = [
   -1, -1, -1, -1,  # +0 - +3, decrease the step size
    2, 4, 6, 8,     # +4 - +7, increase the step size
   -1, -1, -1, -1,  # -0 - -3, decrease the step size
    2, 4, 6, 8 ]     # 
    
SIZEOF_INDEX_ADJUST_TABLE = len( INDEX_ADJUST_TABLE ) 

def Clamp(value, min, max):
    if (value < min): value = min;
    if (value > max): value = max;
    return value

def ADPCMDecoder( data , start ):
    # Utiliza o algoritmo IMA
    out = array.array("c")
    
    for sampd in data:
        sampd = ord( sampd )
        
        # Cada 4 bits representa 16 bits na saída decodificada
        for i in range(2):
            Index, Last = start

            val = (sampd >> (i*4)) & 0xf
            diff = STEP_SIZE_TABLE[Index] / 8 + \
                    STEP_SIZE_TABLE[Index] / 4 * ((val >> 0) & 1) + \
                    STEP_SIZE_TABLE[Index] / 2 * ((val >> 1) & 1) + \
                    STEP_SIZE_TABLE[Index] * ((val >> 2) & 1)  
                        
            samp = Last + diff * ( -1 if (( val >> 3 ) & 1) else 1 )
                
            Last = Clamp(samp, SHORT_MIN, SHORT_MAX);
            Index = Clamp(Index + INDEX_ADJUST_TABLE[val & 7], 0, 88)    
    
            start[0] = Index
            start[1] = Last
            out.extend( struct.pack( "<h" , Last ) )
 
    return out

KEYFRAME_NUMBER = 0 
KEYFRAME_OFFSET = 1
    
class ModsReader:  
    def __init__( self , fd ):
        assert fd.read(4) == "MODS" , "Not a MODS file"
        
        self.TagId = struct.unpack("<H" , fd.read(2))[0]
        self.TagIdSizeDword = struct.unpack("<H", fd.read(2))[0]
        self.FrameCount = struct.unpack("<L" , fd.read(4))[0]
        self.Width = struct.unpack("<L" , fd.read(4))[0]
        self.Height = struct.unpack("<L" , fd.read(4))[0]
        self.Fps = struct.unpack("<L" , fd.read(4))[0]
        self.AudioCodec = struct.unpack("<H" , fd.read(2))[0]
        self.NbChannel = struct.unpack("<H" , fd.read(2))[0]
        self.Frequency = struct.unpack("<L" , fd.read(4))[0]
        self.BiggestFrame = struct.unpack("<L" , fd.read(4))[0]
        self.AudioOffset = struct.unpack("<L" , fd.read(4))[0]
        self.KeyframeIndexOffset = struct.unpack("<L" , fd.read(4))[0]
        self.KeyframeCount = struct.unpack("<L" , fd.read(4))[0]
        
        self.__fd = fd  
        
        self.KeyframeTable = [[],[]]
        self.KeyframeReader()
        
    def KeyframeReader( self ):
        # Tabela de ponteiros        
        self.__fd.seek( self.KeyframeIndexOffset )
        for _ in range( self.KeyframeCount ):
            FrameNumber, DataOffset = struct.unpack( "<LL", self.__fd.read(8) )
            self.KeyframeTable[KEYFRAME_NUMBER].append( FrameNumber ) 
            self.KeyframeTable[KEYFRAME_OFFSET].append( DataOffset )

    def AudioReader( self, sname ):
        assert len( self.KeyframeTable[KEYFRAME_NUMBER] ) == self.KeyframeCount , "Error with Keyframe Table"
        
        if self.NbChannel == 0:
            return
    
        AudioData = [ array.array("c") , array.array("c") ] * self.NbChannel 
        ADPCMStart = [ None , None ]
    
        init = [ False , False ]
        
        BaseFrame = 0
        
        with open( self.__fd.name + ".txt" , "r" ) as ofs:
            AudioOffsets = map(lambda x: int(x.strip("\r\n")), ofs.readlines())

        for RelativeFrame in range( self.FrameCount ):
            CurFrame = BaseFrame + RelativeFrame
            print "\rFrame %d of %d" % ( CurFrame+1 , self.FrameCount ) ,
            try:
                if CurFrame in self.KeyframeTable[KEYFRAME_NUMBER]:
                    init = [ False , False ]
                    IsKeyFrame = True
                    idx = self.KeyframeTable[KEYFRAME_NUMBER].index(CurFrame)
                    self.__fd.seek( self.KeyframeTable[KEYFRAME_OFFSET][idx] )
                else:
                    IsKeyFrame = False            
                offset = self.__fd.tell()
                PacketInfo = struct.unpack( "<L" , self.__fd.read(4) )[0]
                PacketSize = PacketInfo >> 14
                NrAudioPackets = PacketInfo & 0x3fff 
          
                # Com essa informação, podemos saltar o vídeo
                if IsKeyFrame:
                    AudioOffset = PacketSize - self.NbChannel * ( NrAudioPackets * 128 + 4 ) # O +4 é relativo ao valor inicial do filtro, que só existe nos key frames
                else:
                    AudioOffset = PacketSize - self.NbChannel * ( NrAudioPackets * 128 )
                
                # Pra isso funcionar, eu preciso da informação do offset do áudio extraida pela ferramenta do gericom modificada
                if ( struct.unpack("<H", self.__fd.read(2))[0] & 0x8000 ):
                    self.__fd.seek(offset + AudioOffsets[CurFrame] + 8)
                else:
                    self.__fd.seek(offset + AudioOffsets[CurFrame] + 4)
                    
                for j in range( NrAudioPackets ):
                    for k in range( self.NbChannel ):
                        if init[k] == False:
                            # Inicialização do filtro
                            #Index = struct.unpack( "<h" , struct.pack( "<H" , struct.unpack("<H", self.__fd.read(2))[0] & 0x7f )) [0]
                            Index = struct.unpack( "<h" , self.__fd.read(2))[0]
                            Last = struct.unpack("<h", self.__fd.read(2))[0]  # Signed
                            ADPCMStart[k] = [Index, Last]
                            init[k] = True
                        ret = ADPCMDecoder( self.__fd.read(128) , ADPCMStart[k] ) 

                        AudioData[k].extend( ret )
         
                self.__fd.seek( offset + PacketSize + 4 )
            except:
                print CurFrame
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print "*** print_tb:"
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                print "*** print_exception:"
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                break
    
        print ""
        print "Len of each channel: %s and %s" % (len(AudioData[0]) , len(AudioData[1]))
            
        print "Generating wave"
        wavef = wave.open(sname,'w')
        wavef.setnchannels(self.NbChannel) # stereo
        wavef.setsampwidth(2) #16 bits
        wavef.setframerate(self.Frequency) # 32728 Hz
        # Interleave
        for k in range( 0, len(AudioData[0]) , 2 ):      
            wavef.writeframesraw( AudioData[0][k:k+2] + AudioData[1][k:k+2] )
 
        wavef.close()     
        
def scandirs(path):
    files = []
    for currentFile in glob.glob( os.path.join(path, '*') ):
        if os.path.isdir(currentFile):
            files += scandirs(currentFile)
        else:
            files.append(currentFile)
    return files            

def unpackSound( src, dst ):
    files = filter(lambda x: x.endswith('.mods'), scandirs(src))
        
    for _, fname in enumerate(files):
        print fname
        path = fname[len(src):]
        fdirs = dst + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)   
    
        sname = fdirs + os.path.basename(path) + '.wav'
    
        with open( fname, "rb" ) as fd:
            a = ModsReader( fd )
            a.AudioReader( sname )

if __name__ == "__main__":

    import argparse
    
    os.chdir( sys.path[0] )
    #os.system( 'cls' )

    print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', dest = "mode", type = str, required = True )
    parser.add_argument( '-s', dest = "src", type = str, nargs = "?", required = True )
    parser.add_argument( '-d', dest = "dst", type = str, nargs = "?", required = True )
    
    args = parser.parse_args()
    
    # dump bg
    if args.mode == "e":
        print "Unpacking sound"           
        unpackSound( args.src , args.dst )
    # insert bg
    # elif args.mode == "i0": 
        # print "Packing background"
        # packBackground( args.src , args.dst )
    # # dump ani
    # elif args.mode == "e1": 
        # print "Unpacking animation"
        # unpackSprite( args.src , args.dst )
    # # insert ani
    # elif args.mode == "i1": 
        # print "Packing animation"
        # print args.src1
        # packSprite( args.src , args.dst , args.src1 )
    else:
        sys.exit(1)

    # with open( "802.mods" , "rb" ) as fd:
        # a = ModsReader( fd )
        # a.AudioReader()

    pass

