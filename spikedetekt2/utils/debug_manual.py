import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle 
from matplotlib.backends.backend_pdf import PdfPages
from spikedetekt2.processing import extract_waveform

from IPython import embed # For manual debugging


def plot_diagnostics_twothresholds(threshold = None, probe = None,components = None,chunk = None,chunk_detect= None,chunk_threshold=None, chunk_fil=None, chunk_raw=None,**prm):

    multdetection_times = prm['observation_time_samples']
    s_start = chunk.s_start  # Absolute start of the chunk
   

  
    #debug_fd = GlobalVariables['debug_fd']
    
    samplingrate= prm['sample_rate']
 #   samplingrate= 20000 
  
#  multdetection_times_ms = Parameters['OBSERVATION_TIMES']
  #  multdetection_times =  np.array(multdetection_times_ms, dtype=np.int32)
  #  multdetection_times = multdetection_times*samplingrate/1000
  #  multdetection_times = multdetection_times.astype(int)

    

    chunk_size_less= prm['chunk_size']-200
#-Parameters['CHUNK_OVERLAP']
#    print 'Parameters: \n', Parameters
   # probefilename = Parameters['PROBE_FILE']
#    print 'chunk_size_less = ', chunk_size_less
#    window_width = 120
#    samples_backward = 60
    window_width = 140
    samples_backward = 70

 # path='/home/skadir/alignment/'
    #path = Parameters['OUTPUT_DIR']
    for interestpoint in multdetection_times:
   # for interestpoint_ms in multdetection_times_ms:
    #    interestpoint = int(interestpoint_ms*samplingrate/1000)
  
 #      pp = PdfPages('/home/skadir/alignment/multipagegraphs.pdf')
        if (interestpoint - chunk_size_less) <= s_start < (interestpoint):
            #print interestpoint_ms, ':\n'
            #debug_fd.write(str(interestpoint_ms)+':\n')
            print interestpoint, ':\n'
            #debug_fd.write(str(interestpoint)+':\n')
             # sampmin = interestpoint - s_start - 3
            sampmin = np.amax([0,interestpoint - s_start - samples_backward])
            sampmax = sampmin + window_width 
            print 'sampmin, sampmaz ',sampmin, sampmax

            
            connected_comp_enum = np.zeros_like(chunk_fil)
            j = 0
            debugnextbits = []
            for k,indlist in enumerate(components):
                indtemparray = np.array(indlist.items)
                #print k,':',indlist, '\n'
               # print '\n'
               # j = j+1
               # connected_comp_enum[indtemparray[:,0],indtemparray[:,1]] = j
                
               # debug_fd.write(str(k)+': '+'\n')
               # debug_fd.write(str(indlist)+'\n')
               # debug_fd.write('\n') 
               # debug_fd.flush()   
                #embed()
                if (set(indtemparray[:,0]).intersection(np.arange(sampmin,sampmax+1)) != set()):
                    
                    print k,':',indlist, '\n'
                    print '\n'
                    j = j+1
                    connected_comp_enum[indtemparray[:,0],indtemparray[:,1]] = j
                    
                    #debug_fd.write(str(k)+': '+'\n')
                    #debug_fd.write(str(indlist)+'\n')
                    #debug_fd.write('\n') 
                    #debug_fd.flush()       # makes sure everything is written to the debug file as program proceeds
                    
                    
                    #N_CH = prms['nchannels']
                    
                    chunk_extract = chunk_detect 
                    wv = extract_waveform(indlist,
                                 chunk_extract=chunk_extract,
                                 chunk_fil=chunk_fil,
                                 chunk_raw=chunk_raw,
                                 threshold_strong=threshold.strong,
                                 threshold_weak=threshold.weak,
                                 probe=probe,
                                 **prm)
                    
                    
                    
                    s_peak = wv.s_min 
                    sf_peak= wv.s_min 
                    #+ wv.s_frac_part
                    
                    
                    
                    #embed()                                
                    debugnextbits.append((s_peak, sf_peak))
                    print 'debugnextbits =', debugnextbits
                    #debug_fd.write('debugnextbits ='+ str(debugnextbits)+'\n')
                    #debug_fd.flush()  
                    #embed()


            plt.figure()
            #filtchunk_normalised = np.maximum((filteredchunk - ThresholdWeak) / (ThresholdStrong - ThresholdWeak),0)
            #filtchunk_normalised_power = np.power(filtchunk_normalised,Parameters['WEIGHT_POWER'])
            
            print 'plotting figure now'
            
            #plt.suptitle('%s \n with %s \n Time %s samples'%(Parameters['RAW_DATA_FILES'],Parameters['PROBE_FILE'],interestpoint), fontsize=10, fontweight='bold')
           # plt.suptitle('Time %s ms'%(interestpoint_ms), fontsize=14, fontweight='bold')
            #plt.subplots_adjust(hspace = 0.5)
            plt.subplots_adjust(hspace = 0.25,left= 0.12, bottom = 0.10, right = 0.90, top = 0.90, wspace = 0.2)
            
            dataxis = plt.subplot(3,1,1)
            dataxis.set_title('DatChunks',fontsize=10)
            imdat = dataxis.imshow(np.transpose(chunk_raw[sampmin:sampmax,:]),interpolation="nearest",aspect="auto")
            dataxis.set_xlabel('Samples')
            dataxis.set_ylabel('Channels')

            
           
            filaxis = plt.subplot(3,1,2)
            filaxis.set_title('FilteredChunks',fontsize=10)
            imfil = filaxis.imshow(np.transpose(chunk_fil[sampmin:sampmax,:]),interpolation="nearest",aspect="auto")
            filaxis.set_xlabel('Samples')
            filaxis.set_ylabel('Channels')
            
            
           
            #filaxis = plt.subplot(4,2,2)
            compaxis = plt.subplot(3,1,3)
            #filaxis.set_title('BinChunks',fontsize=10)
            imcomp = compaxis.imshow(np.transpose(chunk_threshold.weak[sampmin:sampmax,:].astype(int)+chunk_threshold.strong[sampmin:sampmax,:].astype(int)),interpolation="nearest",aspect="auto")
            compaxis.set_xlabel('Samples')
            compaxis.set_ylabel('Channels')
            for spiketimedebug in debugnextbits:
                compaxis.axvline(spiketimedebug[1]-sampmin,color = 'w') #plot a vertical line for s_fpeak
                print spiketimedebug[1]-sampmin
            
            
            
            
            plt.show()
            plt.savefig('SD2floodfillchunk_%s_samples.pdf'%(interestpoint))
            #tosave = [debugnextbits,binarychunkweak,binarychunkstrong,binarychunk,filteredchunk,datchunk,connected_comp_enum,sampmin,sampmax]
            #pickle.dump(tosave,open('savegraphdata_%s.p'%(interestpoint),'wb'))