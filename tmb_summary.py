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
    parser.add_argument('-o','--outputF', help='TMB output file', required=True)
    args = parser.parse_args()
    inputDir = os.path.abspath(args.inputDir)
    outputF = os.path.abspath(args.outputF)

    sn_list = glob.glob('{}/Logs_Intermediates/SampleAnalysisResults/*SampleAnalysisResults.json'.format(inputDir))
    with open(outputF,'w') as fo:
        fo.write('Sample ID\tTotal TMB\tCoding Region size in Megabases\tNumber of Passing Eligible Variants\n')
        for i in sn_list:
            print(i)
            sn=i.split('/')[-1].split('_SampleAnalysisResults.json')[0]
            with open(i) as json_file:
                data_loaded = json.load(json_file)
                if data_loaded['data']["biomarkers"]:
                    entree = data_loaded['data']["biomarkers"]['tumorMutationalBurden']
                    Total_TMB = entree['tumorMutationalBurdenPerMegabase']
                    if entree['additionalMetrics'][0]['name'] == "CodingRegionSizeMb":
                        Coding_Region_Size_in_Megabases = entree['additionalMetrics'][0]["value"]
                    if entree['additionalMetrics'][1]['name'] == "SomaticCodingVariantsCount":
                        Eligible_Variants_Count = entree['additionalMetrics'][1]["value"]
                    
                    fo.write('{}\t{}\t{}\n'.format(sn, Total_TMB,Coding_Region_Size_in_Megabases,Eligible_Variants_Count))
                else:
                    # in case samples have no data
                    Total_TMB = 'NA'
                    Coding_Region_Size_in_Megabases = 'NA'
                    Eligible_Variants_Count = 'NA'
                    fo.write('{}\t{}\t{}\n'.format(sn, Total_TMB,Coding_Region_Size_in_Megabases,Eligible_Variants_Count))
if __name__=="__main__": __main__()
