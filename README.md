# SEO Spam Finder Pro V2

A GUI-based SEO spam investigation tool for identifying indexed spam pages, checking URL activity, SSL security, redirects, WHOIS information, and security headers.

## Features

* Search URLs using site:domain keyword queries
* Active URL verification
* Redirect detection
* SSL validation
* WHOIS analysis
* Security header analysis
* CSV export
* Copy selected URLs
* Open URLs in browser
* Multi-threaded scanning
* Sortable results table

## Requirements

* Python 3.10 or newer
* Internet connection

## Installation

### Clone Repository

```bash
git clone https://github.com/anishry/seo_spam_finder.git
cd seo_spam_finder
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python SEO_Spam_Finder_Pro_V2.py
```

## Windows Installation

### Install Python

Download Python from:

https://www.python.org/downloads/

Ensure "Add Python to PATH" is checked.

### Install Dependencies

Open Command Prompt:

```cmd
pip install -r requirements.txt
```

### Launch

```cmd
python SEO_Spam_Finder_Pro_V2.py
```

## Usage

1. Enter domain name.
2. Enter keywords separated by commas.
3. Click Search.
4. View active URLs.
5. Sort results by clicking column headers.
6. Export results to CSV.

## Example

Domain:

```text
example.com
```

Keywords:

```text
rummy,casino,poker,betting
```

## Output

The tool returns:

* Active URLs
* HTTP Status
* Redirect Information
* SSL Status
* Security Header Score

## Disclaimer

This tool is intended for authorized security research, SEO auditing, and website administration purposes only.
