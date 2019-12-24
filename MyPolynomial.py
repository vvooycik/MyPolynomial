class InvalidOperandError(Exception):
	def __init__(self):
		print("You cannot add these elements")



class InvalidInputOperandError(Exception):
	def __init__(self):
		print(f"The type is incorrect. Provide integer.")



class OperationNotSupportedError(TypeError):
	def __init__(self):
		print(f"{self} is not supported yet")



class MyPolynomial:

	def __init__(self, *args):
		if not args:
			args = [0]
		for i in args:
			if isinstance(i, bool) or not isinstance(i,(int,float,complex)):
				raise InvalidInputOperandError
		self.__coefs = self._truncate_zeros(*args) 

	def _truncate_zeros(self, *args):
		i = len(args)
		while i>1 and args[i-1] == 0:
			i -= 1
		return list(args[:i])

	@classmethod
	def from_iterable(cls, iterable):
		return cls(*iterable)

	def __str__(self):
		st = '{}'.format(self.__coefs[0])
		for i in range(1, len(self.__coefs)):
			if self.__coefs[i] == 0:
				continue
			elif self.__coefs[i] == 1:
				st += ' + x^{}'.format(i)
			elif self.__coefs[i] == -1:
				st += ' - x^{}'.format(i)
			elif self.__coefs[i] < -1 :
				st += ' - {}x^{}'.format(abs(self.__coefs[i]), i)
			else:
				st += ' + {}x^{}'.format(self.__coefs[i], i)
		return st

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(repr(x) for x in self.__coefs)})"
		# if sum(self.__coefs) == 0:
		# 	return "MyPolynomial(0)"
		# return "MyPolynomial{}".format(tuple(self.__coefs))

	def __call__(self, x):
		if not isinstance(x, int):
			raise InvalidInputOperandError
		result = self.__coefs[0]
		result += sum([self.__coefs[i] * x ** i for i in range(1, len(self.__coefs))])
		return result

	def __getitem__(self, idx):
		return self.__coefs[idx]

	def __eq__(self, other):
		self.__coefs = self._truncate_zeros(*self.__coefs)
		other.__coefs = other._truncate_zeros(*other.__coefs)

		if len(self.__coefs) == len(other.__coefs):
			for i in range(0, len(self.__coefs)):
				if self.__coefs[i] != other.__coefs[i]:
					return False
			return True 
		else:
			return False

	def __add__(self, other):
		if type(self) != type(other):
			if type(other) == type(1):
				result = self
				result.__coefs[0] += other
				return result
			else: 
				raise InvalidOperandError
		if len(self.__coefs) > len(other.__coefs):
			dif = len(self.__coefs) - len(other.__coefs)
			other.__coefs += [0] * dif
		elif len(other.__coefs) > len(self.__coefs):
			dif = len(other.__coefs) - len(self.__coefs)
			self.__coefs += [0] * dif
		new_coefs = [self.__coefs[i] + other.__coefs[i] for i in range(0, len(self.__coefs))]
		return MyPolynomial(*new_coefs)
		
	def __pow__(self, power):
		raise OperationNotSupportedError

	def __rshift__(self,other):
		raise OperationNotSupportedError

	def __lshift__(self, other):
		raise OperationNotSupportedError

	def __radd__(self, other):
		return self + other

	def __iadd__(self, other):
		if type(self) != type(other):
			self.__coefs[0] += other
			return self
		if len(self.__coefs) > len(other.__coefs):
			dif = len(self.__coefs) - len(other.__coefs)
			other.__coefs += [0] * dif
		elif len(other.__coefs) > len(self.__coefs):
			dif = len(other.__coefs) - len(self.__coefs)
			self.__coefs += [0] * dif
		self.__coefs = [self.__coefs[i] + other.__coefs[i] for i in range(0, len(self.__coefs))]
		return self

	def __sub__(self, other):
		if isinstance(other, MyPolynomial):
			return self + (-other)
		# elif isinstance(other, int):
		# 	result = self
		# 	result.__coefs[0] = result.__coefs[0] - other
		# 	return result
		else:
			raise InvalidOperandError

	def __isub__(self, other):
		if isinstance(other, MyPolynomial):
			result = self + (-other)
			self.__coefs = result.__coefs
			return self
		# elif isinstance(other, int):
		# 	self.__coefs[0] = self.__coefs[0] - other
		else:
			raise InvalidOperandError
			
	def __rsub__(self, other):
		return self - other
		
	def __neg__(self):
		self.__coefs = [-i for i in self.__coefs]
		return self

	def __mul__(self, other):
		# if isinstance(other, int):
		# 	new_coefs = [x * other for x in self.__coefs]
		# 	return MyPolynomial(*new_coefs)
		if isinstance(other, MyPolynomial):
		  new_coefs = self._inner_mul(other)
		  return MyPolynomial(*new_coefs)
		else:
		  raise InvalidOperandError
		

	def __imul__(self, other):
		if isinstance(other, int):
			self.__coefs = [x * other for x in self.__coefs]
			return self
		elif isinstance(other, MyPolynomial):
		  self.__coefs = self._inner_mul(other)
		  return self
		else:
		  raise InvalidOperandError

	def __rmul__(self, other):
		return self * other

	def _inner_mul(self, other):
		new_len = len(self.__coefs) + len(other.__coefs) - 1
		new_coefs = [0] * new_len
		computation_matrix = [[0] * new_len] * len(self.__coefs)
		for s_i, s in enumerate(self.__coefs):
				computation_matrix[s_i] = [0]*s_i + [s*o for o in other.__coefs]
				while len(computation_matrix[s_i]) < new_len:
					computation_matrix[s_i] += [0]		
		for i in range(len(computation_matrix)):
			for j in range(len(computation_matrix[i])):
				new_coefs[j] += computation_matrix[i][j]
		new_coefs = new_coefs
		return new_coefs 

	def __truediv__(self, other):
		if isinstance(other, bool):
			raise InvalidOperandError
		if isinstance(other, (int, float)) and other != 0:
			self.__coefs = [i/other for i in self.__coefs]
			return self
		else:
		  raise InvalidOperandError
			
	def __rtruediv__(self, other):
	  raise OperationNotSupportedError
	
	def __floordiv__(self, other):
		raise OperationNotSupportedError

	def degree(self):
		return len(self.__coefs) - 1

