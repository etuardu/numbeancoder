#!/usr/bin/env python3
"""
numbeancoder - A number to EAN13-code encoder/decoder with some security

This module provides facilities to create a EAN13-code from an integer
and decode it back. The codes are signed against a salt in order to
allow the verification that they belong to a given scope, i.e. that
they were created using that specific salt.
The integer must be up to 4 digits long.

Usage (cli, encoding only):
$ ./numbeancoder.py test 45
0045245903365

Usage (python interpreter):
>>> import numbeancoder
>>> ean = numbeancoder.Numbeancoder('test')
>>> ean.encode(45)
'0045245903365'
>>> ean.decode('0045245903365')
45

The structure of the resulting EAN13-code is the following:

  0045 24590336 5
   |    |       |
   |    |       +- EAN checksum
   |    |
   |    +- signature
   |
   +- input number

"""

import hashlib
import sys

class Numbeancoder:
  def __init__(self, salt):
    self.salt = salt

  def encode(self, n):

    str_n = str(n)

    if len(str_n) > 4:
      raise ValueError('Input number longer than 4 digits: {}'.format(n))

    # 8-digits decimal salted hash of n
    str_hash = str(
      int(
        hashlib.sha256(
          (self.salt + str_n).encode('utf-8')
        ).hexdigest()[:8],
        16 # from base
      )
    )[:8].zfill(8)

    str_n_hash = str_n.zfill(4) + str_hash
    return str_n_hash + self.eanMakeChecksum(str_n_hash)

  def decode(self, code):
    if not self.eanVerifyChecksum(code):
      raise ValueError([-1, 'Checksum error'])

    n = int(code[:4])
    if code != self.encode(n):
      raise ValueError([-2, 'Hash mismatch'])

    return n

  def eanVerifyChecksum(self, code):
    return self.eanMakeChecksum(code[:-1]) == code[-1]
    
  def eanMakeChecksum(self, number):
    """Return the checksum for a EAN-13 code
    @param {string} number - The first 12 digits of a EAN-13 code
    @return {int} The checksum to be appended"""
    return str((10 - sum(
      (3, 1)[i % 2] * int(n)
      for i, n in enumerate(reversed(number))
    )) % 10)

if __name__ == '__main__':
  ean = Numbeancoder(sys.argv[1])
  print(ean.encode(sys.argv[2]))
