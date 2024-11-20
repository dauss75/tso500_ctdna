#!/usr/bin/python

"""
Created on Nov 20, 2024
@author: segun.jung
"""

import json
import os
import argparse
import glob
import pandas as pd

def __main__():
    parser = argparse.ArgumentParser(description='extract MSI')
    parser.add_argument('-i','--inputDir', help='LBx pipeline output folder', required=True)
    parser.add_argument('-o','--outputF', help='MSI SUM_JSD output file', required=True)
    args = parser.parse_args()
    inputDir = os.path.abspath(args.inputDir)
    outputF = os.path.abspath(args.outputF)

    sn_list = glob.glob('{}/Logs_Intermediates/SampleAnalysisResults/*SampleAnalysisResults.json'.format(inputDir))
    sum_jsd_dic = {}
    for i in sn_list:
        sn=i.split('/')[-1].split('_SampleAnalysisResults.json')[0]
        with open(i) as json_file:
            data_loaded = json.load(json_file)
            if data_loaded['data']["biomarkers"]:
                sum_jsd = data_loaded['data']["biomarkers"]["microsatelliteInstability"]["additionalMetrics"][0]["value"]
                sum_jsd_dic[sn]=sum_jsd
            else:
                # in case samples have no data
                sum_jsd_dic[sn]='NA'
    df_sum_jsd=pd.DataFrame.from_dict([sum_jsd_dic]).T
    df_sum_jsd.rename(columns={0:'SUM_JSD'}, inplace=True)

    inputF='{}/Final_Results/TSO500_ctDNA_MSI_result.tsv'.format(inputDir)
    if os.path.exists(inputF):
        df = pd.read_csv(inputF,sep='\t')
        df_merged = df.merge(df_sum_jsd, left_on='sample_msi', right_index=True, how='left')
        df_merged.to_csv(outputF, sep='\t', index=False)
    else:
        df_sum_jsd=df_sum_jsd.rename_axis('sample_msi').reset_index()
        df_sum_jsd.to_csv(outputF, sep='\t', index=False)
if __name__=="__main__": __main__()
