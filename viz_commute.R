library(ggplot2)
library(dplyr)
library(reshape2)
library(scales)

# below line updated to reflect latest .csv file downloaded
commutes <- read.csv("ngihxhngzmtcwjhalspmtdfikchs.csv",
    stringsAsFactors=FALSE)

# over all days that data recorded
commutes <- commutes %>% 
    select(-to_work_dist_miles, -from_work_dist_miles) %>%
        mutate(req_time=substr(req_time, 1, 19))
colnames(commutes) <- c("departure", "home_to_work", "work_to_home")
commutes.melt <- melt(commutes, id="departure")
colnames(commutes.melt)[2:3] <- c("direction", "trip_length_min")
commutes.melt$departure <- strptime(commutes.melt$departure, 
    "%Y-%m-%d %H:%M:%S", tz="EST") - as.difftime(8, unit="hours")
# -8 to convert to LA time

ggplot(commutes.melt, aes(x=departure, y=trip_length_min, colour=direction)) + 
    geom_line() + 
        scale_x_datetime(labels = date_format("%m/%d %H"), breaks = "2 hour")


#### summarize by time (round to nearest minute)

#### to work
# get time diff and then round to nearest 10 minute, convert to hours
a <- as.numeric(strptime(substr(
    commutes.melt$departure, 12, 16), "%H:%M") - strptime("00:00:00", "%H:%M:%S"))

by.time <- commutes.melt %>% 
    mutate(departure = round(a, -1) / 60) %>%
        group_by(departure, direction) %>%
            summarise(mean=mean(trip_length_min), 
                med=median(trip_length_min), count=n())

ggplot(by.time, aes(x=departure, y=mean)) + 
    geom_line(aes(colour=direction)) + 
        scale_x_continuous(breaks=seq(0, 24, 1))