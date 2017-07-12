"""
This script is designed to determine, based on user input, what functions to call 
from wedge_utils.py.

It requires a HERA data filename string such as:
    "path/to/zen.2457700.47314.xx.HH.uvcRR"

wedge_utils.py, and the calfile should be in the PYTHONPATH

Command line format example:
$ python2.7 getWedge.py -f path/to/file path/to/file -c=hsa7458_v001.py --pol=xx,xy,yx,yy 
-t -x=20,9 -s=3

Co-Author: Paul Chichura <pchich@sas.upenn.edu>
Co-Author: Amy Igarashi <igarashiamy@gmail.com>
Co-Author: Austin Fox Fortino <fortino@sas.upenn.edu>
Created: June 21, 2017
Last Updated: July 11, 2017
"""
import argparse, wedge_utils, os, pprint

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filenames', help='Input a list of filenames to be analyzed.', nargs='*', required=True)
parser.add_argument('-c', '--calfile', help='Input the calfile to be used for analysis.', required=True)
parser.add_argument('-p', '--pol', help='Input a comma-delimited list of polatizations to plot.', required=True)
parser.add_argument('-t', '--time_avg', help='Toggle time averaging.', action='store_true')
parser.add_argument('-x', '--ex_ants', help='Input a comma-delimited list of antennae to exclude from analysis.', type=str)
parser.add_argument('-s', '--step', help='Toggle file stepping.', action='store', type=int)
parser.add_argument("--delay_avg", help="sfsdfasdfsf", action="store_true")
parser.add_argument("--multi_delayavg", help="sfsdfsdff", action="store_true")
args = parser.parse_args()

if not args.step is None:
    opts = ["-c " + args.calfile, "-p " + args.pol]
    if args.time_avg:
        opts.append("-t")
    if not args.ex_ants is None:
        opts.append("-x={}".format(args.ex_ants))

    files_all = [file for file in args.filenames if 'xx' in file]

    for file_index in range(0, len(files_all), args.step):
        cmd = opts + ["-f"] + files_all[file_index : file_index + args.step]
        
        print "I just executed the following arguments:"
        pprint.pprint(cmd)
        
        os.system("python2.7 getWedge.py {}".format(" ".join(cmd)))
        
        print
    quit()

pols = args.pol.split(",")

if not args.ex_ants is None:
    ex_ants_list = map(int, args.ex_ants.split(','))
else:
    ex_ants_list = []

if pols == ['stokes']:
    filenames = []
    for pol in ['xx','xy','yx','yy']:
        #make a list of all filenames for each polarization
        pol_filenames = []
        for filename in args.filenames:
            #replace polarization in the filename with pol we want to see
            filepol = filename.split('.')[-3]
            new_filename = filename.split(filepol)[0]+pol+filename.split(filepol)[1]
            #append it if it's not already there
            if not any(new_filename in s for s in pol_filenames):
                pol_filenames.append(new_filename)
        filenames.append(pol_filenames)
    #calculate and get the names of the npz files
    npz_names = wedge_utils.wedge_stokes(filenames, args.calfile.split('.')[0], ex_ants_list)

#XXX need to keep npz funcs here, move plotting to plotWedge.py
#if args.delay_avg and (len(pols) == 1 ):
#    for filename in args.filenames:
#        wedge_utils.fork2wedge(filename)

#if args.multi_delayavg and (len(pols) == 1 ):
#    for filename in args.filenames:    
#        wedge_utils.plot_multi_delayavg(filename)

elif len(pols) == 1:
    if args.time_avg:
        npz_name = wedge_utils.wedge_timeavg(args.filenames, args.pol, args.calfile.split('.')[0], ex_ants_list)
    else:
        npz_name = wedge_utils.wedge_blavg(args.filenames, args.pol, args.calfile.split('.')[0], ex_ants_list)

elif len(pols) > 1:
    npz_names = []
    for pol in pols:
        #make a list of all filenames for each polarization
        filenames = []
        for filename in args.filenames:
            #replace polarization in the filename with pol we want to see
            filepol = filename.split('.')[-3]
            new_filename = filename.split(filepol)[0]+pol+filename.split(filepol)[1]
            #append it if it's not already there
            if not any(new_filename in s for s in filenames):
                filenames.append(new_filename)
        npz_names.append(wedge_utils.wedge_timeavg(filenames, pol, args.calfile.split('.')[0], ex_ants_list))