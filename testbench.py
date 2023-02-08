import os
import shutil
import subprocess

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

for v in results:
    print(results[v].decode('utf-8'))
        