# args = ['1','2']
# a = MyPolynomial(*args)
# print(str(MyPolynomial(-1, 1, -2)))
# assert '-1 + x^1 - 2x^2' == str(MyPolynomial(-1, 1, -2))
# test1 = MyPolynomial(0,1,2,0,-1, 0)
# test2 = MyPolynomial(-3,4,-5)
# print(str(test2))
# test3 = test1 + test2

a = MyPolynomial(1, 2, 3)
try:
    c = a + "22"
except InvalidOperandError:
  print('cought InvalidOperandError exception')


try:
    a = MyPolynomial(1, 2, {'a': 11})
except InvalidInputOperandError:
  print('cought InvalidInputOperandError exception')
  
  
try:
    c = a >> 1
except OperationNotSupportedError:
  print('cought OperationNotSupportedError exception')

print("Zadanie 1")
assert type(MyPolynomial()) is MyPolynomial
assert type(MyPolynomial(1)) is MyPolynomial
assert type(MyPolynomial(1, 2)) is MyPolynomial
assert type(MyPolynomial(0, 0)) is MyPolynomial
assert any(
    name.startswith("_") and not callable(name)
    for name in MyPolynomial().__dict__.keys()
)


print("Zadanie 2")
assert "1 + 2x^1" == str(MyPolynomial(1, 2))
assert "MyPolynomial(1, 2)" == repr(MyPolynomial(1, 2))
assert "MyPolynomial(0)" == repr(MyPolynomial())
assert "MyPolynomial(0)" == repr(MyPolynomial(0, 0, 0))
assert "0" == str(MyPolynomial(0, 0, 0))


print("Zadanie 3")
assert MyPolynomial(1, 2, 2)(0) == 1
assert MyPolynomial(1, 2, 2)(1) == 5
assert MyPolynomial(1, 2, 2)(2) == 13
assert MyPolynomial(1, 2, 2)(3) == 25
assert MyPolynomial(1, 2, 2)(4) == 41


