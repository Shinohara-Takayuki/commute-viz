# commute-viz
Visualization for commute times obtained from Heroku scheduler hitting Bing Maps every 10 min for this summer

In trying to figure out my commuting schedule for my internship at Google this summer, I set up a Heroku app with 0 web dynos and a 10-min granularity scheduler to hit the Bing Maps API and find out the commute time both to and from work (Google Distance Matrix API only gives times in traffic to Business customers who paid for their license).

I've included some visualization to find the optimal time to leave for and from work.
