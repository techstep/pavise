# Pavise Architecture

Pavise is a RESTful service that, given a URL, returns whether that URL is known to have malware.

## General Design

The current assumption is that either a URL contains malware, or not. It is a binary determination, without a likelihood score attached to it.

Another assumption is that the number of URLs containing malware is a fraction of all possible URLs.

The design does not store the specific list of URLs; rather, it stores SHA-256 hashes. If the hashed 

We go through a normalization process:

1. We change URLs into all lower-case.

One consequence of this is that this procedure is susceptible to false positives. As query strings and, say, base-64 strings are case-sensitive, the difference between one that actually contains malware and one that does it can hinge upon capitalization. By collapsing case, a URL would be marked as having malware regardless of capitalization.)

2. Query strings are sanitized using URLencode.

3. This string becomes the basis of a SHA-256 hash.

A SHA-256 hash takes 64 bytes.

4. While SHA-256 collisions _can_ happen theoretically, the probability is small

## Routes

Currently, we have one route:
`GET /urlinfo/1/[hostname_and_port]/[original_path_and_query_string]`

The states are:

200 - The URL has been found in the database;
404 - The URL cannot be found in the database;
503 - 
