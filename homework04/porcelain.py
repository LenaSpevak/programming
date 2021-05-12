import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    # PUT YOUR CODE HERE
    update_index(gitdir, path)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # PUT YOUR CODE HERE
    tree = write_tree(gitdir, read_index(gitdir))
    commit = commit_tree(gitdir, tree, message, author=author)
    return commit

def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    indexes = [index.name for index in read_index(gitdir)]
    catalog = gitdir.parent
    for obj in catalog.iterdir():
        if obj in [gitdir.name]:
            continue
        if obj.name in indexes:
            os.remove(obj)

    commit = read_object(obj_name, gitdir)[1].decode()
    tree = commit.split()[1]  #разделяет по всем нечитаемым символам
    #tree = read_object(tree, gitdir)[1]
