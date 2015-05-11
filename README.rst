=======================
Demography model
=======================

This directory contains a demography model for HIV diagnosed individuals by Julia Hood.

.. contents::

The projection model
=====================

The goal is to project the number of individuals in some demographic category with HIV in the United States as a function of time and age. Let :math:`H_{a,t}` be the number of individuals in this demographic category diagnosed with HIV in age category :math:`a` at year :math:`t` (the times are years). We have the relationship

.. math::

    H_{a,t} &=& \left[\mbox{already diagnosed and stayed in age group}\right] + \left[\mbox{already diagnosed and aged in}\right] + \left[\mbox{newly diagnosed in age group}\right] + \left[\mbox{newly diagnosed and aged in}\right] \\
    &=& \left[H_{a,t - 1} \times \left(1 - \frac{1}{n_a}\right) \times \left(1 - M_{a}\right)\right] + \left[H_{a-1,t-1} \times \frac{1}{n_{a-1}} \times \left(1 - M_{a-1}\right)\right] + \left[N_{a,t-1} \times \left(1 - \frac{1}{n_a}\right) \times D_{a}\right] + \left[N_{a-1,t-1} \times \frac{1}{n_{a-1}} \times D_{a-1}\right]

where :math:`n_a` is the number of years in age category :math:`a` (e.g. for an age category of 13 to 24, :math:`n_a = 12`), where :math:`M_{a-1}` is the annual mortality rate of HIV-diagnosed individuals in age category :math:`a-1` in this demographic category, :math:`N_{a-1,t-1}` is the number of individuals in age category :math:`a-1` in the demographic category **not** diagnosed with HIV at year :math:`t`, and :math:`D_{a-1}` is the annual HIV diagnosis rate in the demographic category of individuals in age category :math:`a-1`. We also need to know the number :math:`N_{a,t}` of individuals in the demographic category **not** diagnosed with HIV. We have US census projections of the total number of individuals :math:`C_{a,t}` in the demographic category and age category :math:`a` at year :math:`t`, so we just note that 

:math:`C_{a,t} = N_{a,t} + H_{a,t}.`

This means we can substitute :math:`N_{a,t} = C_{a,t} - H_{a,t}` to rewrite our original equation as

.. math::
    H_{a,t} &=& \left[H_{a,t - 1} \times \left(1 - \frac{1}{n_a}\right) \times \left(1 - M_{a}\right)\right] + \left[H_{a-1,t-1} \times \frac{1}{n_{a-1}} \times \left(1 - M_{a-1}\right)\right] + \left[\left(C_{a,t-1} - H_{a,t-1}\right) \times \left(1 - \frac{1}{n_a}\right) \times D_{a}\right] + \left[\left(C_{a-1,t-1} - H_{a-1,t-1}\right) \times \frac{1}{n_{a-1}} \times D_{a-1}\right]


Running the program
====================
The ``Python`` program ``make_projections.py`` will make the projections. Simply run this program with ``Python``. It will ask you for the names of four files giving `The input data`_; you must provide it with the names of the four files in the formats described in `Input data file formats`_.

The input data
====================
The model is built on vectors of data:

* :math:`\mathbf{H_{0}}` is the vector of the :math:`H_{a,t=0}` values, giving the number of HIV diagnosed individuals in our demographic category at year :math:`t = 0` (whatever year we are using to start our projections) for each age category :math:`a`.

* :math:`\mathbf{M}` is the vector of the :math:`M_{a}` of the mortality rate of individuals diagnosed with HIV in age category :math:`a` in our demographic category. 

* :math:`\mathbf{D}` is the vector of the diagnosis rate :math:`D_a` of age group :math:`a` in our demographic category.

* :math:`\mathbf{C_t}` is the vector of the census counts of individual in our demographic category in age category :math:`a` for year :math:`t`. We have a vector provided by US Census data for each year :math:`t` that we are modeling.

Input data file formats
=========================
All of these files should be comma separated value (CSV) files in the following formats:

Census data
----------------------------
The census data should be specified in a format that looks like this: 

.. include:: census.csv
   :literal: 
   :end-line: 6
    
Note that these data should already be pre-processed so that they are **only for our demographic group of interest** (for instance, the counts only for white MSM). Also note that the census data does not need to be aggregated into age categories.

Diagnosis rate
---------------
The diagnosis rates should be specified in a format that looks like this:

.. include:: diagnosis_rate.csv
   :literal:
   :end-line: 6

Mortality rate
---------------
The mortality rates should be specified in a format that looks like this:

.. include:: mortality_rate.csv
   :literal:
   :end-line: 6

People living with diagnosed HIV
----------------------------------
The number of people living with diagnosed HIV should be specified in a format that looks like this:

.. include:: PLWDH.csv
   :literal:
   :end-line: 6

