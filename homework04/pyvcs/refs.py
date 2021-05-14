import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with open(gitdir / ref, "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with open(gitdir / "HEAD", "w") as f:
        f.write("ref: {ref}\n")
    update_ref(gitdir, ref, name)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    with open(gitdir / refname, "r") as f:
        content = f.read()
        if "ref" in content:
            ref = content.split()[1] 
        else:
            return content
    if (gitdir / ref).exists():
        with open(gitdir / ref, "r") as f:
            return f.read() 
    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    with open(gitdir / "HEAD", "r") as f:
        if "ref" not in f.read():
            return True 
        else:
            return False 


def get_ref(gitdir: pathlib.Path) -> str:
    with open(gitdir / "HEAD", "r") as f:
        return f.read().split()[1]
