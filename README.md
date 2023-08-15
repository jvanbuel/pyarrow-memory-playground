# Python / PyArrow memory management

When creating an Arrow table from a Python object (collections of lists, dict, ...), the memory consumption doubles: it will create a separate copy of the table in Arrow's specific memory format.

To basically halve the amount of necessary memory, you can use some simple memory management tricks: read in the records in smaller batches, convert those batches into Arrow tables, concatenate the batches, and delete the Python objects containing the original data. 

This repo contains two example scripts, one with memory managament and one without.

 ⚠️CAVEAT⚠️: the `tracemalloc` module only seem to track memory used by Python objects, so the Arrow table (which relies on Arrow's C++ implementation) memory consumption should be tracked separately.
