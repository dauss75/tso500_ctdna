#!/usr/bin/python

"""
Created on Oct 31, 2024
@author: segun.jung
"""

import json
import os
import argparse
import glob

def __main__():
    parser = argparse.ArgumentParser(description='extract MSI')
    parser.add_argument('-i','--inputDir', help='LBx pipeline output folder', required=True)
    parser.add_argument('-o','--outputF', help='CNV output file', required=True)
    args = parser.parse_args()
    inputDir = os.path.abspath(args.inputDir)
    outputF = os.path.abspath(args.outputF)

    sn_list = glob.glob('{}/Logs_Intermediates/SampleAnalysisResults/*SampleAnalysisResults.json'.format(inputDir))
    with open(outputF,'w') as fo:
        fo.write('Sample ID\tGene\tFold Change\n')
        for i in sn_list:
            print(i)
            sn=i.split('/')[-1].split('_SampleAnalysisResults.json')[0]
            with open(i) as json_file:
                data_loaded = json.load(json_file)
                if data_loaded['data']["biomarkers"]:
                    cnv = data_loaded['data']["variants"]["copyNumberVariants"]
                    for entree in cnv:
                        cnv_gene = entree['gene']
                        cnv_fc = entree['foldChange']
                        fo.write('{}\t{}\t{}\n'.format(sn, cnv_gene,cnv_fc))
                else:
                    # in case samples have no data
                    cnv_gene = 'NA'
                    cnv_fc = 'NA'
                    fo.write('{}\t{}\t{}\n'.format(sn, cnv_gene,cnv_fc))
if __name__=="__main__": __main__()
