import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('input_folder', type=str, help='source folder with extracted UNCOMPRESSED wiki files')
parser.add_argument('target', type=str, help='target file name to store xml file in')
parser.add_argument('-d','--delete_old', action='store_true', help='remove extracted files')

args = parser.parse_args()
cmd = 'find ' + args.input_folder + ' -name "wiki*" -exec cat {} + >> ' + args.target
os.system(cmd)

os.system('grep -o "<doc" ' + args.target + ' | wc -w')
os.system("sed -i 's/<[^>]*>//g' " + args.target)

if args.delete_old:
    shutil.rmtree(args.input_folder)
    print('deleted old files')