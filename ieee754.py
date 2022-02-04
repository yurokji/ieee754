from numbers import Number
import string
NUM_SIGN = 1
NUM_EXP = 8
NUM_MENTISSA = 23

class IEEE754_Float32:
	def __init__(self, strFloat):
		sg, num, point = self.strSplit(strFloat)
		num = self.convNum2Bin(num)
		point = self.convPoint2Bin(point)
		ordinay_float = num+"."+point
		print("정규화 전:"+ordinay_float)
		self.value = self.convertNormalize(sg, num, point)
	# value 16진수로 출력
	def __str__(self):
		S = self.value[0]
		E = self.value[1]
		M = self.value[2]		
		binaryString = '0b'+str(S) + str(bin(E))[2:] + M
		return hex(int(binaryString, 2))

	#  부동 소수 덧셈
	def __add__(self, other):
		#  두 수의 부호가 같은 경우
		s1 = self.value[0]
		s2 = other.value[0]
		e1 = self.value[1]
		e2 = other.value[1]
		m1 = self.value[2]
		m2 = other.value[2]
		s3 = 0
		e3 = 0
		m3 = 0
		print(m1)
		print(m2)
		if(s1 == s2):
			if(e1 != e2):
				diff_e = e1 - e2
				if diff_e > 0:
					e2 += diff_e
					m2 = "0" * (diff_e - 1) + "1" + m2[:len(m2)-diff_e]

				else:
					e1 += abs(diff_e)
					m1 = "0" * (abs(diff_e) - 1) + "1" + m1[:len(m1)-abs(diff_e)]

			e3 = e1
			m3 = str(bin(int(m1,2) + int(m2,2)))[2:]
			num_overflow = len(m3) - NUM_MENTISSA
			if num_overflow < 0:
				m3 = "0" * abs(num_overflow) + m3
			num_overflow = len(m3) - NUM_MENTISSA
			if num_overflow > 0:
				e3 += num_overflow
				m3 = m3[num_overflow:]
			print(m1)
			print(m2)
			print(m3)
		obj = IEEE754_Float32("0.0")
		obj.value = [s3, e3, m3]
		return obj
					

	# 원본 부동소수 문자열을 분리
	def strSplit(self, str):
		num, point = str.split('.')
		sg = 0
		if(num[0] == '-'):
			sg = 1
			num = num[1:]
		return sg, int(num), int(point)

	# 소수점 위의 숫자를 이진수 문자열로 
	def convNum2Bin(self, value):
		share = value
		resultStr = ""
		while share != 0:
			resultStr += str(share % 2)
			share = share // 2
		resultStr = resultStr[::-1]
		return resultStr

	# 소수점 아래의 숫자를 이진수 문자열로
	def convPoint2Bin(self, value):
		MAX_DIGITS = 32
		num = value
		original_digits = len(str(num)) 
		resultStr = ""
		curr_bit = ""
		for i in range(MAX_DIGITS):
			num = num * 2
			digits = len(str(num)) 
			if digits > original_digits:
				num -= 10 ** (digits - 1)
				curr_bit = "1"
			else:
				curr_bit = "0"
			resultStr += curr_bit
		return resultStr
			 
	# 정규화된 ieee754형태의 부동소수 저장
	def convertNormalize(self, sg, num, point):
		S = sg
		e = len(num) - 1
		E = 127 + e
		point = num[1:]+ point
		M = point[:NUM_MENTISSA]
		return [S, E, M]


strNum1 = "129.55275"
strNum2 = "18.5625"
fnum1 = IEEE754_Float32(strNum1)
fnum2 = IEEE754_Float32(strNum2)
fnum3 = fnum1 + fnum2
print(fnum1)
print(fnum2)
print(fnum3)

