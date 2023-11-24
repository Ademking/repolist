# RepoList

Repolist is a command-line interface (CLI) tool designed to generate wordlists from GitHub repositories. It simplifies the process of extracting files and directories from GitHub repos, enabling the creation of custom wordlists for penetration testing and bug bounty programs.

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

For more options and configurations, use the -h flag for help.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer
This tool is intended to be used for security testing purposes only and should not be used for any illegal purposes.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
[Adem Kouki](https://github.com/Ademking)


