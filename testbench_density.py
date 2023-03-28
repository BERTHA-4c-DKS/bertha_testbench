import os
import sys
import shutil
import pickle
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
    maxthread = 4
    
    results = {}

    krgridvalues = [25,  50,  75, 100, 125, 150, 175, 200]
    kagridvalues = [86, 146, 194, 302, 434, 770, 974]
    
    for system in os.listdir(basedir):
        for input in os.listdir(basedir+"/"+system):
            if input == "input.inp" or input == "fitt2.inp":
                shutil.copyfile(basedir+"/"+system+"/"+input, dstdir+"/"+ input)

        for krgrid in krgridvalues:

            kagrid = -1
        
            print("Running system: ", system, file=sys.stderr)
            print("  Thread: ", maxthread, file=sys.stderr)
            print("  KRGRID: ", krgrid, file=sys.stderr)
            print("  KAGRID: ", kagrid, file=sys.stderr)
            result = subprocess.run([dstdir+"/"+"run_density.sh", \
                str(maxthread), str(krgrid), str(kagrid)], stdout=subprocess.PIPE)
    
            results[system+";"+str(maxthread)+";"+str(krgrid)+";"+str(kagrid)] = result.stdout
        
        for kagrid in kagridvalues:

            krgrid = -1
        
            print("Running system: ", system, file=sys.stderr)
            print("  Thread: ", maxthread, file=sys.stderr)
            print("  KRGRID: ", krgrid, file=sys.stderr)
            print("  KAGRID: ", kagrid, file=sys.stderr)
            result = subprocess.run([dstdir+"/"+"run_density.sh", \
                str(maxthread), str(krgrid), str(kagrid)], stdout=subprocess.PIPE)
    
            results[system+";"+str(maxthread)+";"+str(krgrid)+";"+str(kagrid)] = result.stdout

        for krgrid in krgridvalues:

            for  kagrid in kagridvalues:
        
                print("Running system: ", system, file=sys.stderr)
                print("  Thread: ", maxthread, file=sys.stderr)
                print("  KRGRID: ", krgrid, file=sys.stderr)
                print("  KAGRID: ", kagrid, file=sys.stderr)
                result = subprocess.run([dstdir+"/"+"run_density.sh", \
                    str(maxthread), str(krgrid), str(kagrid)], stdout=subprocess.PIPE)
            
                results[system+";"+str(maxthread)+";"+str(krgrid)+";"+str(kagrid)] = result.stdout

        filename = system
        with ZipFile(filename+".zip","w") as zip:
            for file in os.listdir(dstdir):
                if file.startswith("run_"+str(maxthread)+"_"):
                    zip.write(file)
            for file in os.listdir(dstdir):
                if file.startswith("run_"+str(maxthread)+"_"):
                    os.remove(file)

    with open('results_data.pkl', 'wb') as fp:
        pickle.dump(results, fp)
    