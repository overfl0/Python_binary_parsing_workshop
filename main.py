from hurry.filesize import size
from tabulate import tabulate

from parser_construct.disk import full_data


def get_mbr_partition_data(prefix, i, partition):
    return {
        'Device': prefix + str(i),
        'Boot': '*' if partition.bootable_flag else '',
        'Start': partition.LBA_address,
        'End': partition.LBA_address + partition.nof_sectors - 1,
        'Sectors': partition.nof_sectors,
        'Size': size(partition.size),
        'Id': hex(partition.partition_type.intvalue),
        'Type': partition.partition_type,
    }


def print_mbr(prefix, data):
    data_out = [
        get_mbr_partition_data(prefix, 1, data.mbr.partition1),
        get_mbr_partition_data(prefix, 2, data.mbr.partition2),
        get_mbr_partition_data(prefix, 3, data.mbr.partition3),
        get_mbr_partition_data(prefix, 4, data.mbr.partition4),
    ]

    # This is optional if you manage to get the Type of the partition
    # Don't print unused partitions
    data_out = [d for d in data_out if d['Type'] != 'unused']
    print(tabulate(data_out, headers='keys'))


# def get_gpt_partition_data(prefix, i, partition):
#     return {
#         'Device': prefix + str(i),
#         'Boot': '?',
#         'Start': '?',
#         'End': '?',
#         'Sectors': '?',
#         'Size': '?',
#         'Name': '?',
#     }
#
#
def print_gpt(prefix, data):
    return
#     if not data.gpt:
#         print('No GPT partition')
#         return
#
#     out = []
#
#     for i in range(data.gpt.header.nof_partitions):
#         if data.gpt.partitions[i].first_lba == 0:
#             continue
#
#         out.append(get_gpt_partition_data(prefix, i + 1, data.gpt.partitions[i]))
#
#     print()
#     print(tabulate(out, headers='keys'))


def print_info(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    parsed = full_data.parse(data)
    print_mbr(file_path, parsed)
    print_gpt(file_path, parsed)
    # print(parsed)


print_info('data/nas_data.bin')
