import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    environ = os.environ.get("GIT_DIR", default=".pyvcs")
    workdir = pathlib.Path(workdir)

    while str(workdir.absolute()) != "\\":
        if (workdir / environ).exists():
            return workdir / environ
        workdir = workdir.parent

    if (workdir / environ).exists():
        return workdir / environ
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    environ = os.environ.get("GIT_DIR", default=".pyvcs")
    
    workdir = pathlib.Path(workdir)
    git_dir = workdir / environ

    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")

    if not git_dir.exists():
        git_dir.mkdir()

        refs = git_dir / "refs" 
        refs.mkdir() 
        heads = refs / "heads"
        heads.mkdir()
        tags = refs / "tags"
        tags.mkdir()

        objects = git_dir / "objects"
        objects.mkdir()

        with open(git_dir / "HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")

        with open(git_dir / "config", "w") as f:
            f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")

        with open(git_dir / "description", "w") as f:
            f.write("Unnamed pyvcs repository.\n")

    return git_dir

if __name__ == "__main__":
    workdir = pathlib.Path(".")
    gitdir = repo_create(".")
    print(gitdir)