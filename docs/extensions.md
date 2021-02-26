# Extensions ("Part 2")

## Preliminary Estimates

Some of the below questions involve estimates, especially of size.

I make the following assumptions:

1. I am assuming a typical maximum size of URLs of 2000 UTF-8 characters. (There is no official upper limit to URLs; that said, some checking around suggests that some web browsers won't handle URLs above 2000 characters, and the 2000 limit permits URLs that contain executable code.)
2. I am assuming that UTF-8 characters two bytes. (That is, there are relatively few emoji addresses, and the majority of URLs use characters in the first 2,048 code points, expressible in two bytes.)
3. Timestamps are 8 bytes each. (This seems to be typical across databases.)
4. SHA-256 hashes are 64 characters. (We could convert these into 32-byte numbers, but storing them as strings in the database would be more convenient.)
5. There are on average 5,000 new unique URLs per day added.

In that case, we have approximately 10 million characters to add to the database each day. If we use 2-byte UTF-8, that is around 20MB of URL data added to the database daily.

## Thought exercises

Here are some thoughts I have had about the next steps:

1. "The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system?"

My current design involves using sqlite3, as it has built-in support in Python and has no external dependencies. The data model here is fairly simple at present, with a few fields and tables, so it should be adaptable with a bit of work to different database systems. While it can grow infinitely, very little is kept in memory on the machine, and the requests themselves do not involve much state that needs to be maintained, in memory or otherwise, beyond the length of the request.

(**NB** if we were to store it in an in-memory cache, we could hold around 10 million URLs and their associated hashes in around 10GB of memory, possibly less depending on the data structures at hand.)

2. "Assume that the number of requests will exceed the capacity of a single system. Describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe."

The first pass of a solution would be to load balance requests between containers. As the majority of operations will be GETs, and needing comparatively little data, this can be done without requiring much communication from the Pavise servers, except for some nominal heartbeat functions.

What we need to ensure, in that case, is that as we increase the number of copies of the application running, we do not overload the database. Similarly, we will need to distribute the database, possibly using a cluster system like Galera for MySQL/MariaDB, or ClusterControl for PostgreSQL.

Now, if we need to distribute this to additional regions, we could replicate the same process in each data center. (See #7 for deployment strategies.) The problem will be ensure that the data are identical across regions. We would need to make sure that our database sync strategies (which depend largely on the DBMS we are using) are up to the task. In our favor, the data changes are not overly large and continuous, and the hashes are not tied to specific ID numbering, so concerns about partition robustness and consistency are a little lower than other applications.

3. "What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes."

Going with my preliminary estimates and assumptions from above, at 5,000 new URLs per day, that would be 20MB per day in UTF-8 characters. Creation and deletion modification timestamps add 16 bytes per entry, or another 80,000 bytes in total. Add in 64 bytes each for SHA-256 hashes, which is another 320,000 bytes. Adding in some overhead, we can say that we add 30MB per day to the database, or 11GB per year.

If we spread the 5,000 out through a 24-hour period, at 10-minute intervals, we would have 5000/144, or approximately 35 URLs at each update. Batching these into a POST where the URLs are in the body, and the database gets updated accordingly, should be fairly straightforward.

Of course, as it currently stands, Pavise is an unauthenticated system. Currently, anyone can POST URLs and update the database that way. If we are lucky, we can use a pre-existing SSO system with an identity provider to generate a JWT or other token, and use said token as a way of authenticating with Pavise. This will make the architecture somewhat more complicated than this initial proof of concept.

More complicated is ensure that these changes are distributed to all regions, including internationally.

We now need to consider what happens when we make changes in one region. These changes must propagate throughout the other regions. Given the size of the data, this should be a fairly fast process. At around 30MB of data per day, the impact on traffic and speed of sycnchronization is fairly miminal.

One of the advantages of using a SHA-256 hash is that it will remain the same for the same URLs, so it is robust to how the information is ordered in the database.

4. "You're woken up at 3am, what are some of the things you'll look for?"

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

This would require some changes to the application as currently designed. For example, as of now I do not have hooks into services for metrics, logging, and alerts. Ensuring that there are keep-alives is another necessary component.

6. "What are some considerations for the lifecycle of the app?"

* Hooks for tracing and performance montitoring would be welcome, especially as the service was used more.
* Determining what the service-level indicators are, which will inform our service-level objectives, and influence the SLAs we can reasonably offer, directly to the proxy team, and indirectly to customers.
* Coming up with clear, consistent policies of when URLs get added and removed, and a process for appealing incorrectly filed URLs.
* Devising policies for API changes, with an eye on making any changes not impact API signatures and results whenever possible.
* Improving the testing strategy: more tests, make it easier to build and improve existing tests.
* Regular evaluation of user experience; even though they do not directly interact with the app, problems in the app can severely cause problems in their experience.

7. "You need to deploy a new version of the application. What do you do?"

Assuming a fix or a feature has been written and locally tested:
* Make a PR, and have a code review.
* Ensure that there are feature flags in place that work, so that if the new feature or fix fails, we can rapidly get to the previous version without another rollout.
* If the changes require modifications to the API, let the maintainers of the proxy service have input, and give them ample time to make changes on their end.
* If it passes the code review, merge it into `develop`.
* Make sure that the suite of tests pass.

Next is the deployment stage. Since this service is comparatively small, and not directly user-facing, deploying changes that do not break the API can be rolled out using, for example, rolling deployments in Kubernetes. As for getting the changes out to multiple clusters, that will likely depend upon what our overall multi-cluster management strategy would be.

Deployments where the API breaks existing code are somewhat more complicated, as we need to take into account the development processes of the maintainers of the proxy. Again, we can use feature flags and API versioning to our advantage, as we can turn on those features in the new version when everyone is ready.
