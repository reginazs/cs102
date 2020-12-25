import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


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
        return struct.pack(
            "!10I20sh" + str(len(self.name)) + "s" + str(8 - (62 + len(self.name)) % 8) + "x",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino & 0xFFFFFFFF,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )

        ...

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        struct.unpacked("!LLLLLLLLLL20sH", data)
        return GitIndexEntry(
            unpacked[0],
            unpacked[1],
            unpacked[2],
            unpacked[3],
            unpacked[4],
            unpacked[5],
            unpacked[6],
            unpacked[7],
            unpacked[8],
            unpacked[9],
            unpacked[10],
            unpacked[11],
            unpacked[12].rstrip(b"\00").decode(),
        )
        ...


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index = []
    if not (gitdir / "index").is_file():
        return []
    with open(gitdir / "index", "rb") as index_file:
        data = index_file.read()
    entry_count = struct.unpack("!i", data[8:12])[0]
    data = data[12:]
    for _ in range(entry_count):
        entry = data[:60]
        flags = data[60:62]
        data = data[62:]
        entry += flags
        num_flags = int.from_bytes(flags, "big")
        name = data[:num_flags].decode()
        data = data[num_flags:]
        entry += name.encode()
        while True:
            if len(data) == 0:
                break
            byte = chr(data[0])
            if byte != "\x00":
                break
            entry += byte.encode("ascii")
            data = data[1:]

        entry_unpacked = GitIndexEntry.unpack(entry)
        index.append(entry_unpacked)

    return index
    ...


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index = gitdir / "index"
    with index.open("wb") as file:
        data = b"DIRC\00\00\00\02"
        data += struct.pack(">I", len(entries))
        for i in entries:
            data += i.pack()
        file.write(data + hashlib.sha1(data).digest())
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for entry in read_index(gitdir):
        if details:
            print(f"{entry.mode:o} {entry.sha1.hex()} 0\t{entry.name}")
        else:
            print(entry.name)

    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = read_index(gitdir)
    for i in paths:
        with i.open("rb") as f:
            data = f.read()
        stat = os.stat(i)
        entries.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash_object(data, "blob", write=True)),
                flags=7,
                name=str(i),
            )
        )
    if write:
        write_index(gitdir, sorted(entries, key=lambda x: x.name))
    ...
