#import modules
import os
import glob
import pandas as pd
#list all csv files only

def merge_csv(path_files) :
    """ Merge all csv files in path_files

    Args:
        path_files (string): dir path
    """
    cv_append = pd.DataFrame()

    for file in path_files : 
        print('\nMergin file : %s'%file)
        temp = pd.read_csv(file)
        cv_append = cv_append.append(temp,ignore_index = True)

    cv_append.dropna()
    cv_append.to_csv('./Generation/data/merge_csv/movie_data_merge_2.csv')


csv_unnamed_files = glob.glob('./Generation/data/unnamed/*.{}'.format('csv'))
csv_named_files = glob.glob('./Generation/data/named/*.{}'.format('csv'))


if __name__ == "__main__" : 
    merge_csv(csv_unnamed_files)
