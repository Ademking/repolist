import argparse
import requests
import sys
from colorama import Fore, Style


class RepoList:
    def __init__(self):
        self.repo_content = []
        self.args = None
        self.error_messages = {
            404: "Repository not found, check the URL and try again, or check if the repository is private to use the --token option.",
            422: "Too many requests, try again later",
            403: "API rate limit exceeded, try again later or use a proxy with the --proxy option"
        }
        self.header = """
    ____                   __    _      __ 
   / __ \___  ____  ____  / /   (_)____/ /_
  / /_/ / _ \/ __ \/ __ \/ /   / / ___/ __/
 / _, _/  __/ /_/ / /_/ / /___/ (__  ) /_  
/_/ |_|\___/ .___/\____/_____/_/____/\__/  
          /_/ v0.1.0                              
"""
        self.example_text = """
Examples:
  repolist -u "https://github.com/PrestaShop/PrestaShop"
  repolist -u "https://github.com/WordPress/WordPress" -o "wp_wordlist.txt"
  repolist -u "https://github.com/laravel/laravel" --files
  repolist -u "https://github.com/username/private_repo" --token "your_token_here"
        """
        self.description = "Generate wordlists from Github repositories"

    def init_cli(self, arr_args=None):
        parser = argparse.ArgumentParser(description="{}\n{}".format(self.header, self.description),
                                         formatter_class=argparse.RawDescriptionHelpFormatter, usage=argparse.SUPPRESS, epilog=self.example_text)
        # add help messages
        parser._optionals.title = "Arguments"
        parser.add_argument(
            "-u", "--url", help="Github repository URL (required)")
        parser.add_argument("-o", "--output", help="Output file (optional)")
        parser.add_argument(
            "-b", "--branch", help="Use a specific branch (optional)")
        parser.add_argument("-t", "--token", help="Github token (optional)")
        parser.add_argument(
            "-p", "--prefix", help="Prefix (optional)")
        parser.add_argument(
            "-s", "--suffix", help="Suffix (optional)")
        parser.add_argument(
            "-f", "--files", help="Get only files (optional)", action="store_true")
        parser.add_argument("-d", "--directories",
                            help="Get only directories (optional)", action="store_true")
        parser.add_argument("-v", "--verbose",
                            help="Verbose mode (optional)", action="store_true")
        parser.add_argument("--proxy", help="Proxy (optional)")

        # if no arguments are passed, use sys.argv
        if not arr_args or len(arr_args) == 0:
            args = parser.parse_args()
        else:
            args = parser.parse_args(arr_args)
        self.args = args
        if not args.url:
            parser.print_help()
            sys.exit(1)

    def _get_repo_name_owner(self, url):
        """Get the repository name and owner from a URL"""
        # check if the URL is valid
        if not url.startswith("https://github.com/"):
            self._log_error(
                msg="Invalid URL. Please use a valid Github repository URL. Example: https://github.com/user/repo")
            exit(1)
        url = url.replace("https://github.com", "")
        username, repo = url.split("/")[1:]
        return username, repo

    def _make_request(self, url):
        """Make a request to Github API"""
        try:
            r = requests.get(
                url, headers=self._get_request_headers(), proxies=self._get_proxy())
            if r.status_code == 200:
                return r
            else:
                self._log_error(msg="{}: {}".format(
                    r.status_code, r.text), type=r.status_code)
                exit(1)
        except Exception as e:
            self._log_error(msg="Error: {}".format(e))
            exit(1)

    def _get_branch(self, username, repo):
        """Use the default branch if no branch is specified"""
        if self.args.branch:
            return self.args.branch
        r = self._make_request(
            "https://api.github.com/repos/{}/{}".format(username, repo))
        if r.status_code == 200:
            return r.json()["default_branch"]
        else:
            self._log_error(msg="{}: {}".format(
                r.status_code, r.text), type=r.status_code)
            exit(1)

    def _log(self, msg):
        """Print only if verbose is enabled"""
        if self.args.verbose:
            print(Fore.BLUE + Style.BRIGHT +
                  "[INFO] {}".format(msg) + Style.RESET_ALL)

    def _log_error(self, msg="", type=None):
        if type in self.error_messages.keys():
            msg = self.error_messages[type]
        else:
            msg = "{}".format(msg)
        print(Fore.RED + Style.BRIGHT +
              "[ERROR] {}".format(msg) + Style.RESET_ALL)

    def _print_only_files(self):
        """Print only files"""
        for file in self._get_only_files():
            print(self.format_text(
                file["path"], self.args.prefix, self.args.suffix))

    def _print_only_directories(self):
        """Print only directories"""
        for directory in self._get_only_directories():
            print(self.format_text(
                directory["path"], self.args.prefix, self.args.suffix))

    def format_text(self, text, prefix, suffix):
        """Helper function to format text"""
        result = "".join([
            str(prefix) if prefix is not None else "",
            str(text) if text is not None else "",
            str(suffix) if suffix is not None else ""
        ])
        return result

    def _print_all(self):
        """Print all files and directories"""
        for file in self.repo_content:
            print(self.format_text(file["path"],
                  self.args.prefix, self.args.suffix))

    def _get_only_files(self):
        """Return only file list"""
        files = [file for file in self.repo_content if file["type"] == "blob"]
        return files

    def _get_only_directories(self):
        """Return only directory list"""
        directories = [
            directory for directory in self.repo_content if directory["type"] == "tree"]
        return directories

    def _get_request_headers(self):
        if self.args.token:
            headers = {'Authorization': 'Bearer {}'.format(
                self.args.token), 'Accept': 'application/vnd.github+json'}
        else:
            headers = {'Accept': 'application/vnd.github+json'}
        return headers

    def _get_proxy(self):
        if self.args.proxy:
            return {"http": self.args.proxy, "https": self.args.proxy}
        else:
            return None

    def _get_files(self, username="", repo="", branch="main"):
        """
        Get files and directories from a repository (recursive)
        https://docs.github.com/en/rest/reference/git#trees
        """
        url = "https://api.github.com/repos/{}/{}/git/trees/{}?recursive=1".format(
            username, repo, branch)
        r = self._make_request(url)
        # add headers if token is specified
        if r.status_code == 200:
            for file in r.json()["tree"]:
                self.repo_content.append({
                    "path": file["path"],
                    "type": file["type"]
                })
        else:
            self._log_error(type=r.status_code, msg=r.text)
            exit(1)

    def run(self):
        self._log("Starting gitWordlist...")
        self._log("Repository URL: {}".format(self.args.url))
        self._log("Output file: {}".format(self.args.output))
        username, repo = self._get_repo_name_owner(self.args.url)
        self._log("Username: {}".format(username))
        self._log("Repository: {}".format(repo))
        branch = self._get_branch(username, repo)
        self._log("Branch: {}".format(branch))
        self._get_files(username=username, repo=repo, branch=branch)
        self._log("Number of lines: {}".format(len(self.repo_content)))
        self._log("Number of files: {}".format(len(self._get_only_files())))
        self._log("Number of directories: {}".format(
            len(self._get_only_directories())))
        if self.args.output:  # save to file
            with open(self.args.output, "w") as f:
                if self.args.files:  # save only files
                    for file in self._get_only_files():
                        f.write(
                            self.format_text(file["path"], self.args.prefix, self.args.suffix) + "\n")
                elif self.args.directories:  # save only directories
                    for directory in self._get_only_directories():
                        f.write(
                            self.format_text(directory["path"], self.args.prefix, self.args.suffix) + "\n")
                else:  # save all
                    for file in self.repo_content:
                        f.write(
                            self.format_text(file["path"], self.args.prefix, self.args.suffix) + "\n")
            self._log("Output saved to {}".format(self.args.output))
        else:
            if self.args.files:  # print only files
                self._print_only_files()
            elif self.args.directories:  # print only directories
                self._print_only_directories()
            else:  # print all
                self._print_all()
