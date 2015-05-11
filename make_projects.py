"""Python script to make projections about people living with diagnosed HIV."""


import os
import csv


def ReadCensusCounts():
    """Read in census counts from user specified file.
    
    Returns the dictionary *counts* where *counts[age][year]* is the 
    census counts of people of age *age* projected for year *year*."""
    infile = raw_input("Enter the census counts file: ")
    assert os.path.isfile(infile), "Cannot find census counts file %s" % infile
    firstrow = True
    years = []
    with open(infile) as f:
        for row in csv.reader(f):
            if firstrow:
                assert row[0] == 'year', "First row of census counts file doesn't begin with year"
                ages = [int(age) for age in row[1 : ]]
                counts = dict([(age, {}) for age in ages])
                firstrow = False
            else:
                assert len(row) == len(ages) + 1, "invalid number of entries in row in census counts file"
                year = int(row[0])
                for (n, age) in zip(row[1 : ], ages):
                    counts[age][year] = float(n)
    return counts


def ReadAgeCategoryData(datatype, lastage=100):
    """Read in age categorical data of indicated type.

    Returns the dictionary *d* where *d[a]* is the
    data for age category *a*. Age categories are indicated like this:
    *(13, 24)* or *(55, lastage)*.

    *datatype* specifies the type of data, should be the heading
    of the second column in the input data file.

    *lastage* is the highest age (used for a final category with a
    ``+`` upper bound).
    """
    infile = raw_input("Enter the name of the file containing the age category data for %s: " % datatype)
    assert os.path.isfile(infile), "Cannot find file %s" % infile
    firstrow = True
    d = {}
    with open(infile) as f:
        for row in csv.reader(f):
            assert len(row) == 2, "row does not have two entries"
            if firstrow:
                assert row[0] == 'age', 'title of first column is not "age"'
                assert row[1] == datatype, 'title of second column is not "%s"' % datatype
                firstrow = False
            else:
                agecategory = row[0]
                if agecategory.count('-'):
                    agecategory = tuple([int(a) for a in agecategory.split('-')])
                elif agecategory[-1] == '+':
                    agecategory = (int(agecategory[ : -1]), lastage)
                else:
                    raise ValueError("unrecognized age category: %s" % agecategory)
                n = float(row[1])
                d[agecategory] = n
    return d


def AgeCategorizeCensusData(age_categories, census_counts):
    """Returns an age categorized version of *census_counts*.

    In the new version *new_counts, for each age category *a* in *age_categories*,
    *new_counts[a][year]* is the projected number of individuals in category *a*
    in year *year*.
    """
    new_counts = {}
    years = census_counts[census_counts.keys()[0]].keys()
    categorized_ages = set([])
    for age_category in age_categories:
        ages = [a for a in range(age_category[0], age_category[1] + 1)]
        assert not categorized_ages.intersection(ages), "overlapping age categories, not allowed"
        new_counts[age_category] = {}
        for year in years:
            new_counts[age_category][year] = sum([census_counts[a][year] for a in ages])
    return new_counts



def main():
    """Main body of script."""
    #
    # read in the data
    census_counts = ReadCensusCounts()
    diagnosis_rates = ReadAgeCategoryData('diagnosis rate', lastage=max(census_counts.keys()))
    mortality_rates = ReadAgeCategoryData('mortality rate')
    plwdh = ReadAgeCategoryData('PLWDH')
    #
    # check that the age categories are consistently defined
    age_categories = diagnosis_rates.keys()
    age_categories.sort()
    assert set(age_categories) == set(mortality_rates.keys()), "age categories differ for diagnosis and mortality"
    assert set(age_categories) == set(plwdh.keys()), "age categories differ for diagnosis and PLWDH"
    census_counts = AgeCategorizeCensusData(age_categories, census_counts)
    assert set(age_categories) == set(census_counts.keys()), "age categories differ for diagnosis and census_counts"
    print census_counts
    


main() # run the script


