import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = (fmt + f" {len(data)}\0").encode() 
    store = header + data
    hash_obj = hashlib.sha1(store).hexdigest() 

    if write:
        repo = repo_find() 
        objects = repo / "objects" / hash_obj[:2]
        if not objects.exists():
            objects.mkdir() 
        
        with open(objects / hash_obj[2:], "wb") as f: 
            compressed = zlib.compress(store)
            f.write(compressed)

    return hash_obj

# возвращает названия объектов, походящих под obj_name
def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    
    repo = repo_find() 
    obj_path = repo / "objects" / obj_name[:2]
    objects = []

    if obj_path.exists() and obj_path.is_dir():
        for child in obj_path.iterdir():
            if child.name[:3] == obj_name[2:]:
                objects.append(obj_name[:2] + child.name) 

    if len(objects) == 0:
        raise Exception(f"Not a valid object name {obj_name}") 

    return objects

def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2]

    with open(path / sha[2:], "rb") as f:
        store = f.read()
        store = zlib.decompress(store)
        header = store[:store.find(b"\0") + 1]
        data = store[store.find(b"\0") + 1:]

    fmt = (header[:header.find(b" ")]).decode()
    
    return (fmt, data)
    

def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree_files = []

    while data != b"":
        mode = data[:data.find(b" ")]
        data = data[data.find(b" ") + 1:]
        name = data[:data.find(b"\0")]
        data = data[data.find(b"\0") + 1:]
        sha1 = data[:20]
        data = data[20:]

        mode = int(mode.decode())
        name = name.decode()
        sha1 = bytes.hex(sha1)
        tree_files.append((mode, name, sha1))

    return tree_files


def cat_file(obj_name: str, pretty: bool = True) -> None:
    repo = repo_find() 

    read_obj = read_object(obj_name, repo)
    if read_obj[0] == "blob":
        print(read_object(obj_name, repo)[1].decode())
    elif read_obj[0] == "tree":
        objs = read_tree(read_obj[1])
        s = ""
        for obj in objs:
            if obj[0] == 40000:
                s += f"0{obj[0]} tree {obj[2]}\t{obj[1]}\n"
            else:
                s += f"{obj[0]} blob {obj[2]}\t{obj[1]}\n"
        print(s)
    elif read_obj[0] == "commit":
        print(read_obj[1].decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    tree_data = read_object(tree_sha, gitdir)[1]
    tree = read_tree(tree_data)
    tree_files = []

    while tree_data != b"":
        tree_data = tree_data[tree_data.find(b" ") + 1:]
        name = tree_data[:tree_data.find(b"\0")]
        name = name.decode()
        tree_data = tree_data[tree_data.find(b"\0") + 1:]
        sha1 = tree_data[:20]
        sha1 = bytes.hex(sha1)
        tree_data = tree_data[20:]
        
        check_if_tree = read_object(sha1, gitdir)
        if check_if_tree[0] == 'tree':
            tree = read_tree(check_if_tree[1])
            subname = tree[0][1]
            tree_files.append((name + "\\" + subname, tree[0][2]))
        elif check_if_tree[0] == 'blob':
            tree_files.append((name, sha1))
    
    return tree_files


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
