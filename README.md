# RepoList - Generate Wordlists from GitHub Repositories

![Build](https://img.shields.io/badge/Built%20with-Python-Blue)
[![PyPI version](https://badge.fury.io/py/repolist.svg)](https://badge.fury.io/py/repolist)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![image](https://github.com/Ademking/repolist/assets/12462188/9b72b1ee-6cf8-4ff5-9bc0-c994ecb9ee03)

Repolist is a command-line interface (CLI) tool designed to generate wordlists from GitHub repositories. It simplifies the process of extracting files and directories from GitHub repos, enabling the creation of custom wordlists for penetration testing and bug bounty programs.

> You can read more about it in this blog: [https://ademkouki.tech/posts/repolist](https://ademkouki.tech/posts/repolist/)


Table of Contents
------------
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Options](#options)
* [Why RepoList?](#why-repolist)
* [Rate Limiting](#rate-limiting)
* [Contributing](#contributing)
* [Disclaimer](#disclaimer)
* [License](#license)
* [Author](#author)


## Features

- Wordlist Generation: Easily create wordlists from GitHub repositories. Choose between generating a wordlist of files, directories, or both.
- Customization: Add custom prefixes and suffixes to the generated wordlists, such as appending .php to each word.
- Support for Private Repositories: Access and generate wordlists from both private and public repositories by providing a GitHub token using the `-t` option.
- Branch Selection: Specify a different branch using the `-b` option.
- Proxy Support: Utilize a proxy by using the `-p` option.

## Installation

```bash
pip3 install repolist
```

## Usage

Generate a wordlist by providing the URL of the GitHub repository:

```bash
repolist -u https://gihtub.com/user/repo
```
![demo](https://github.com/Ademking/repolist/assets/12462188/f94ade42-06fd-4eb9-a846-65519f1f651b)



## Options

```
Arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Github repository URL (required)
  -o OUTPUT, --output OUTPUT
                        Output file (optional)
  -b BRANCH, --branch BRANCH
                        Use a specific branch (optional)
  -t TOKEN, --token TOKEN
                        Github token (optional)
  -p PREFIX, --prefix PREFIX
                        Prefix (optional)
  -s SUFFIX, --suffix SUFFIX
                        Suffix (optional)
  -f, --files           Get only files (optional)
  -d, --directories     Get only directories (optional)
  -v, --verbose         Verbose mode (optional)
  --proxy PROXY         Proxy (optional)
```

## Why RepoList?

I created this tool to simplify the process of generating wordlists from GitHub repositories. I found myself cloning repositories and looking for files and directories to add to my wordlists. This tool automates that process and allows you to generate wordlists from GitHub repositories with a single command. 
Using RepoList with tools like [ffuf](https://github.com/ffuf/ffuf) and [gobuster](https://github.com/OJ/gobuster) can be very useful for penetration testing and bug bounty programs.

Example using `ffuf`:

```bash
repolist -u "https://github.com/WordPress/WordPress" | ffuf -u "http://example.com/FUZZ" -w -
```

## Rate Limiting

GitHub has a rate limit. To avoid this, you can provide a GitHub token using the `-t` option. This will increase the rate limit. You can create a GitHub token by following [these instructions](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

You can also use a proxy by using the `-p` option.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer
This tool is intended to be used for security testing purposes only and should not be used for any illegal purposes.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
[Adem Kouki](https://github.com/Ademking)


