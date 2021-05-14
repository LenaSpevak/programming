import os
import pathlib
import typing as tp
import shutil

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref, symbolic_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir))
    commit = commit_tree(gitdir, tree, message, author=author) 
    return commit


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:    
    indexes = [index.name for index in read_index(gitdir)]
    catalog = gitdir.parent 
    for obj in catalog.iterdir():
        if obj in [gitdir.name]:
            continue
        for index in indexes:
            if obj.name in index:
                if obj.is_dir():
                    shutil.rmtree(obj.name)
                else:
                    os.remove(obj)

    commit = read_object(obj_name, gitdir)[1].decode()
    tree = commit.split()[1]
    tree_files = find_tree_files(tree, gitdir)

    for name, sha1 in tree_files:
        if "/" in name:
            dirname, filename = name.split("\\")
            (gitdir.parent / dirname).mkdir()
            with open(gitdir.parent / dirname / filename, "w") as f:
                f.write(read_object(sha1, gitdir)[1].decode())
        else:
            with open((gitdir.parent) / name, "w") as f:
                f.write(read_object(sha1, gitdir)[1].decode()) 

    symbolic_ref(gitdir, name=obj_name, ref=get_ref(gitdir))
    return None
