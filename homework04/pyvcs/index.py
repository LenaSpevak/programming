import hashlib
import zlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object
from pyvcs.repo import repo_find

class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        fmt = "!" + "I"*10 + "20sH" + str(len(self.name)) + "s"
        packed = struct.pack(fmt, self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n, self.dev, self.ino, self.mode, self.uid, self.gid, self.size, self.sha1, self.flags, self.name.encode())
        return packed + b"\x00\x00\x00"

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        entry = {}
        size = struct.calcsize("I")
        entry["ctime_s"] = struct.unpack("!I", data[0:size])[0]
        data = data[size:]
        entry['ctime_n'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['mtime_s'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['mtime_n'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['dev'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['ino'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['mode'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['uid'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['gid'] = struct.unpack("!I", data[:size])[0]
        data = data[size:]
        entry['size'] = struct.unpack("!I", data[:size])[0]

        data = data[size:]
        entry['sha1'] = struct.unpack("!20s", data[:struct.calcsize("20s")])[0]
        data = data[struct.calcsize("20s"):]
        entry['flags'] = struct.unpack("!H", data[:struct.calcsize("H")])[0]
        data = data[struct.calcsize("H"):]
        namelen = entry['flags'] & 0xFFF
        entry['name'] = struct.unpack(f"!{namelen}s", data[:struct.calcsize(f"{namelen}s")])[0].decode()

        gitIndexEntry = GitIndexEntry(**entry) #распаковка словаря
        return gitIndexEntry

# список объектов в индексе
def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    repo = repo_find() / "index"
    entries = []

    if repo.exists():
        with open(repo, "rb") as f: 
            _ = f.read(8) 
            num_entries = struct.unpack("!I", f.read(4))[0]
            for entry in range(num_entries):
                indexEntry = {}

                indexEntry['ctime_s'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0] 
                indexEntry['ctime_n'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0] 
                indexEntry['mtime_s'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['mtime_n'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['dev'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['ino'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['mode'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['uid'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['gid'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]
                indexEntry['size'] = struct.unpack("!I", f.read(struct.calcsize("I")))[0]

                indexEntry['sha1'] = struct.unpack("!20s", f.read(struct.calcsize("20s")))[0]
                indexEntry['flags'] = struct.unpack("!H", f.read(struct.calcsize("H")))[0]
                namelen = indexEntry['flags'] & 0xFFF 
                indexEntry['name'] = struct.unpack("!" + str(namelen) + "s", f.read(struct.calcsize("!" + str(namelen) + "s")))[0].decode()
                
                entries.append(GitIndexEntry(**indexEntry))
                nuls = 3
                _ = f.read(nuls)

    entries.sort(key=lambda x: x.name)
    return entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    git = gitdir / "index"
    fmt = "!4s2I"
    index = struct.pack(fmt, b"DIRC", 2, len(entries))

    for entry in entries:
        packed = entry.pack() 
        index += packed 

    index += bytes.fromhex(hashlib.sha1(index).hexdigest()) # checksum
    with open(git, "bw") as f:
        f.write(index)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir) 
    if details:
        info = []
        for entry in entries:
            s = f"{oct(entry.mode)[2:]} {bytes.hex(entry.sha1)} 0\t{entry.name}"
            info.append(s) 
        s = "\n".join(info)
        print(s)
    else:
        names = []
        for entry in entries:
            names.append(entry.name) 

        s = "\n".join(names)
        print(s)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = read_index(gitdir)

    for path in paths:
        stat = path.stat()
        with open(path, "rb") as f:
            entry = GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_uid,
                size=stat.st_size,
                sha1= bytes.fromhex(hash_object(f.read(), "blob", write=write)),
                flags=len(str(path)),
                name=str(path),
            )
        entries.append(entry) 
    write_index(gitdir, entries)
