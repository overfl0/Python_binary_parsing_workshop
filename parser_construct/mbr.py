from construct import Struct, Byte, Bitwise, BitsInteger, Computed, this, Enum, Hex, BytesInteger, Bytes, Const

chs_address = Struct(
    'head' / Byte,
    # 'sector' / Byte,
    # 'sector2' / Byte,
    '_inner'/ Bitwise(Struct(
        'high_cylinder' / BitsInteger(2),
        'sector' / BitsInteger(6),
        'low_cylinder' / BitsInteger(8),
    )),
    'sector' / Computed(this._inner.sector),
    'cylinder' / Computed((this._inner.high_cylinder << 8) + this._inner.low_cylinder)
)

partition_type = Enum(
    Hex(Byte),
    unused=0,
    GPT=0xEE,
    Linux=0x83,
)

partition = Struct(
    # 'bootable_flag' / FlagsEnum(Byte, bootable=0x80),  # bootable_flag.bootable
    # 'bootable_flag' / Bitwise(Struct('bootable' / Flag, Padding(7))),  # bootable_flag.bootable
    '_raw_byte' / Byte,
    'bootable_flag' / Computed(this._raw_byte & 0x80 == 0x80),
    'first_sector' / chs_address,
    'partition_type' / partition_type,
    'last_sector' / chs_address,
    'LBA_address' / BytesInteger(4, swapped=True),
    'nof_sectors' / BytesInteger(4, swapped=True),
    'size' / Computed(this.nof_sectors * 512),
)

mbr = Struct(
    'bytes' / Bytes(446),
    'partition1' / partition,
    'partition2' / partition,
    'partition3' / partition,
    'partition4' / partition,
    'magic' / Const(b'\x55\xAA')
)
