#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
import os
import zlib
import sys

file_name = "rcs"
if len(sys.argv) == 2:
    file_name = sys.argv[1]

@dataclass
class IndexItem:
  name: str
  offset: int


index_items = []
with open(f"{file_name}.ind", "rb") as archive:
  file_count = int.from_bytes(archive.read(2), byteorder="little")
  print(f"file count: {file_count}")
  for i in range(file_count):
    try:
        index_item = IndexItem(
          name=archive.read(20).decode(encoding="ascii").split('\0')[0],
          offset=int.from_bytes(archive.read(4), byteorder="little"),
        )
    except UnicodeDecodeError:
        index_item = IndexItem(
            name=f"Unkown{i}.tga",
            offset=int.from_bytes(archive.read(4), byteorder="little")
        )
    if i < 16:
      print(f"{i} {index_item}")
    if i > 0:
      index_items.append(
        index_item
      )


os.makedirs("result", exist_ok=True)
sorted
with open(f"{file_name}.img", "rb") as archive:
  archive.seek(4)
  check = int.from_bytes(archive.read(2), byteorder="little")
  if (check == 55928 or check == 40056):
    compressed = True
    print("Found that file contains compression")
  else:
    compressed = False
    print("No compression found")
  for i in range(len(index_items)):
    print(f"Creating {index_items[i].name}")
    archive.seek(index_item.offset);
    if compressed:
        size = int.from_bytes(archive.read(4), byteorder="little")
    else:
      next_index_offset = size = os.path.getsize(f"{file_name}.img")
      for index_item in index_items:
        if index_items[i].offset < index_item.offset and next_index_offset > index_item.offset:
          next_index_offset = index_item.offset
      size = next_index_offset - index_items[i].offset


    if size == 0:
      break
    with open(f"result/{index_items[i].name}", "wb") as archived_file:
      if compressed:
        archived_file.write(zlib.decompress(archive.read(size), wbits=zlib.MAX_WBITS))
      else:
        archive.seek(index_items[i].offset)
        archived_file.write(archive.read(size))
