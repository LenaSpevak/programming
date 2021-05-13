import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # PUT YOUR CODE HERE
    tree = []
    catalog_items = []
    for item in (gitdir.parent / dirname).glob("*"):
        #print(str(catalog_items))
        catalog_items.append(str(item))
    for entry in index:
        if entry.name in catalog_items:
            record = (entry.mode, entry.name, entry.sha1)
            tree.append(record)
        else:
            folder = entry.name.split("/")[0]
            #print(folder)
            if dirname == "":
                sha1 = bytes.fromhex(write_tree(gitdir, [entry], folder)) #entry - список файлов
                record = (0o40000, str(gitdir.parent / folder), sha1 )
            else:
                sha1 = bytes.fromhex(write_tree(gitdir, [enrty], dirname + "/" + folder))
                record = (0o40000, str(gitdir.parent / dirname / folder), sha1)
        tree.append(record)

        #print(pathlib.Path(entry.name).parent)
    tree.sort(key=lambda x: x[1]) #отсортировать всё по первому элементу-по именам
    data = b""
    for element in tree:
        line = f"{oct(element[0])[:2]} {element[1].split('/')[-1]}\0".encode + element[2]
        data += line

    return hash_object(data, "tree", True)

def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    if time.timezone > 0:
        timezone = "-"
    else:
        timezone = "+"
    timezone += f"{abs(time.timezone) // 60 // 60:02}{abs(time.timezone) // 60 % 60:02}"
    data = f"tree {tree}\nauthor {author} {int(time.mktime(time.localtime()))} {timezone}\n"
    data += f"commiter {author} {int(time.mktime(time.localtime()))} {timezone}\n"
    data += f"\n{message}\n"
    data = data.encode()
    return hash_object(data, "commit", write=True)