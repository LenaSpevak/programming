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
    # PUT YOUR CODE HERE
    header = fmt + f"{len(data)}\0".encode()
    store = header + data
    hashobj = hashlib.sha1(store).hexdigest()
    
    if write:
        repo = repo_find
        
        objects = repo / "objects" / hashobj[:2]
        if not objects.exists():
            objects.mkdir()
            
        with open(hashobj[2:], "wb") as f:
            compressed = zlib.compress(store)
            f.write(compressed)   
    return hashobj   



def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
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
    # PUT YOUR CODE HERE
    path = gitdir / "objects" / sha[:2]

    with open(path / sha[2:], "rb") as f:
        store = f.read()
        store = zlib.decompress(store)
        store = store.decode() # получить utf-строку из байтовой 
        header = store[:store.find("\0") + 1]
        data = store[store.find("\0") + 1:].encode()

    fmt = header[:header.find(" ")]
    
    return (fmt, data)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    repo = repo_find() 

    obj_path = repo / "objects" / obj_name[:2] 
    with open(obj_path / obj_name[2:], "rb") as f: 
        store = f.read() 
        store = zlib.decompress(store).decode() 
        data = store[store.find("\0") + 1:]
        print(data)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
