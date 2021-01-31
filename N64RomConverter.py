#!/bin/env python3
import sys

def getRomHead(byteArray):
    '''returns the head of the rom to determine file extension'''

    romHead = ''.join(format(x, '02x') for x in byteArray[:4])
    romHead = int(romHead, 16)
    return romHead

def readFile(fname):
    '''reads in the rom file and return a byte array'''

    with open(fname, "rb") as f:
        file_array = bytearray(f.read())
        return file_array

def writeFile(fname, data):
    '''writes the modified data back to the rom'''

    with open(fname, "wb") as f:
        f.write(data)

def printUsage():
    '''prints the usage for the script'''
    
    print("python3 N64RomConverter.py -i [INPUT] -o [OUTPUT] \n - [OUTPUT] must have one of these Extensions: n64, v64, z64")

def dWordSwap(byteArray):
    for i in range(0, len(byteArray), 4):
        byteArray = wordSwap2(byteArray, i, i + 3)
        byteArray = wordSwap2(byteArray, i + 1, i + 2)
    return byteArray

def wordSwap2(byteArray, a, b):
    temp = byteArray[a]
    byteArray[a] = byteArray[b]
    byteArray[b] = temp
    return byteArray

def wordSwap(byteArray):
    for i in range(0, len(byteArray), 2):
        byteArray = wordSwap2(byteArray, i, i + 1)
    return byteArray

def main():

    # Check args
    if len(sys.argv) != 5 or sys.argv[1] != "-i" or sys.argv[3] != "-o":
        printUsage()
        sys.exit(-1)

    # Get input file
    inputName = sys.argv[2]

    # Set output file name
    outputName = sys.argv[4]

    # Hold the bytes read in from the rom file
    romData = readFile(inputName)

    # Get input and output extensions
    inExtension  = inputName[-3:]
    outExtension = outputName[-3:]
    print("Converting from " + inExtension + " to " + outExtension)

    # Get rom head
    romHead = getRomHead(romData)

    # n64 format
    if 0x40123780 == romHead:
        if outExtension == "n64":
            pass
        elif outExtension == "z64":
            romData = dWordSwap(romData)
        elif outExtension == "v64":
            romData = wordSwap(dWordSwap(romData))

    # z64 format
    if 0x80371240 == romHead:
        if outExtension == "n64":
            romData = dWordSwap(romData)
        elif outExtension == "z64":
            pass
        elif outExtension == "v64":
            romData = wordSwap(romData)

    # v64 format
    if 0x37804012 == romHead:
        if outExtension == "n64":
            romData = dWordSwap(wordSwap(romData))
        elif outExtension == "z64":
            romData = wordSwap(romData)
        elif outExtension == "v64":
            pass

    # Write modified data back to rom
    writeFile(outputName, romData) 

if __name__ == "__main__":
    main()