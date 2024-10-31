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
    parser.add_argument('-o','--outputF', help='MSI SUM_JSD output file', required=True)
    args = parser.parse_args()
    inputDir = os.path.abspath(args.inputDir)
    outputF = os.path.abspath(args.outputF)

    sn_list = glob.glob('{}/Logs_Intermediates/SampleAnalysisResults/*SampleAnalysisResults.json'.format(inputDir))
    with open(outputF,'w') as fo:
        fo.write('Sample_ID\tSUM_JSD\n')
        for i in sn_list:
            sn=i.split('/')[-1].split('_SampleAnalysisResults.json')[0]
            with open(i) as json_file:
                data_loaded = json.load(json_file)
                if data_loaded['data']["biomarkers"]:
                    sum_jsd = data_loaded['data']["biomarkers"]["microsatelliteInstability"]["additionalMetrics"][0]["value"]
                else:
                    # in case samples have no data
                    sum_jsd = 'NA'
            fo.write('{}\t{}\n'.format(sn, sum_jsd))
if __name__=="__main__": __main__()
