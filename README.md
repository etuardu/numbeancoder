# numbeancoder
A number to EAN13-code encoder/decoder with some security.

This module provides facilities to create a EAN13-code from an integer
and decode it back. The codes are signed against a salt in order to
allow the verification that they belong to a given scope, i.e. that
they were created using that specific salt.
The integer must be up to 4 digits long.

Usage (cli, encoding only):
```
$ ./numbeancoder.py test 45
0045245903365
```

Usage (python interpreter):
```
>>> import numbeancoder
>>> ean = numbeancoder.Numbeancoder('test')
>>> ean.encode(45)
'0045245903365'
>>> ean.decode('0045245903365')
45
```

The structure of the resulting EAN13-code is the following:
```
  0045 24590336 5
   |    |       |
   |    |       +- EAN checksum
   |    |
   |    +- signature
   |
   +- input number
```
