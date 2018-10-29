'''
Calculates the Levenshtein distance of a string against the members of a 
Series of strings, to determine how similar they are. Specifically meant to be 
used for fuzzy string matching when a gold standard data set for the strings 
is known. Can also be used for clustering similar text if the gold standard is 
unknown or more of a "brass standard."
'''

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import numpy as np

def best_option(value, correct_values, 
    cluster = False, scorer = 'token_set_ratio',
    score_threshold = 90):
    '''
    Takes a string value and returns the original string, the recommended gold standard string, and the score for that set.

    Parameters
    ----------
    value: str. String that you want to compare against.

    correct_values: pandas Series of str values. Represents all of the 
    allowed, gold standard values for the strings in data. If no gold standard 
    data are available, set cluster = True and pass the Series of which value 
    is a member to this parameter.

    cluster: bool. Determines if best_option should assume that clustering is desired, instead of comparison to a gold standard data set. If True, will assume that value is already in correct_values and ignore that perfect match in favor of a less optimal one. If using this feature, pass the Series that contains value for correct_values.

    scorer: str. Indicates what fuzzywuzzy scorer you want to use. Choices are:
                
                None: uses the simple fuzz.ratio() scorer. Not usually 
                    recommended.

                'partial_ratio': matches on substrings to give a higher match 
                    score than would result from simple full string comparison.
                    For example, simple fuzz.ratio() would return 60 for a 
                    comparison of "Yankees" to "New York Yankees". But
                    fuzz.partial_ratio() returns 100.

                'token_set_ratio': the default. Tokenizes the string 
                    (separates words into substrings, makes everything lower 
                    case, removes punctuation), determines the most 
                    intersecting substrings, and weights the score based 
                    upon how much intersection there is, while discarding 
                    duplicate tokens. Also alphabetizes tokens prior to 
                    sorting. Probably the most flexible option.

                'token_sort_ratio': similar to token_set_ratio, but more 
                    simplistic, only doing the tokenizing and sorting aspects.
                    Potentially a good compromise option.

    score_threshold: int. Establishes the fuzzy match score that is the 
                        lowest allowed value before just returning NaN. 

    Returns
    --------
    pandas Series of the format original value, top suggested value to replace 
    it, and the score of the top suggested replacement. 


    If value is None or null, it returns (value, value, 0)

    If an element in correct_values is null, it is ignored

    If an element in correct_values is null, it is ignored

    If a match scores below 90, it returns (value, NaN, score of bad 
    match
    '''

    #Check that scorer has a meaningful value
    if scorer not in [None, 'partial_ratio', 
    'token_set_ratio', 'token_sort_ratio']:
        raise ValueError("scorer parameter not set to allowed value")


    #Check that value isn't None or NaN
    if value is None or value is np.nan:
        return value, value, 0

    #Make sure null values in correct_values (which shouldn't be there in the 
        #first place!) are ignored
    correct_values = correct_values.dropna().drop_duplicates()


    #Have a gold standard data set? Not already in there is it?
    #Don't want to waste time doing pairwise scoring for values that are 
        #already gold standard
    if not cluster and value in list(correct_values):  
        return value, value, 100


    #Are we not using gold standard data but actually trying to find
        #the closest match of a value within correct_values?
        #If so, ignore the value itself (perfect match by default)
    if cluster and value in list(correct_values):
        correct_values = correct_values[correct_values != value]

        #TODO: more efficient to use Series method for "is in" check?

    if scorer == 'token_set_ratio':
        new_value, score = process.extractOne(value, list(correct_values),
            scorer = fuzz.token_set_ratio)

    elif scorer == 'token_sort_ratio':
        new_value, score = process.extractOne(value, list(correct_values),
            scorer = fuzz.token_sort_ratio)

    elif scorer == 'partial_ratio':
        new_value, score = process.extractOne(value, list(correct_values),
            scorer = fuzz.partial_ratio)

    else:
        new_value, score = process.extractOne(value, list(correct_values))



    if score < score_threshold:
        return value, np.nan, score

    else:
        return value, new_value, score