# Page analyzer
The "Page_analyzer" application analyzes web pages for their SEO suitability similar to [PageSpeed ​​Insights](https://pagespeed.web.dev/). The project does not measure performance, but provides users with the ability to check the availability of websites and analyze elements such as H1 tags, headers, and site descriptions. Implemented in Python, Flask, and PostgreSQL. The results of the checks are stored in the database.
 
## Installation
### Prerequisites
- Python version 3.10 or higher
- Flask version 3.0.3 or higher
- PostgreSQL version 16.6 or higher
- Poetry version 1.8.3 or higher (optional)
 
### Download
    git clone https://github.com/kazanmarat/python-project-83.git
### Set configuration
In the project directory, rename the `.env_example` file to `.env`. Then enter your data for the following variables:
- SECRET_KEY: secret key for the application.
- DATABASE_URL: to connect to the PostgreSQL database.

To build the application and create database tables, use the bash script `build.sh`. \
`Makefile` simplifies the installation and startup process with the following commands:
#### Starting a local development server
    make dev
#### Starting a production (working) server
    make start

### How to use the page analyzer:
On the main page, enter the site address and click "Проверить" to open the page for checking. \
If the address format is incorrect, the site will return an error. On the page for checking, click the "Запустить проверку" button and wait for the result. \
If you click "Сайты" in the navigation, a list of verified sites will appear.

### Hexlet test and linter status:
[![Actions Status](https://github.com/kazanmarat/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kazanmarat/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/ecb37f8e1d27b19bb825/maintainability)](https://codeclimate.com/github/kazanmarat/python-project-83/maintainability)
