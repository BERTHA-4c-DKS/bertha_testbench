import os
import shutil
import subprocess

import numpy as np

class summirizedata:
    def __init__ (self):
        self.fitted_density = None
        self.fitted_density_unique = None 

        self.functional_energy = None
        self.functional_energy_unique = None 

        self.vxc = None
        self.vxc_unique = None

        self.total_energy = None
        self.total_energy_unique = None

        self.convergence = None
        self.convergence_unique = None

        self.cputime_avg = None
        self.cputime_stdev = None
        self.walltime_avg = None
        self.walltime_stdev = None

        self.memory_avg = None
        self.memory_stdev = None

if __name__ == "__main__":

    basedir = "./testsystems"
    dstdir = "./"
    maxthread = 5
    maxrun = 4
    
    results = {}
    
    for system in os.listdir(basedir):
        for input in os.listdir(basedir+"/"+system):
            shutil.copyfile(basedir+"/"+system+"/"+input, dstdir+"/"+ input)
        
        print("Running system: ", system)
        print("  Maxthread: ", maxthread)
        print("  Maxrun:    ", maxrun)
    
        for threadsched in ["dynamic", "static"]:
            print("  Sched:     ", threadsched)
            for model in range(1,5):
                print("  Model:     ", model)
    
                result = subprocess.run([dstdir+"/"+"run.sh", \
                    str(maxthread),  \
                    str(model), \
                    threadsched,  \
                    str(maxrun)], stdout=subprocess.PIPE)
    
                results[system+";"+threadsched+";"+str(model)] = result.stdout
    
                #print(result.stdout)
                #print(result.stderr)
    
            
    collectionresults = {}
    for key in results:
        system = key.split(";")[0]
        scheduling = key.split(";")[1]
        model = key.split(";")[2]
    
        print("System: ", system, \
            " Scheduler: ", scheduling, \
            " Model: ", model)
    
        startnumth = False
        runcounter = 0
        numoftread = 0
    
        fitted_density = []
        functional_enerhy = []
        vxc = []
        total_energy = []
        convergence = []
        totalwtime = []
        totalctime = []
        memory = []
        for line in results[key].decode('utf-8').split("\n"): 
            if startnumth:
                if line.find("total fitted density") >= 0:
                    val = float(line.split()[-1])
                    fitted_density.append(val)
                elif line.find("functional energy") >= 0:
                    val = float(line.split()[-1])
                    functional_enerhy.append(val)
                elif line.find("vxc[fit]*rho[fit]") >= 0:
                    val = float(line.split()[-1])
                    vxc.append(val)
                elif line.find("total energy") >= 0:
                    val = float(line.split()[-1])
                    total_energy.append(val)
                elif line.find("convergence obtained in") >= 0:
                    val = int(line.split()[-2])
                    convergence.append(val)
                elif line.find("Total time for iteration") >= 0:
                    walltime = float(line.split()[-3])
                    cputime = float(line.split()[-1])
                    totalwtime.append(walltime)
                    totalctime.append(cputime)
                elif line.find("Maximum resident set size") >= 0:
                    val = float(line.split()[-1])
                    memory.append(val)
    
                if line.find("Maximum resident set size") >= 0:
                    runcounter += 1
            
            if runcounter >= maxrun:
                startnumth = False
                runcounter = 0
    
                if len(fitted_density) > 0:
                    uniquekey = key + ";" + str(numoftread)
                    datatostore = summirizedata()
                    
                    #print("Num. of Threads ", numoftread)
                    
                    f_density = set(fitted_density)
                    f_density_unique = (len(f_density) == 1)
                    datatostore.fitted_density = f_density
                    datatostore.fitted_density_unique = f_density_unique
                    #print("Fitted Density Unique",f_density_unique)
                    
                    f_energy = set(functional_enerhy)
                    f_energy_unique = (len(f_energy) == 1)
                    datatostore.functional_energy = f_energy
                    datatostore.functional_energy_unique = f_energy_unique
                    #print("Functional Energy Unique", f_energy_unique)
                    
                    s_vxc = set(vxc)
                    s_vxc_unique = (len(s_vxc) == 1)
                    datatostore.vxc = s_vxc
                    datatostore.vxc_unique = s_vxc_unique
                    #print("vxc[fit]*rho[fit] Unique", s_vxc_unique)
                    
                    t_energy = set(total_energy)
                    t_energy_unique = (len(t_energy) == 1)
                    datatostore.total_energy = t_energy
                    datatostore.total_energy_unique = t_energy_unique
                    #print("Total Enerhy Unique ", t_energy_unique)
                    
                    s_convergence = set(convergence)
                    s_convergence_unique = (len(s_convergence) == 1)
                    datatostore.convergence = s_convergence
                    datatostore.convergence_unique = s_convergence_unique
                    #print("Convergence Unique ", s_convergence_unique)
                    
                    avgtotalctime = np.mean(totalctime)
                    datatostore.cputime_avg = avgtotalctime
                    datatostore.cputime_stdev = np.std (totalctime)
                    #print(" CPUTIME: %10.5f s"%(avgtotalctime))
                    avgtotalwtime = np.mean(totalwtime)
                    datatostore.walltime_avg = avgtotalwtime
                    datatostore.walltime_stdev = np.std(totalwtime)
                    #print("WALLTIME: %10.5f s"%(avgtotalwtime))
                    
                    collectionresults[uniquekey] = datatostore
    
                fitted_density = []
                functional_enerhy = []
                vxc = []
                total_energy = []
                convergence = []
                totalctime = []
                totalwtime = []
                memory = []
    
            if line.startswith("Num. of Threads:"):
                startnumth = True
                numoftread = int(line.split()[-1])

    print("System , Scheduling , Model , NumOfThreads , " + \
        "FittedDensityUnique , FittedDensity ," + \
        "FunctionalEnergyUnique , FunctionalEnergy ," + \
        "VxcUnique , Vxc , "+ \
        "TotalEnergyUnique , TotalEnergy , " + \
        "CpuTime , WallTime , Memory ")
    
    for key in collectionresults:
        system = key.split(";")[0]
        scheduling = key.split(";")[1]
        model = key.split(";")[2]
        numoth = key.split(";")[3]
    
        data = collectionresults[key]
    
        if (len(data.fitted_density) > 0):
    
            print (system, " , ",  scheduling, " , ", model, " , ", numoth, " , ", \
                data.fitted_density_unique," , ", list(data.fitted_density)[-1], " , ", \
                data.functional_energy_unique," , ", list(data.functional_energy)[-1], " , ", \
                data.vxc_unique," , ", list(data.vxc)[-1], " , ", \
                data.total_energy," , ", list(data.total_energy)[-1], " , ", \
                data.cputime_avg," , ", data.walltime_avg ," , ", \
                data.memory_avg)
    
