import os, sys,random,shutil
import argparse

homeDir = None#os.environ["HOME"]
srcFolder = None #sys.argv[1]
# Src folder is a 'design' folder under abcScripts from where the scripts to be copied.
graphDataFolder = None #os.path.join(homeDir,"OPENABC_DATASET","bench")
scriptsDataFolder = None #os.path.join(homeDir,"OPENABC_DATASET","synScripts")
libraryCellFolder = None #os.path.join(homeDir,"OPENABC_DATASET","lib")


numSynthesizedScript = 1500
delimiter = "\n"
designSet1 = ['i2c','spi','des3_area','ss_pcm','usb_phy','sasc','wb_dma','simple_spi']
designSet2 = ['dynamic_node','aes','pci','ac97_ctrl','mem_ctrl','tv80','fpu']
designSet3 = ['wb_conmax','tinyRocket','aes_xcrypt','aes_secworks']
designSet4 = ['jpeg','bp_be','ethernet','vga_lcd','picosoc']
designSet5 = ['dft','idft','fir','iir','sha256']
designs = designSet1+designSet2+designSet3+designSet4+designSet5


## Perform all the optimization steps for all the designs

def genSynthesisScripts():
    for i in range(numSynthesizedScript):
        srcFile = os.path.join(srcFolder,'abc'+str(i)+'.script')
        origScriptFile = open(srcFile,'r')
        fileLines = origScriptFile.readlines()
        origScriptFile.close()
        for des in designs:
            scriptFolder = os.path.join(scriptsDataFolder,des)
            if(not os.path.exists(scriptFolder)):
                os.mkdir(scriptFolder)
            graphDumpFolder = os.path.join(graphDataFolder,des)
            scriptFilePath = os.path.join(scriptFolder, 'abc' + str(i) + '.script')
            scriptFile = open(scriptFilePath, 'w+')
            readLibLine = "read "+os.path.join(libraryCellFolder,"nangate45.lib")+delimiter
            scriptFile.write(readLibLine)
            fileLines[1] = "read_bench "+graphDumpFolder+os.sep+des+"_orig.bench"+delimiter
            scriptFile.write(fileLines[1])
            scriptFile.write("strash"+delimiter)
            firstPathFileName = os.path.join(graphDumpFolder, "syn" + str(i),des + "_syn" + str(i) + "_step0.bench"+delimiter)
            dumpFirstGraphLine = "write_bench -l " + firstPathFileName
            scriptFile.write(dumpFirstGraphLine)
            numSteps = 1
            for line in fileLines[2:-8]:
                scriptFile.write(line)
                intermediatePathFileName = os.path.join(graphDumpFolder,"syn"+str(i),des+"_syn"+str(i)+"_step"+str(numSteps)+".bench"+delimiter)
                dumpIntermediateGraphLine = "write_bench -l " + intermediatePathFileName
                scriptFile.write(dumpIntermediateGraphLine)
                numSteps+=1
            scriptFile.write("map -B 0.9"+delimiter+"topo"+delimiter+"stime -c"+delimiter)
            scriptFile.close()


def _read_designs(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def setGlobalAndEnvironmentVars(cmdArgs):
    global homeDir, srcFolder, graphDataFolder, scriptsDataFolder, libraryCellFolder, designs, numSynthesizedScript
    homeDir = cmdArgs.home
    srcFolder = cmdArgs.script
    if not (os.path.exists(homeDir) and os.path.exists(srcFolder)):
        print("\nPlease rerun with appropriate paths")
    graphDataFolder = os.path.join(homeDir, "OPENABC_DATASET", "bench")
    scriptsDataFolder = os.path.join(homeDir, "OPENABC_DATASET", "synScripts")
    libraryCellFolder = os.path.join(homeDir, "OPENABC_DATASET", "lib")
    if cmdArgs.designs_file:
        designs = _read_designs(cmdArgs.designs_file)
    if cmdArgs.num_scripts is not None:
        numSynthesizedScript = cmdArgs.num_scripts

def parseCmdLineArgs():
    parser = argparse.ArgumentParser(prog='SYNTHESIS RECIPE GENERATOR', description="Circuit characteristics")
    parser.add_argument('--version',action='version', version='1.0.0')
    parser.add_argument('--home',required=True, help="OpenABC dataset home path")
    parser.add_argument('--script', required=True, help="Sample script folder path of 1500 synthesis scripts")
    parser.add_argument('--designs-file', help="Optional path to designs.txt")
    parser.add_argument('--num-scripts', type=int, help="Override number of synthesis scripts")
    return parser.parse_args()

def main():
    cmdArgs = parseCmdLineArgs()
    setGlobalAndEnvironmentVars(cmdArgs)
    genSynthesisScripts()

if __name__ == '__main__':
    main()
