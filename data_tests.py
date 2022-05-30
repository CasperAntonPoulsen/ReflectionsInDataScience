import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, chisquare, ranksums, median_test
import matplotlib.pyplot as plt
import powerlaw
#%%
#define functions
#function for getting posts at specified age in days
def get_day_df(df, day, days_column='days_passed'):
    return df[df[days_column] == day]

def get_treatment_control_arrays(df, value_column='score', treatment_column='isExperimental'):
    #split dataframe into treatment and control
    experimental_index = df[treatment_column]
    treatment_df = df[experimental_index]
    control_df = df[~experimental_index]
    #create arrays of values
    treatment_array = np.array(treatment_df[value_column])
    control_array = np.array(control_df[value_column])
    return treatment_array, control_array
    

#function for calculating the number of additional votes and score for posts 
def calculate_additional_votes_and_score(df, treatment_column='isExperimental', votes_column='nVotes', comments_column='nComments'):
    #one vote is subtracted from all posts since all posts automatically start with one vote from the author 
    df['additional_votes'] = df[votes_column] - 1
    #an additional vote is subtracted from experimental posts
    experimental_index = df[treatment_column]
    df.loc[experimental_index, 'additional_votes'] = df[df[treatment_column]]['additional_votes'] - 1
    #score is the sum of additional votes and comments
    df['score'] = df['additional_votes'] + df['nComments']


def perform_chi2_test(treatment_array, control_array):
    n_treatment = len(treatment_array)
    n_control = len(control_array)
    #count number of posts with additional score
    treatment_additional = np.sum(treatment_array >= 1)
    treatment_not = n_treatment-treatment_additional
    treatment_pct = treatment_additional/n_treatment
    control_additional = np.sum(control_array >= 1)
    control_pct = control_additional/n_control
    chi2_observed = [treatment_additional, treatment_not]
    #sum of observed and expected must be the same so expected is calculated from control pct and 
    control_additional_adjusted = int(control_pct*n_treatment)
    control_not_adjusted = n_treatment-control_additional_adjusted
    chi2_expected = [control_additional_adjusted, control_not_adjusted]
    #perform chi2 test
    chi2 = chisquare(chi2_observed, chi2_expected)
    return chi2[0], chi2[1], treatment_pct*100, control_pct*100


#%%
#read data
first_batch_file = 'first_batch_wdays.csv'
second_batch_file = 'second_batch_wdays.csv'
first_df = pd.read_csv(first_batch_file, sep = ';')
second_df = pd.read_csv(second_batch_file, sep = ';')
#calculate additional votes
calculate_additional_votes_and_score(first_df)
calculate_additional_votes_and_score(second_df)
#%%
#loop through days and perform statistical tests
value_column = 'additional_votes'
ranksum_alternative = 'greater'
ks_alternative = 'two-sided'
for day in range(7,8):
    day_first_df  = get_day_df(first_df, day)
    day_second_df = get_day_df(second_df, day)
    treatment_array_first, control_array_first = get_treatment_control_arrays(day_first_df, value_column=value_column)
    treatment_array_second, control_array_second = get_treatment_control_arrays(day_second_df, value_column=value_column)
    print('Day {}'.format(day))
    print('First batch count  treatment: {} control: {}'.format(len(treatment_array_first), len(control_array_first)))
    print('Second batch count treatment: {} control: {}'.format(len(treatment_array_second), len(control_array_second)))
    #calculate simple metrics
    #mean
    print('First batch mean  treatment: {:.1f} control: {:.1f}'.format(np.mean(treatment_array_first), np.mean(control_array_first)))
    print('Second batch mean treatment: {:.1f} control: {:.1f}'.format(np.mean(treatment_array_second), np.mean(control_array_second)))
    #median
    print('First batch median  treatment: {} control: {}'.format(np.median(treatment_array_first), np.median(control_array_first)))
    print('Second batch median treatment: {} control: {}'.format(np.median(treatment_array_second), np.median(control_array_second)))
    #perform median test
    median_stat_first, median_p_first, median_med_first, median_mat_first = median_test(treatment_array_first, control_array_first)
    median_stat_second, median_p_second, median_med_second, median_mat_second = median_test(treatment_array_second, control_array_second)
    print('First batch  median test p:{:.4f}'.format(median_p_first))
    print('Second batch median test p:{:.4f}'.format(median_p_second))
    #perform chi2 test and calculate pct succesfull
    chi2_first, chi2_p_first, succes_pct_t_first, succes_pct_c_first = perform_chi2_test(treatment_array_first, control_array_first)
    chi2_second, chi2_p_second, succes_pct_t_second, succes_pct_c_second = perform_chi2_test(treatment_array_second, control_array_second)
    print('First batch succes  chi2: {:.2f} p: {:.4f} treatment {:.1f}% control {:.1f}%'.format(chi2_first, chi2_p_first, succes_pct_t_first, succes_pct_c_first))
    print('Second batch succes chi2: {:.2f} p: {:.4f} treatment {:.1f}% control {:.1f}%'.format(chi2_second, chi2_p_second, succes_pct_t_second, succes_pct_c_second))
    #ranksum test to see if the underlying distribution of the treatment is greater than the control. Null hypothesis is nah son
    ranksum_res_first, ranksum_p_first = ranksums(treatment_array_first, control_array_first, ranksum_alternative)
    ranksum_res_second, ranksum_p_second = ranksums(treatment_array_second, control_array_second, ranksum_alternative)
    print('First batch  rank-sum: {:.2f} p: {:.4f}'.format(ranksum_res_first, ranksum_p_first))
    print('Second batch rank-sum: {:.2f} p: {:.4f}'.format(ranksum_res_second, ranksum_p_second))
    
    #Kolmogorov-Smirnoff test to check if treament and control are similar across batches
    ks_res_treatment, ks_p_treatment = ks_2samp(treatment_array_first, treatment_array_second, ks_alternative)
    ks_res_control, ks_p_control = ks_2samp(control_array_first, control_array_second, ks_alternative)
    print('Treatment KS: {:.2f} p: {:.3f}'.format(ks_res_treatment, ks_p_treatment))
    print('Control   KS: {:.2f} p: {:.3f}'.format(ks_res_control, ks_p_control))
    
