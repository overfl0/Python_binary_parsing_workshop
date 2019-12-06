# How to run the damn thing?

    pip install -r requirements.txt

Then fill in the Construct structures that will read an MBR (and possibly GPT entry).

When you're done, do a:

    python main.py

The data that it will try to read is in `data/nas_data.bin`.

You can compare your output with the original output of fdisk by looking at
`data/nas_sample_output.txt`.

You can find both the [MBR specification](https://en.wikipedia.org/wiki/Master_boot_record)
and the [GPT specification](https://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_table_header_\(LBA_1\))
on their respective Wikipedia pages.
