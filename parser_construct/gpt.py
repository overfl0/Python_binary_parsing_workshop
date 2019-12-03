from construct import Struct, Const, BytesInteger, Bytes, PaddedString, Array, this, Computed

guid = Struct(
    '_uid1' / BytesInteger(4, swapped=True),
    '_uid2' / BytesInteger(2, swapped=True),
    '_uid3' / BytesInteger(2, swapped=True),
    '_uid4' / BytesInteger(2),
    '_uid5' / BytesInteger(6),
    'guid' / Computed(lambda ctx: '{:08X}-{:04X}-{:04X}-{:04X}-{:012X}'.format(
        ctx._uid1, ctx._uid2, ctx._uid3, ctx._uid4, ctx._uid5))
)

gpt_header = Struct(
    'magic' / Const(b'EFI PART'),
    'revision' / BytesInteger(4),
    'header_size' / BytesInteger(4, swapped=True),
    'crc' / BytesInteger(4, swapped=True),
    'reserved' / Const(b'\x00\x00\x00\x00'),
    'current_lba' / BytesInteger(8, swapped=True),
    'backup_lba' / BytesInteger(8, swapped=True),
    'first_usable_lba' / BytesInteger(8, swapped=True),
    'last_usable_lba' / BytesInteger(8, swapped=True),
    'guid' / guid,
    'starting_lba' / BytesInteger(8, swapped=True),
    'nof_partitions' / BytesInteger(4, swapped=True),
    'partition_size' / BytesInteger(4, swapped=True),
    'partition_crc' / BytesInteger(4, swapped=True),
    'reserved2' / Bytes(420),
)

gpt_entry = Struct(
    'partition_type_guid' / guid,
    'unique_partition_guid' / guid,
    'first_lba' / BytesInteger(8, swapped=True),
    'last_lba' / BytesInteger(8, swapped=True),
    'flags' / Bytes(8),
    'partition_name' / PaddedString(72, 'utf_16_le'),
    'size' / Computed((this.last_lba - this.first_lba + 1) * 512)
)

gpt = Struct(
    'header' / gpt_header,
    'partitions' / Array(this.header.nof_partitions, gpt_entry)
)
