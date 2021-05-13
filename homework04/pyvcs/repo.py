import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    environ = os.environ.get("GIT_DIR")
    workdir = pathlib.Path(workdir)

    while str(workdir.absolut()) != "/":
        if (workdir / environ).exists():
            return workdir / environ
        workdir = workdir.parent
    if (workdir / environ).exist():
        return workdir / environ
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # PUT YOUR CODE HERE
    environ = os.environ.get("GIT_DIR")
    workdir = pathlib.Path(workdir)
    gitdir = workdir / environ

    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")

    if not gitdir.exist():
        gitdir.mkdir()

        refs = gitdir / "refs"
        refs.mkdir()
        heads = refs / "heads"
        heads.mkdir()
        tags = refs / "tags"
        tags.mkdir()
        objects = gitdir / "objects"
        objects.mkdir()

        with open(gitdir / "HEAD", "w") as f:
            f.write("ref : refs/heads/master\n")
        with open(gitdir / "config", "w") as f:
            f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
        with open(gitdir / "description", "w") as f:
            f.write("Unnamed pyvcs repository.\n")

    return gitdir



if __name__ == "__main__":
    workdir = pathlib.Path(".")
    gitdir = repo_create(".")
    print(gitdir) # "./.git"