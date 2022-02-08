#!/usr/bin/env python3
import argparse,os,glob
import gzip
import numpy as np
import sys
def select_and_expand(path,pathOut,z,ang,gzipped=True):
    h2 = 716.
    h1 = float(z)
    ang_deg = float(ang)
    n_scanpos = 982
    viewza = np.zeros(n_scanpos)
    viewza2 = np.zeros(n_scanpos)
    ifovrad = 0.00159 
    for i in range(n_scanpos):
        ii=i+1
        ci = (-1.0 * n_scanpos / 2.) + i
        viewza[i] = ci * ifovrad
        viewza2[i] = np.arctan( (h2*np.tan(viewza[i]))/h1 )
    diff2 = np.abs(np.abs(np.rad2deg(viewza2))-ang_deg)
    min_diff2 = diff2.min()
    idx2 = np.where(diff2==min_diff2)
    iiout = np.max(idx2)
    print('outputting idx {} for ang {} and height {}'.format(iiout,ang_deg,h1) ) 
    fout = open(pathOut,'w')
    if(gzipped):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            ii=int(-1)
            for i,line in enumerate(f):
                ii+=1
                if(ii==iiout):
                    #print(np.rad2deg(viewza))
                    fout.write(line)
                elif(ii==981):
                    ii=int(-1)
                
    else:
        with open(path) as f:           
            ii=int(-1)
            for i,line in enumerate(f):
                ii+=1
                if(ii==iiout):
                    fout.write(line)
                elif(ii==981):
                    ii=int(-1)
    fout.close()
    return
if __name__ == '__main__' :
    parser = argparse.ArgumentParser( description = 'read gz text file,select +/-30 deg scan angle, and output to another file using --in directory and --out directory')
    parser.add_argument('--in', help = 'path to gz or text', required = True, dest = 'path')
    parser.add_argument('--out', help = 'path to ncdiag', required = True, dest = 'outpath')
    parser.add_argument('--height', help = 'sat alt', required = True, dest = 'height')
    parser.add_argument('--ang', help = 'desired sat ang', required = True, dest = 'ang')
    arg = parser.parse_args()
    #a= glob.glob('/discover/nobackup/wrmccart/mistic/orbit/sat.1330*.gz')
    #a.sort()
    #print(a)
    a = glob.glob(os.path.join(arg.path,'sat.1330*.gz'))
    a.sort()
    for i,aa in enumerate(a):
        b = os.path.join(arg.outpath,os.path.split(aa)[1].replace('.gz',''))
        print('+/- 30 deg scan angle from {} to {}'.format(aa,b)) 
        select_and_expand(aa,b,arg.height,arg.ang)        
