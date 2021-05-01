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
    return workdir / environ



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
    with open(git_dir / "config", "w") as f:
        f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    with open(git_dir / "description", "w") as f:
        f.write("Unnamed pyvcs repository.\n")

    return gitdir

