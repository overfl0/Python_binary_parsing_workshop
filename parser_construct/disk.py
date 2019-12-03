from construct import Struct, If

from parser_construct.gpt import gpt
from parser_construct.mbr import mbr


def is_gpt(ctx):
    return ctx.mbr.partition1.partition_type == 'GPT' or \
           ctx.mbr.partition2.partition_type == 'GPT' or \
           ctx.mbr.partition3.partition_type == 'GPT' or \
           ctx.mbr.partition4.partition_type == 'GPT'


full_data = Struct(
    'mbr' / mbr,
    'gpt' / If(is_gpt, gpt),
)
