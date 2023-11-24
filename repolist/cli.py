from .repolist import RepoList

def main():
    repolist = RepoList()
    repolist.init_cli()
    repolist.run()