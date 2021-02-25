# pavise

## Introduction

**Pavise** (a type of shield) is a service that, given a URL, returns whether a given URL is a malware site or not.

The general use case for Pavise is for a proxy. The proxy connects to Pavise, passes in the URL, and gets a notification as to whether that URL is known to contain malware.

## Requirements

The goal is to make this fairly low on requirements. At the moment, the following are required:
* Python 3, with a virtual environment;
* A Docker installation.

## Installation

To run locally:
1. Create a virtual environment: `python -m venv venv`
2. Start the virtual environment: `source venv/bin/activate`
3. Install the Python packages: `pip install -r requirements/development.txt`
4. To run tests: `./manage.py test`
5. To deploy in docker: `./manage.py compose up`

## Further Documentation

The `docs/` directory contains information about architecture, possible extensions, and so forth.

