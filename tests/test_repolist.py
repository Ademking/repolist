from repolist.repolist import RepoList
import pytest
# add arguments

@pytest.mark.filterwarnings
def test_repolist_cli(capsys):
    """
    Test if the program runs with the correct arguments
    """
    args = ["-u", "https://github.com/WordPress/WordPress"]
    repolist = RepoList()
    repolist.init_cli(args)
    repolist.run()
    captured = capsys.readouterr()
    assert "wp-login.php" in captured.out

@pytest.mark.filterwarnings
def test_repolist_cli_no_args():
    """
    Test if the program exits when no arguments are passed
    """
    with pytest.raises(SystemExit) as excinfo:
        repolist = RepoList()
        repolist.init_cli()
        repolist.run()
    assert excinfo.value.code == 1

@pytest.mark.filterwarnings
def test_404(capsys):
    """
    Test if the program exits when the repository is not found
    """
    with pytest.raises(SystemExit) as excinfo:
        args = ["-u", "https://github.com/123456789/123456789"]
        repolist = RepoList()
        repolist.init_cli(args)
        repolist.run()
    captured = capsys.readouterr()
    assert "Repository not found" in captured.out
    assert excinfo.value.code == 1
    
@pytest.mark.filterwarnings
def test_wrong_url(capsys):
    """
    Test if the program exits when the URL is invalid
    """
    with pytest.raises(SystemExit) as excinfo:
        args = ["-u", "https://example.com"]
        repolist = RepoList()
        repolist.init_cli(args)
        repolist.run()
    captured = capsys.readouterr()
    assert "Invalid URL" in captured.out
    assert excinfo.value.code == 1

@pytest.mark.filterwarnings
def test_prefix_suffix(capsys):
    """
    Test if the program runs with the correct arguments
    """
    args = ["-u", "https://github.com/WordPress/WordPress", "-p", "CUSTOM_PERFIX", "-s", "CUSTOM_SUFFIX"]
    repolist = RepoList()
    repolist.init_cli(args)
    repolist.run()
    captured = capsys.readouterr()
    assert "CUSTOM_PERFIXwp-login.phpCUSTOM_SUFFIX" in captured.out