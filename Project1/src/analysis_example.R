# Title     : Example analysis
# Created by: Gabriel M P Perez
# Created on: 19/05/2021
library(dplyr)

# Reading data
filepath <- 'MPEForecastVerification/Project1/data/processed/merged_step_24hrs.txt'
df <- read.csv(filepath)

# Calculating ECMWF and UKMet mean squared errors
prevs_ecmwf <- df %>% select(contains('ECMWF'))
prevs_ukmet <- df %>% select(contains('UKMet'))
err_ecmwf <- prevs_ecmwf - df$OBS
err_ukmet <- prevs_ukmet - df$OBS
colMeans(sqrt(err_ecmwf^2))
colMeans(sqrt(err_ukmet^2))

