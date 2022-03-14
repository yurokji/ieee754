class IEEE754_Float32:
	def __init__(self, strFloat):
		self.BIAS = 127
		self.NUM_EXP = 8
		self.NUM_MENTISSA = 23

		sg, num, point = self.strSplit(strFloat)
		# 문자열을 고정소수점 실수로 변환
		num = self.convDecimalNum2BinStr(num)
		point = self.convDecimalPoint2BinStr(point)
		print("10진수            실수:", strFloat)
		print(" 2진수 고정수수점 실수:", num+"."+point)
		# 고정소수점 실수를 부동소수로 변환
		self.S, self.E, self.M = self.convIEEE754Format(sg, num, point)

	def __str__(self):
		res = ""
		if self.S == 1:
			res += "-"
		exp = self.E - self.BIAS
		# 1.000000 을 표시하기 위해 bit_mask 필요
		bit_mask  = (1 << self.NUM_MENTISSA)
		mentissa = self.M | bit_mask
		# 소수점 위의 수 변환
		num = mentissa >> (self.NUM_MENTISSA - exp)

		# 소수점 아래 수를 고정 소수점으로
		point_mask = (2 ** self.NUM_MENTISSA) - 1
		point_mask = point_mask >> exp
		point = self.M & point_mask
		point = point << exp
		point = self.convBinPoint2DecimalPoint(point)
		res += str(num)
		res += "."
		res += str(point)
		return res

	def toHex(self):
		S = self.S
		E = self.E
		M = self.M
		binNumber = S << (self.NUM_EXP + self.NUM_MENTISSA) | E << self.NUM_MENTISSA | M
		return hex(binNumber)

	# 문자열을 분리함
	def strSplit(self, str):
		# "."을 기준으로 나눔
		num, point = str.split(".")
		# 기본 부호는 +
		sg = 0
		# 문자열의 첫번째가 음수를 
		# 나타내는 "-"라면
		if num[0] == '-':
			# 부호를 1로 만들어준다
			sg = 1
			num = num[1:]
		return sg, int(num), int(point)

	# 10진수 소수점 위 숫자를 2진수 문자열로
	def convDecimalNum2BinStr(self, value):
		share = value
		resultStr =""
		while share != 0:
			resultStr += str(share % 2)
			share //= 2
		# 문자열을 거꾸로 뒤집는다
		resultStr = resultStr[::-1]
		return resultStr

	# 10진수 소수점 아래의 숫자를 2진수 문자열로
	# 주의) 문자열 위치를 맟춰주어야 함
	# "5682373" --> 10진수 7자리 수
	# .1101000000000000000000000000000000
	#  50000000000000000000000000
	# +25000000000000000000000000
	# +06250000000000000000000000
	def convDecimalPoint2BinStr(self, value):
		MAX_DIGITS = 32
		num = value
		original_digits = len(str(value))
		resultStr = ""
		curr_bit =""
		for i in range(MAX_DIGITS):
			num *= 2
			digits = len(str(num))
			# 문자열의 자리수(10진수)가 커졌을 때
			# 1을 현재자리수(2진수)로 저장한다
			if digits > original_digits:
				num -= 10 ** (digits - 1)
				curr_bit = "1"
			else:
				curr_bit = "0"
			resultStr += curr_bit
		return resultStr

	# 정규화된 ieee754 부동소수 변화(정밀도 32비트, single precision단정밀)
	def convIEEE754Format(self, sg, num, point):
		S = sg
		e = len(num) - 1
		# 바이어스 127을 더해줌
		E = self.BIAS + e
		point = num[1:] + point
		M = point[:self.NUM_MENTISSA]
		M = int(M,2)
		# 라운딩
		if point[self.NUM_MENTISSA] == "1":
			M += 1
		return S, E, M

	# 2진수 고정 소수점을 10진수 소수점으로 변환
	def convBinPoint2DecimalPoint(self, value):
		bin_point = value
		multiplier = 50000000000000
		result = 0
		count = 0
		while True:
			shift_size = (self.NUM_MENTISSA - count - 1)
			if shift_size > 0:
				result += ((bin_point >> shift_size) & 1) * multiplier
				multiplier //= 2
				count += 1
			else:
				break
		return result


	# 부동 소수 덧셈 연산자
	def __add__(self, other):
		# 일단 두수의 부호가 같은 경우만 취급
		s1 = self.S
		s2 = other.S
		e1 = self.E
		e2 = other.E
		m1 = self.M
		m2 = other.M

		s3 = 0
		e3 = 0
		m3 = 0

		# 덧셈 전에 가수 위에 1.0을 붙여준다
		bit_mask = (1 << self.NUM_MENTISSA)
		m1 |= bit_mask
		m2 |= bit_mask
		# 지수의 차이만큼 한쪽의 가수부를 오른쪽으로 밀어준다
		# 그 대신 지수를 올려 맞춘다
		diff_e = e1 - e2
		if diff_e > 0:
			e2 += diff_e
			m2 = m2 >> diff_e
		elif diff_e < 0:
			e1 += abs(diff_e)
			m1 = m1 >> abs(diff_e)


		e3 = e1
		m3 = m1 + m2
		overflow_mask = 2 ** (self.NUM_MENTISSA + 1) - 1
		overflow = False
		if m3 > overflow_mask:
			overflow = True
		if overflow:
			m3 -= 2 ** (self.NUM_MENTISSA + 1) 
			m3 = m3 >> 1
			e3 += 1
		else:
			m3 -= 2 ** (self.NUM_MENTISSA)
		
		result = IEEE754_Float32("0.0")
		result.S = s3
		result.E = e3
		result.M = m3
		print(s3, e3, m3)
		return result

			




		

		





	
