# pavise

## Introduction

**Pavise** (a type of shield) is a service that, given a URL, returns whether a given URL is a malware site or not.

The general use case for Pavise is for a proxy. The proxy connects to Pavise, passes in the URL, and gets a notification as to whether that URL is known to contain malware.

## Requirements

The goal is to make this fairly low on requirements. A machine, VM, or container with Python 3 is required.

## Installation

1. Create a virtual environment: `python -m venv venv`
2. Start the virtual environment: `source venv/bin/activate`
3. Install the Python packages: `pip install -r requirements.txt`

## Further Documentation

The `docs/` directory contains information about architecture, possible extensions, and so forth.

