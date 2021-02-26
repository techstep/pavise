# Pavise Architecture

Pavise is a RESTful service that, given a URL, returns whether that URL is known to have malware. There are also routes to add and delete entries from the list.

## General Design

I make several assumptions in the design:

1. A URL contains malware, or not. I am not looking in terms of a likelihood or propensity score; rather, I assume that the person or entity that adds in the URLs has the knowledge or belief that sites they are adding in contain malware.

2. If a URL is not in the list, a user is permitted to access it. That is, the database is a restricted list, not a permitted list. (Another assumption embedded in this is that the number of malware-containing sites, if not known, is at least comparatively small to the number that do not.)

3. The maintainers of the proxy service are able to send the appropriate requests and parse the return data as in the specifications provided.

4. The proxy is retaining the actual URL, as the scheme and authority information have been removed for this. Morever, the proxy is able to cache results, so it need not make a request to Pavise each time a user wants to make a request to a URL. (A future extension could offer a time-to-live (TTL) metric for the requests, so that the proxy has a guaranteed caching time.)

5. At the outset, there is no authentication model, but this is something that could be added in (as noted in the [extensions document](extensions.md).)

6. A user will typically be checking one URL at a time. (That is, they're entering a URL into a web browser.) Automated processes are subject to the same proxies, but for the moment these will be handled one at a time as well.

The general process goes as follows, and much of it is the same for both adding and checking URLs.

1. We change the paths into all lower-case. One consequence of this is that this procedure is susceptible to false positives. As query strings and, say, base-64 strings are case-sensitive, the difference between one that actually contains malware and one that does it can hinge upon capitalization. By collapsing case, a URL would be marked as having malware regardless of capitalization.)

2. If a port is not included, we default to port 80. (There is an assumption here that there is a lower change of malware on HTTPS servers.)

3. Query strings are sanitized using URLencode.

4. This string becomes the basis of a SHA-256 hash.

For searches, I check if both the normalized URL is in there, and the hashes match the entry in the database. If there is at least _one_ match among the URLs and the hashes, then that is considered a malware site. If neither matches, then there is not evidence of malware at the moment.

For adding entries, the route determines if the URL has been previously added, and returns an error if there are matches.

For removing entries, the URL and the hash must both match for a deletion to be successful.

## Routes

Currently, we have one route:
`GET /urlinfo/1/[hostname_and_port]/[original_path_and_query_string]`

This returns a JSON payload in the form of:

```
{
    "url": "www.quiescentlyfrozenmalware.org/test?variable=stuff&variable2=things",
    "sha256_hash": "a2e461802f5976b17b968dac38d7734742d3cb71288023a49a0c7d651e3940e6",
    "is_malware: "True"
}
```

Where:
* `url` is the unencoded path (the normalized, encoded one is stored in the database);
* `sha256_hash` is the generated hash;
* `is_malware` is `true` if either the URL and the hash are in the database, and `false` otherwise.
