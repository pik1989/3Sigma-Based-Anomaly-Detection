# Guide on Anomaly Detection

**Anomalies:**

Set of data points that are considerably different than the remainder of the data.

*Challenges*
How many outliers are there in the data?
Method is unsupervised - Validation can be quite challenging
Finding needle is a haystack.

*Working Assumption*
There are considerably more “normal” observations than “abnormal” observations in the data


**Anomaly Detection Scheme**

General Steps:
  Build a profile of the “normal” behavior.
    Profile can be patterns or summary statistics for the overall population.
Use the “normal” profile to detect anomalies
  Anomalies are observations whose characteristics differ significantly from the normal profile.

**Types of AD Scheme**

1. Statistical-based
2. Distance-based
3. Model-based

**Statistical Based**

If we know that the distribution of values in the sample is Gaussian or Gaussian-like, we can use the standard deviation of the sample as a cut-off for identifying outliers.

The Gaussian distribution has the property that the standard deviation from the mean can be used to reliably summarize the percentage of values in the sample.

For example, within one standard deviation of the mean will cover 68% of the data.
So, if the mean is 50 and the standard deviation is 5, as in the test dataset above, then all data in the sample between 45 and 55 will account for about 68% of the data sample. We can cover more of the data sample if we expand the range as follows:

  1 Standard Deviation from the Mean: 68%
  2 Standard Deviations from the Mean: 95%
  3 Standard Deviations from the Mean: 99.7%
  
A value that falls outside of 3 standard deviations is part of the distribution, but it is an unlikely or rare event at approximately 1 in 370 samples.

Three standard deviations from the mean is a common cut-off in practice for identifying outliers in a Gaussian or Gaussian-like distribution. For smaller samples of data, perhaps a value of 2 standard deviations (95%) can be used, and for larger samples, perhaps a value of 4 standard deviations (99.9%) can be used.

*Let’s make this concrete with a worked example:*

Sometimes, the data is standardized first (e.g. to a Z-score with zero mean and unit variance) so that the outlier detection can be performed using standard Z-score cut-off values. This is a convenience and is not required in general, and we will perform the calculations in the original scale of the data here to make things clear.
We can calculate the mean and standard deviation of a given sample, then calculate the cut-off for identifying outliers as more than 3 standard deviations from the mean.

*Algorithm:*
The following example shows how the average (mean) and standard deviation looks like for sample metric (CPU Utilization) on a specific device, when there are three points of data for three Mondays at 2:00 AM.
Collect three data points:

![Test Image 7](https://github.com/pik1989/3Sigma-Based-Anomaly-Detection/blob/master/images/Ex.PNG)

Calculate the population mean = (76+4+6)/3 = 28.67
The standard deviation for this example is 33.48.
The following table depicts the hourly averages (mean) of rate data by day, the average (mean) of hourly averages and the population standard deviation of the hourly averages for the same day of the week, same hour:


![Test Image 7](https://github.com/pik1989/3Sigma-Based-Anomaly-Detection/blob/master/images/Chart.png)


Assume that data is polled at 15-minute interval.

The current utilization is greater than/less than one standard deviation can be considered as minor anomalies.

**MINOR ANOMALY = (current value > mean+ 1xSD) || (current value < mean- 1xSD)**

The current utilization is greater than/less than two standard deviation can be considered as major anomalies.

**MAJOR ANOMALY = (current value > mean+ 2xSD) || (current value < mean- 2xSD)**

The current utilization is greater than/less than three standard deviation can be considered as critical anomalies.

**CRITICAL ANOMALY = (current value > mean+ 3xSD) || (current value < mean- 3xSD)**