print("Zadanie 4")
assert MyPolynomial(1, 2, 2) == MyPolynomial(1, 2, 2)
assert (MyPolynomial(1, 2, 2) == MyPolynomial(1, 2)) is False
assert MyPolynomial(0) == MyPolynomial()
assert MyPolynomial(0, 0) == MyPolynomial(0)
assert MyPolynomial(0, 0, 0) == MyPolynomial(0)
assert MyPolynomial(1, 0, 0) == MyPolynomial(1)
assert MyPolynomial(0, 1, 0) == MyPolynomial(0, 1)
assert MyPolynomial(0, 1, 1) == MyPolynomial(0, 1, 1)


print("Zadanie 5")
assert MyPolynomial.from_iterable([0, 1, 2]) == MyPolynomial(0, 1, 2)
assert MyPolynomial.from_iterable((0, 1, 2)) == MyPolynomial(0, 1, 2)
assert MyPolynomial.from_iterable([1, 2, 2]) == MyPolynomial(1, 2, 2)
assert (MyPolynomial.from_iterable((1, 2, 2)) == MyPolynomial(1, 2)) is False
assert MyPolynomial.from_iterable([0]) == MyPolynomial()
assert MyPolynomial.from_iterable([0, 0]) == MyPolynomial(0)
assert MyPolynomial.from_iterable(set([0, 0, 0])) == MyPolynomial(0)

print("Zadanie 6")
assert MyPolynomial(5, 4).degree() == 1
assert MyPolynomial().degree() == 0
assert MyPolynomial(0, 0, 0).degree() == 0
assert MyPolynomial(0, 1, 0).degree() == 1
assert MyPolynomial(0, 0, 1).degree() == 2
assert MyPolynomial.from_iterable([0, 1, 0]).degree() == 1


print("Zadanie 7")
assert MyPolynomial(5, 8) == MyPolynomial(2, 4) + MyPolynomial(3, 4)
assert MyPolynomial(5, 4) == MyPolynomial(2) + MyPolynomial(3, 4)
assert MyPolynomial(6, 4) == MyPolynomial(2, 4) + MyPolynomial(4)

mp1 = MyPolynomial(2, 4)
old_id = id(mp1)
mp2 = MyPolynomial(3, 4)
mp3 = MyPolynomial(5, 8)
mp1 += mp2
new_id = id(mp1)
assert mp3 == mp1
assert old_id == new_id, "After +=, you returned different object!"


print("Zadanie 8")
assert MyPolynomial(6, 14, 8) == MyPolynomial(2, 2) * MyPolynomial(3, 4)
assert MyPolynomial(9, 6, 13, 4, 4) == MyPolynomial(3, 1, 2) * MyPolynomial(3, 1, 2)
assert MyPolynomial(16, 24, 25, 20, 10, 4, 1) == MyPolynomial(
    4, 3, 2, 1
) * MyPolynomial(4, 3, 2, 1)
assert MyPolynomial(1, 4, 7, 10, 8) == MyPolynomial(1, 2) * MyPolynomial(1, 2, 3, 4)
assert MyPolynomial(1, 4, 7, 10, 8) == MyPolynomial(1, 2, 3, 4) * MyPolynomial(1, 2)
assert MyPolynomial(6, 14, 8) == MyPolynomial(3, 7, 4) * 2
assert MyPolynomial(9, 21, 12) == 3 * MyPolynomial(3, 7, 4)
mp1 = MyPolynomial(3, 7, 4)
mp1_old_id = id(mp1)
mp2 = MyPolynomial(0)
mp1 *= mp2
mp1_new_id = id(mp1)
assert mp1 == mp2, "Something went wrong with: MyPolynomial * MyPolynomial"
assert mp1_old_id == mp1_new_id, "After *=, you returned different object!"

mp1 = MyPolynomial(3, 7, 4)
mp1_old_id = id(mp1)
mp1 *= 0
mp1_new_id = id(mp1)
assert mp1 == MyPolynomial(0), "Something went wrong with: MyPolynomial *= number"
assert mp1_old_id == mp1_new_id, "After *=, you returned different object!"

