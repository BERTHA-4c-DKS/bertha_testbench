import os
import sys
import shutil
import subprocess

import numpy as np
from zipfile import ZipFile

class summirizedata:
    def __init__ (self):
        self.fitted_density = None
        self.fitted_density_unique = None 

        self.afitted_density = None
        self.afitted_density_unique = None

        self.total_energy = None
        self.total_energy_unique = None

        self.convergence = None
        self.convergence_unique = None

if __name__ == "__main__":

    basedir = "./testsystems"
    dstdir = "./"
    maxthread = 8
    
    results = {}
    
    for system in os.listdir(basedir):
        for input in os.listdir(basedir+"/"+system):
            shutil.copyfile(basedir+"/"+system+"/"+input, dstdir+"/"+ input)
        
        print("Running system: ", system, file=sys.stderr)
        print("  Thread: ", maxthread, file=sys.stderr)
    
        result = subprocess.run([dstdir+"/"+"run.sh", \
            str(maxthread)], stdout=subprocess.PIPE)
    
        results[system] = result.stdout

        filename  = system+"_maxthread_"+str(maxthread)
        with ZipFile(filename+".zip","w") as zip:
            for file in os.listdir(dstdir):
                if file.startswith("run_"):
                    zip.write(file)
            for file in os.listdir(dstdir):
                if file.startswith("run_"):
                    os.remove(file)
    