import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / ref, "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "w") as f:
        f.write("ref:{ref}\n")
    update_ref(gitdir, ref, name)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    with open(gitdir / refname, "r") as f:
        ref = f.read().split()[1]
    if (gitdir / ref).exist():
        with open(gitdir / ref, "r") as f:
            return f.read()
    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    resolve_head = ref_resolve(gitdir, "HEAD")
    return resolve_head


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "r") as f:
        if "ref" not in f.read():
            return True
        else:
            return False


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "r") as f:
        return f.read().split()[1]
