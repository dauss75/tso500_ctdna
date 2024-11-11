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
    parser.add_argument('-o','--outputF', help='DNA fusion output file', required=True)
    args = parser.parse_args()
    inputDir = os.path.abspath(args.inputDir)
    outputF = os.path.abspath(args.outputF)

    sn_list = glob.glob('{}/Logs_Intermediates/SampleAnalysisResults/*SampleAnalysisResults.json'.format(inputDir))
    with open(outputF,'w') as fo:
        fo.write('Sample ID\tFusion Call\tGene 1\tGene 2\tBreakpoint 1\tBreakpoint 2\tScore\tFilter\tReads Split by Junction\tReads Paired across Junction\tGene 1 Reference Reads\tGene 2 Reference Reads\tFusion Directionality Known\tGene A Location\tGene B Location\tGene A Sense\tGene B Sense\n')
        for i in sn_list:
            print(os.path.basename(i))
            sn=i.split('/')[-1].split('_SampleAnalysisResults.json')[0]
            with open(i) as json_file:
                data_loaded = json.load(json_file)
                if data_loaded['data']["biomarkers"]:
                    dna_fusion = data_loaded['data']["variants"]["dnaFusions"]
                    print(dna_fusion)
                    for entree in dna_fusion:
                        gene1 = entree['partner1']['gene']
                        breakpoint1 = '{}:{}'.format(entree['partner1']['chromosome'],entree['partner1']['position'])
                        ref_reads1 = entree['partner1']['referenceReads'] 
                        gene2 = entree['partner2']['gene']
                        breakpoint2 = '{}:{}'.format(entree['partner2']['chromosome'],entree['partner2']['position'])
                        ref_reads2 = entree['partner2']['referenceReads'] 
                        fusion_call = '{}-{}'.format(gene1,gene2)
                        score=''; gal=''; gbl='';gas='';gbs=''
                        filter = 'PASS'
                        rsbj= entree['fusionSupportingReads']
                        rpac= entree['totalReads']
                        fdk = entree["fusionDirectionalityKnownAndIndicatedByGeneOrder"]
                        fo.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(sn,fusion_call,gene1, gene2,breakpoint1,breakpoint2,score, filter, rsbj,rpac,ref_reads1,ref_reads2, fdk, gal, gbl, gas, gbs))
                else:
                    # in case samples have no data
                        gene1 = 'NA'
                        breakpoint1 = 'NA'
                        ref_reads1 = 'NA' 
                        gene2 = 'NA'
                        breakpoint2 = 'NA'
                        ref_reads2 = 'NA' 
                        fusion_call = 'NA'
                        score=''; gal=''; gbl='';gas='';gbs=''
                        filter = 'NA'
                        rsbj= 'NA'
                        rpac= 'NA'
                        fdk = 'NA'
                        fo.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(sn,fusion_call,gene1, gene2,breakpoint1,breakpoint2,score, filter, rsbj,rpac,ref_reads1,ref_reads2, fdk, gal, gbl, gas, gbs))
if __name__=="__main__": __main__()
