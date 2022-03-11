PLUS_PLUS = 0
PLUS_MINUS = 1
MINUS_PLUS = 2
MINUS_MINUS = 3

class IEEE754_Float32:
    def __init__(self, strFloat):
        self.BIAS = 127
        self.NUM_EXP = 8
        self.NUM_MENTISSA = 23
        # 문자열을 고정소수점 실수로 변환
        sg, numBinStr, pointBinStr = self.deicimalPointStr2FixedBinPointStr(strFloat)
        # 고정소수점 실수를 부동소수로 변환
        self.S, self.E, self.M = self.convIEEE754Format(sg, numBinStr, pointBinStr)

    def deicimalPointStr2FixedBinPointStr(self, strFloat):
        sign_str, num_str, point_str = self.strSplit(strFloat)
        num_str = self.convDecimalString2BinStr(num_str)
        point_str = self.convDecimalPointString2BinStr(point_str)
        return sign_str, num_str, point_str
    
    def printFixedBinNum(self, strFloat):
        sign_str, num_str, point_str = self.deicimalPointStr2FixedBinPointStr(strFloat)
        print("10진수            실수:", strFloat)
        print(" 2진수 고정수수점 실수:", sign_str+num_str+"."+point_str) 
         
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
        point = self.convBinPoint2DecimalPointStr(point)
        res += str(num)
        res += "."
        res += point
        return res

    def toHex(self):
        S = self.S
        E = self.E
        M = self.M
        binNumber = S << (self.NUM_EXP + self.NUM_MENTISSA) | E << self.NUM_MENTISSA | M
        return hex(binNumber)

    def countDecimalDigits(self, val):
        count = 1
        while True:
            if val // 10 > 0:
                val //= 10
                count += 1
            else:
                break
        return count

    # 문자열을 분리함
    def strSplit(self, inputStr):
        # "."을 기준으로 나눔
        num, point = inputStr.split(".")
        # 기본 부호는 +
        sg = "+"
        # 문자열의 첫번째가 음수를 
        # 나타내는 "-"라면
        if num[0] == '-':
            # 부호를 1로 만들어준다
            sg = "-"
            num = num[1:]
        return sg, num, point

    # 10진수 소수점 위 숫자를 2진수 문자열로
    def convDecimalString2BinStr(self, inputStr):
        share = int(inputStr)
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
    def convDecimalPointString2BinStr(self, inputStr):
        MAX_DIGITS = 32
        string_length = len(inputStr)
        num = int(inputStr)
        tenth_digits = self.countDecimalDigits(num)
        diff = string_length - tenth_digits
        resultStr = ""
        curr_bit =""
        for i in range(MAX_DIGITS):
            num *= 2
            digits =  self.countDecimalDigits(num)
            # 문자열의 자리수(10진수)가 커졌을 때
            # 1을 현재자리수(2진수)로 저장한다
            if digits > string_length:
                num -= 10 ** (digits - 1)
                curr_bit = "1"
            else:
                curr_bit = "0"
            resultStr += curr_bit
        return resultStr

    # 정규화된 ieee754 부동소수 변화(정밀도 32비트, single precision단정밀)
    def convIEEE754Format(self, sg, num, point):
        S = 0
        if sg == '-':
            S = 1
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
    def convBinPoint2DecimalPointStr(self, value):
        ten_digits = 15
        bin_point = value
        digits = self.countDigits(value)
        multiplier = 500000000000000 
        diff = self.NUM_MENTISSA - digits
        multiplier //= (2 ** diff)
        result = 0
        count = 0
        while True:
            shift_size = (self.NUM_MENTISSA - diff - 1)  - count 
            if shift_size > 0:
                result += ((bin_point >> shift_size) & 1) * (multiplier // (2 ** count))
                count += 1
            else:
                break
        result =str(result)
        result = result.zfill(ten_digits)  
        return result
    
    def negate(self, value):
        res = value ^ (2 ** (self.NUM_MENTISSA + 1) - 1)
        res += 1
        return res 

    # # 부동 소수 덧셈 연산자
    # def __add__(self, other):
    # 	# 일단 두수의 부호가 같은 경우만 취급
    # 	s1 = self.S
    # 	s2 = other.S
    # 	e1 = self.E
    # 	e2 = other.E
    # 	m1 = self.M
    # 	m2 = other.M

    # 	s3 = 0
    # 	e3 = 0
    # 	m3 = 0

    # 	# 덧셈 전에 가수 위에 1.0을 붙여준다
    # 	bit_mask = (1 << self.NUM_MENTISSA)
    # 	m1 |= bit_mask
    # 	m2 |= bit_mask
    # 	# 지수의 차이만큼 한쪽의 가수부를 오른쪽으로 밀어준다
    # 	# 그 대신 지수를 올려 맞춘다
    # 	diff_e = e1 - e2
    # 	if diff_e > 0:
    # 		e2 += diff_e
    # 		m2 = m2 >> diff_e
    # 	elif diff_e < 0:
    # 		e1 += abs(diff_e)
    # 		m1 = m1 >> abs(diff_e)


    # 	e3 = e1
    # 	m3 = m1 + m2
    # 	overflow_mask = 2 ** (self.NUM_MENTISSA + 1) - 1
    # 	overflow = False
    # 	if m3 > overflow_mask:
    # 		overflow = True
    # 	if overflow:
    # 		m3 -= 2 ** (self.NUM_MENTISSA + 1) 
    # 		m3 = m3 >> 1
    # 		e3 += 1
    # 	else:
    # 		m3 -= 2 ** (self.NUM_MENTISSA)
        
    # 	result = IEEE754_Float32("0.0")
    # 	result.S = s3
    # 	result.E = e3
    # 	result.M = m3
    # 	print(s3, e3, m3)
    # 	return result

    def compare(self, other):
        e1 = self.E
        e2 = other.E
        m1 = self.M 
        m2 = other.M
        diff_e = e1 - e2
        if diff_e > 0:
            return True
        elif diff_e < 0:
            return False
        else:
            if m1 >= m2:
                return True
            else:
                return False
            
    def countDigits(self, value):         
        count = 0
        while True:
            temp = (value >> count)
            if  temp== 0 or temp == 1:
                count +=1
                break
            else:
                count +=1
        return count
                
    # 부동 소수 덧셈 연산자
    def __add__(self, other):
        # 일단 두수의 부호가 같은 경우만 취급
        s1 = self.S
        s2 = other.S
        e1 = self.E
        e2 = other.E
        m1 = self.M
        m2 = other.M

        # 덧셈 전에 가수 M 위에 1.0을 붙여준다
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
        
        # 지수를 맞춘 후 
        # m1과 m2의 크기를 비교하여
        # m2가 더 크면 그 두 수를 서로 바꾼다
        # m1 <--> m2 (음수 계산을 위해)
        s3 = s1
        e3 = e1
           
        add_type = PLUS_PLUS
        if s1 == 0 and s2 == 1:
            add_type = PLUS_MINUS
        elif  s1 == 1 and s2 == 0:
            add_type = MINUS_PLUS
        elif s1 == 1 and s2 == 1:
            add_type = MINUS_MINUS
                 
                 
        if add_type == PLUS_MINUS:
            if self.compare(other):
                s3 = s1
            else:
                s3 = s2
            m3 = m1 + self.negate(m2)
            if m1 < m2:
                m3 = self.negate(m3)
        elif add_type == MINUS_PLUS:
            if self.compare(other):
                s3 = s1
            else:
                s3 = s2
            m3 = self.negate(m1) + m2
            if m1 > m2:
                m3 = self.negate(m3)
        elif add_type == MINUS_MINUS:
            s3 = 1
            m3 = m1 + m2
        else:
            m3 = m1 + m2
        
        # 뺄셈에 해당하는 덧셈의 경우(즉, 두 부호가 다른 경우)
        if add_type == PLUS_MINUS or add_type == MINUS_PLUS:       
            m3_digits = self.countDigits(m3)
            num_overflow_bits = m3_digits - (self.NUM_MENTISSA + 1) 
            # 뺄셈의 결과로 오버플로우 없음
            if num_overflow_bits < 0:
                # 모자라는 비트만큼 가수를 쉬프트하여 올려주어
                # 1.M의 형태로 만듬
                m3 = m3 << abs(num_overflow_bits)
                # 그리고 1.을 소거하기 위해 2^23승을 빼주어
                # 순수한 M 비트만 남김
                m3 -= 2 ** (self.NUM_MENTISSA)
                # M의 자리를 올려준만큼 반대로 지수를 빼줌 
                e3 -= abs(diff_e)

            # 뺄셈의 결과로 오버플로우 발생
            elif num_overflow_bits > 0:
                # 뺄셈의 결과에서 오버플로우는 버려야 함
                # 따라서 가수에서 오버플로우를 제거하기 위해
                # 오버플로우된 자리는 2^24에 있는 1을 빼줌
                overflow_number = 2 ** (self.NUM_MENTISSA + 1)
                m3 -= overflow_number 
                # 그리고 나머지 가수의 자리수를 다시 계산
                # 가수 유효자리수에서 실제 자리수가 
                # 얼마나 모자라는지 다시 계산한 후
                # 가수를 쉬프트하여 올려주고
                # 그만큼 지수에서 빼줌
                m3_digits = self.countDigits(m3)
                num_overflow_bits = m3_digits - (self.NUM_MENTISSA + 1) 
                m3 = m3 << abs(num_overflow_bits)
                e3 -= abs(num_overflow_bits)
                
        #  덧셈에 해당하는 덧셈의 경우(즉, 두 부호가 같은 경우, 예 ++, --) 
        else:
            # 가수의 모든 자리수가 1로 채워지는 수가 가장 큰 수
            # 이를 넘기면 오버플로우로 간주한다
            max_mentissa = 2 ** (self.NUM_MENTISSA + 1) - 1
            # 만약 오버플로우가 일어났는지 검사
            if m3 > max_mentissa:
                # 오버플로우가 일어났다면
                # 가수 위의 비트를 삭제하기 위해
                # 2^24승만큼 빼준후
                overflow_number = 2 ** (self.NUM_MENTISSA + 1)
                m3 -= overflow_number 
                m3 -= 2 ** (self.NUM_MENTISSA)
                # 지수를 한자리 올려준다
                e3 += 1
            # m3의 자리수를 다시 검사하여 가수와 지수를 정규화한다
            m3_digits = self.countDigits(m3)
            num_overflow_bits = m3_digits - (self.NUM_MENTISSA + 1) 
            m3 = m3 << abs(num_overflow_bits)
            e3 -= abs(num_overflow_bits)
            
        
        result = IEEE754_Float32("0.0")
        result.S = s3
        result.E = e3
        result.M = m3
        return result