import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree = []

    catalog_items = []
    for item in (gitdir.parent / dirname).glob("*"):
        catalog_items.append(str(item))

    for entry in index:   
        if entry.name in catalog_items:
            record = (entry.mode, entry.name, entry.sha1)
        else:
            folder = entry.name.split("/")[0]
 
            if dirname == "":
                sha1 = bytes.fromhex(write_tree(gitdir, [entry], folder))
                record = (0o40000, str(gitdir.parent / folder), sha1)
            else:
                sha1 = bytes.fromhex(write_tree(gitdir, [entry], dirname + "/" + folder))
                record = (0o40000, str(gitdir.parent / dirname / folder), sha1)
        tree.append(record)
    
    tree.sort(key=lambda x: x[1]) 
    data = b""
    for elem in tree:
        line = f"{oct(elem[0])[2:]} {elem[1].split('/')[-1]}\0".encode() + elem[2]
        data += line

    return hash_object(data, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if time.timezone > 0:
        timezone = "-"
    else:
        timezone = "+" 
    timezone += f"{abs(time.timezone) // 60 // 60:02}{abs(time.timezone) // 60 % 60:02}"
    data = f"tree {tree}\nauthor {author} {int(time.mktime(time.localtime()))} {timezone}\n" 
    data+= f"committer {author} {int(time.mktime(time.localtime()))} {timezone}\n"
    data += f"\n{message}\n"
    
    data = data.encode() 

    return hash_object(data, "commit", write=True)
