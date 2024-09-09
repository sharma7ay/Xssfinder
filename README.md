# XSS Detection Tool

## Overview

This tool is designed to detect Cross-Site Scripting (XSS) vulnerabilities in web applications. It works by testing specified URLs with various XSS payloads.

## Key Differences

- **Alert Detection**: This tool focuses on finding URLs that generate alert boxes as a result of XSS payloads. Other tools may only report potential vulnerabilities without indicating whether an alert was triggered.
- **Ease of Use**: With a simple command-line interface, users can easily specify URLs and payloads to test.

## Requirements

- **Python**: Version 3.6 or higher
- **Google Chrome**: The latest version of the Chrome browser must be installed on your machine.

### Python Packages

Then, run the following command to install the dependencies:

```bash
pip install -r requirements.txt
```

## Note

This XSS Detection Tool works in conjunction with the Gxss tool. Ensure that the Gxss tool is run first to set up the necessary conditions for testing.
