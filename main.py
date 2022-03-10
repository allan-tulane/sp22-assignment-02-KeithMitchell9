"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time
import tabulate

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    

## Imported from Lab 3
def quadratic_multiply(x, y):
  return _quadratic_multiply(x, y).decimal_val

## Imported from Lab 3
def _quadratic_multiply(x, y):
  
  xvec = x.binary_vec
  yvec = y.binary_vec

  if x.decimal_val <= 1 and y.decimal_val <= 1:
    return BinaryNumber(x.decimal_val * y.decimal_val)

  xvec, yvec = pad(xvec, yvec)

  xl, xr = split_number(xvec)
  yl, yr = split_number(yvec)

  left = _quadratic_multiply(xl, yl)
  mid_left = _quadratic_multiply(xl, yr)
  mid_right = _quadratic_multiply(xr, yl)
  right = _quadratic_multiply(xr, yr)

  mid = BinaryNumber(mid_left.decimal_val + mid_right.decimal_val)
  mid = bit_shift(mid, len(xvec) // 2)
  left = bit_shift(left, len(xvec))

  bin_mult = BinaryNumber(left.decimal_val + mid.decimal_val + right.decimal_val)

  return bin_mult
## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y

def subquadratic_multiply(x, y):
  return _subquadratic_multiply(x, y).decimal_val

def _subquadratic_multiply(x, y):
  
  xvec = x.binary_vec
  yvec = y.binary_vec

  if x.decimal_val <= 1 and y.decimal_val <= 1:
    return BinaryNumber(x.decimal_val * y.decimal_val)

  xvec, yvec = pad(xvec, yvec)

  xl, xr = split_number(xvec)
  yl, yr = split_number(yvec)

  left = _subquadratic_multiply(xl, yl)
  ##mid_left = subquadratic_multiply(xl, yr)
  ##mid_right = subquadratic_multiply(xr, yl)
  right = _subquadratic_multiply(xr, yr)

  mid1 = BinaryNumber(xl.decimal_val + xr.decimal_val)
  mid2 = BinaryNumber(yl.decimal_val + yr.decimal_val)
  
  mid = _subquadratic_multiply(mid1, mid2)
  newmid = mid.decimal_val - (left.decimal_val + right.decimal_val)
  newmid = BinaryNumber(newmid)
  newmid = bit_shift(newmid, len(xvec) // 2)
  left = bit_shift(left, len(xvec))

  bin_mult = BinaryNumber(left.decimal_val + newmid.decimal_val + right.decimal_val)

  return bin_mult

## Feel free to add your own tests here.
def test_multiply():
  assert subquadratic_multiply(BinaryNumber(4), BinaryNumber(2)) == 4*2
  assert subquadratic_multiply(BinaryNumber(4), BinaryNumber(4)) == 4*4
  assert subquadratic_multiply(BinaryNumber(6), BinaryNumber(8)) == 6*8

def time_multiply(x, y, f):
    start = time.time()
    f(BinaryNumber(x), BinaryNumber(y))
    return (time.time() - start)*1000

## Imported from Lab 2
def print_results(results):
    print(tabulate.tabulate(results,
                            headers=['n', 'Subquadratic Times', 'Quadratic Times'],
                            floatfmt=".3f",
                            tablefmt="github"))

## Imported from Lab 2
def compare_multiply(fn_1, fn_2, sizes=[0, 10, 100, 1000, 10000, 100000, 1000000]):
    result = []
    for n in sizes:
        result.append((n, time_multiply(n, n, fn_1), time_multiply(n, n, fn_2)))
    return result


def test_compare_multiply():
  compare_multiply(subquadratic_multiply, _quadratic_multiply, sizes=[0, 10, 100, 1000, 10000, 100000, 1000000])