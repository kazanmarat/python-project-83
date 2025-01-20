### Hexlet tests and linter status:
[![Actions Status](https://github.com/kazanmarat/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kazanmarat/python-project-83/actions)


### Codeclimate test:
[![Maintainability](https://api.codeclimate.com/v1/badges/ecb37f8e1d27b19bb825/maintainability)](https://codeclimate.com/github/kazanmarat/python-project-83/maintainability)


This web application takes a website URL similar to PageSpeed Insights (https://pagespeed.web.dev/) and checks its validity. It does not measure performance, but outputs the contents of the header (h1), title, and description of the page.
To run on a local computer, type gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app and open your browser to http://0.0.0.0:8000
The Page Analyzer demo site (https://python-project-83-sl6j.onrender.com/) has been running for less than a month due to a database outage.
