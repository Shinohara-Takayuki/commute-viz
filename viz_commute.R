library(ggplot2)
library(dplyr)
library(reshape2)

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
    geom_line()


# summarize by time
by.time <- commutes.melt %>% 
    mutate(departure = substr(departure, 12, 19)) %>%
        group_by(departure) %>%
            summarise(mean=mean(trip_length_min), 
                med=median(trip_length_min), count=n())

# get time diff
a <- strptime(by.time$departure, "%H:%M:%S") - strptime("00:00:00", "%H:%M:%S")
# convert to hours, subtract 8 hours to get to EST, add 24 and mod 24 to get wrap-around
a <- (24 + ((as.numeric(a) / 60) - 8)) %% 24
by.time$departure <- a
ggplot(by.time, aes(x=departure, y=mean)) + geom_point()