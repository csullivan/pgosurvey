#import matplotlib
#matplotlib.use('Agg')

import os as os
import os.path as path
import numpy as np
import pylab
from pylab import *
from setfont import setfont
import csv

# A simple class for reading data from file and return a list of lists
# in the form 
# [[1st_entry_in_col1,1st_entry_in_col2,...,1st_entry_in_coln],
#  [2nd_entry_in_col1,2nd_entry_in_col2,...,2nd_entry_in_coln],
#  ...,
#  [nth_entry_in_col1,nth_entry_in_col2,...,nth_entry_in_coln]]
class FileData(object):
    def __init__(self,datafile):
        self.table = []               
        for line in open(datafile):
            entries = line.split()
            self.table.append(entries);


def input_parser(file,searchExp):
    input_file = open(file)
    for line in input_file:
        if searchExp in line:
            if searchExp == 'Directory':
                return line.split()[1].rstrip()
            if searchExp == 'Runs':
                files = []
                while True:
                    try:
                        line = next(input_file)
                        if line == '\n':
                            """ Break if empty line is 
                            found after reading last state """
                            break
                    except:
                        break
                    files.append(line.rstrip())
                return files    

def read_file(csvfile):
    with open(csvfile, 'r') as f:
        data = [row for row in csv.reader(f.read().splitlines())]
        return data

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class survey_results(object):    
    def __init__(self,csvdata,criteria):
        self.criteria = criteria
        # [index, list of criteria to match, list for each criteria that holds lists for each question [ [ [],[],[],[],..., [] ], [ ... ] , ... , [ ... ] ]
        #                                                                                                     ^ question          ^ criteria

        for criterion in criteria:
            for k,specific_crit in enumerate(criterion[1]):
                criterion[2].append([])
            for specific_crit_list in criterion[2]:
                for i in range(0,len(csvdata[0])):
                    specific_crit_list.append([])



        # i iterates over questions
        for i in range(0,len(csvdata[0])):
            data = []
            if not is_number(csvdata[1,i]):
                continue
            # j iterates over responses
            for j in range(0,len(csvdata[:,0])):
                if csvdata[j,i] == '':
                    continue
                for criterion in criteria:                    
                    for k,specific_crit in enumerate(criterion[1]):
                        if csvdata[j,criterion[0]]==specific_crit:
                            criterion[2][k][i].append(float(csvdata[j,i]))

        # criteria:
        # [criterion object][element of criterion object
        #                    0=csvdata index used for comparison,
        #                    1=list of specific criterion to match,
        #                    2=list of data (list for each question)][list for each criterion][data]
        #                   > <               > <      these indices correspond to one another, they are the criteria, ie year, or

        #print criteria[0][1][7],np.average(criteria[0][2][7][1])



        
    def get_avg_based_on_criteria(self,criteria,question_index):
        for criterion in self.criteria:
            for i,specific_crit in enumerate(criterion[1]):
                cut_data = criterion[2][i]
                if len(cut_data[question_index]) and specific_crit == criteria:
                    return np.average(cut_data[question_index])

    def get_answers_based_on_criteria(self,criteria,question_index):
        for criterion in self.criteria:
            for i,specific_crit in enumerate(criterion[1]):
                cut_data = criterion[2][i]
                if len(cut_data[question_index]) and specific_crit == criteria:
                    return cut_data[question_index]
            
    



if __name__=='__main__':
    setfont()

    datafile = 'survey_results.csv'
    csvdata = np.asarray(read_file(datafile))
    subfields = set(csvdata[1:,-4])
    years = set(csvdata[1:,-5])
    thexp = set(csvdata[1:,-3])
    gender = set(csvdata[1:,-8])
    martial = set(csvdata[1:,-6])
    reside = set(csvdata[1:,-7])
    criteria = [  [-5,list(years),[]]  ,  [-4,list(subfields),[]]  ,  [-3,list(thexp),[]]  ,  [-8,list(gender),[]], [-6,list(martial),[]], [-7,list(reside),[]]  ]
    results = survey_results(csvdata,criteria)
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#333333']

    fig = pylab.figure(figsize=(11,8.5))

    nplot = 0
    pplot = 0
    for i in range(1,len(csvdata[0])):
        if nplot == 25:
            print " "
            fig.savefig('/user/sullivan/public_html/surveyhist_'+str(pplot)+'.pdf')
            pylab.clf()
            pplot += 1
            nplot = 0
        if not is_number(csvdata[1,i]):
            continue

        q_total = [float(x) for x in csvdata[1:,i] if x != '']
        if np.average(q_total) < 1.0:
            continue

        ax = fig.add_subplot(5,5,nplot+1)
        
        print i, csvdata[0,i]
        #fig = pylab.figure(figsize=(8,5))
        #ax = fig.add_subplot(111)
        ylep_hist = pylab.hist(q_total,bins=11,color='black',histtype='step')
        for k,criterion in enumerate(criteria[3][1]):
            if criterion != "":
                cutdata = results.get_answers_based_on_criteria(criterion,i)
                if cutdata == None:
                    continue
                if len(cutdata) > 4:
                    avg = np.average(cutdata)
                    pylab.axvline(avg,label=criterion,color=colors[k-1])
                    #ax.annotate("PHY",xy=(avg,25),xytext=(avg,25))
        text(0.1, 0.9, str(i), fontsize=10,ha='center', va='center',transform=ax.transAxes,color='red')
        pylab.xlabel(r"Responses")
        pylab.xlim(0.0,10.0)
        pylab.ylim(0,50)
        #pylab.subplots_adjust(right=0.7)
        if nplot == 0 or nplot == 25:
            pylab.legend(loc=2, prop={'size':8})
        nplot += 1

        
    
    







