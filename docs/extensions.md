# Extensions ("Part 2")

Here are some thoughts I have had about the next steps:

1. "The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system?"

My current design involves using an in-memory database. With very little change, we can use a small database, like sqlite3. The data model here is fairly simple at present, with a few fields and tables. 

2. "Assume that the number of requests will exceed the capacity of a single system. Describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe."

The first pass of a solution would be to load balance requests between containers. As the majority of operations will be GETs, and needing comparatively little data, this can be done without requiring much communication from the Pavise servers, except for some nominal heartbeat functions.

What we need to ensure, in that case, is that as we increase the number of copies of the application running, we do not overload the database. Similarly, we will need to distribute the database, possibly using a cluster system like Galera for MySQL/MariaDB, or ClusterControl for PostgreSQL.

3. "What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes."

FOr ease of calculation, let's say there are 10,000 additional URLs per day, and each URL has 100 characters on average. This means, we have an additional 1,000,000 characters to add to the database per day. With 4-bit UTF-16 (if we're being generous), that's about 4MB net of overhead. Add in timestamps for modification and creation, which are on average 8 bytes, depending on the database, and that's another 160,000 bytes. Even with overhead, the updates have the approximate impact of adding in a decent-sized MP3 each day.

If we spread the 10,000 out through a 24-hour period, at 10-minute intervals, we would have 10,000/144, or approximately 70 URLs at each update. Batching these into a POST where the URLs are in the body, and the database gets updated accordingly, should be fairly straightforward.

Of course, as it currently stands, Pavise is an unauthenticated system. Currently, anyone can POST URLs and update the database that way. If we are lucky, we can use a pre-existing SSO system with an identity provider to generate a JWT or other token, and use said token as a way of authenticating with Pavise. This will make the architecture somewhat more complicated than this initial proof of concept.

More complicated is ensure that these changes are distributed to all regions, including internationally.

We now need to consider what happens when we make changes in one region. These changes must propagate throughout the other 

4. "You're woken up at 3am, what are some of the thigns you'll look for?"

I would look at what reports are coming in:
* On a first pass: what are the symptoms? 
    - Are users complaining about slow access?
    - Are updates failing to process?
    - Are customers unable to reach any sites?
    - Are sites they previously _could_ go to now blocked, or vice versa?

For example, if access is slow, this could mean that the proxy is successfully sending the request to Pavise, and getting the response, but Pavise is slow on returning data from the database. Likewise, if there are sites that they could get to but not anymore, that could be due to a database update, erroneous or otherwise.

* Are there errors on the proxy server logs? If so, what kinds?
* What do the logs look like on the servers or containers where Pavise is running? Or the database?
* Are there time-series metrics that can shed some light on when things started to happen?
* Are the Pavise servers reachable?
* Where are the issues happening? Is it global, or localized to a specific region? 

5. "Does that change anything you've done in the app?"

This would require some changes to the application as currently designed. For example, as of now I do not have hooks into services for metrics, logging, and alerts.

6. "What are some considerations for the lifecycle of the app?"

7. "You need to deploy a new version of the application. What do you do?"

Assuming a fix or a feature has been written and locally tested
