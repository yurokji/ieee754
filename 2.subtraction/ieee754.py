# 덧셈의 부호에 따른 타입
PLUS_PLUS = 0
PLUS_MINUS = 1
MINUS_PLUS = 2
MINUS_MINUS = 3


class IEEE754_Float:
    def __init__(self, strFloat, precision="single"):
        # 64비트 부동소수(배정밀도)
        if precision=="double":
            self.precision = precision
            self.size = 64
            self.NUM_EXP = 11
        # 128비트 부동소수(4배정밀도)
        elif precision=="quad":
            self.precision = precision
            self.size = 128
            self.NUM_EXP = 15
        else:
            self.precision = precision
            self.size = 32
            self.NUM_EXP = 8
        
        self.BIAS = 2 ** (self.NUM_EXP - 1) - 1
        # print(self.BIAS)
        self.NUM_MENTISSA = self.size - self.NUM_EXP - 1
        print(self.size, self.NUM_EXP, self.NUM_MENTISSA)
        # 문자열을 고정소수점 실수로 변환
        sg, numStr, pointStr = self.decimalPointStr2FixedPointStr(strFloat) 
        # 고정소수점 실수를 부동소수로 변환
        self.S, self.E, self.M = self.convIEEE754Format(sg, numStr, pointStr)



    # 문자열을 고정소수점 실수로 변환
    def decimalPointStr2FixedPointStr(self, strFloat):
        # 문자열을 나눔
        sign_str, num_str, point_str = self.strSplit(strFloat)
        # 문자열을 고정소수점 실수중 소수 위자리수로 변환
        num_str = self.convDecimalNum2BinStr(num_str)
        # 문자열을 고정소수점 실수중 소수 아래자리수로 변환
        point_str = self.convDecimalPoint2BinStr(point_str)
        return sign_str, num_str, point_str

    # 2진수 고정 소수점 출력
    def printFixedBinNum(self, strFloat):
        sign_str, numStr, pointStr =  self.decimalPointStr2FixedPointStr(strFloat)
        print("10진수            실수:", strFloat)
        print(" 2진수 고정수수점 실수:", sign_str+numStr+"."+pointStr)


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
        point = 0
        if exp >= 0:
            point_mask = (2 ** self.NUM_MENTISSA) - 1
            point_mask = point_mask >> exp
            point = (self.M & point_mask) << exp
        else:
            point = mentissa >> abs(exp)
        # 고정 소수점을 10진수 소수점으로 바꿔줌
        point = self.convBinPoint2DecimalPoint(point)
        res += str(num)
        res += "."
        res += str(point)
        return res

    def toHex(self):
        S = self.S
        E = self.E
        M = self.M
        # print(S, E, M)
        binNumber = S << (self.NUM_EXP + self.NUM_MENTISSA) | E << self.NUM_MENTISSA | M
        return hex(binNumber)

    # 10진수 자리수를 카운트함
    def countDecimalDigits(self, val):
        count = 1
        while True:
            # 2자리 이상이라면
            if val // 10 > 0:
                val //= 10
                count += 1
            else:
                break
        return count



    # 문자열을 분리함
    def strSplit(self, str):
        # "."을 기준으로 나눔
        num, point = str.split(".")
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
    def convDecimalNum2BinStr(self, inputStr):
        share = int(inputStr)
        if share == 0:
            return "0"
        
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
    def convDecimalPoint2BinStr(self, inputStr):
        MAX_DIGITS = self.size
        # 0034985  7개
        string_length = len(inputStr)
        num = int(inputStr)
        # 10진수 자리수를 체크
        #  34985 5개
        tenth_digits = self.countDecimalDigits(num)
        # 2개 차이
        diff = string_length - tenth_digits
        resultStr = ""
        curr_bit =""
        for i in range(MAX_DIGITS):
            num *= 2
            digits = self.countDecimalDigits(num)
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
        # 바이어스를 더해줌
        E = self.BIAS + e
        point = num[1:] + point
       
        M = point[:self.NUM_MENTISSA]
        M = int(M,2) 
        # # 이진수 1101.000101101......같은 경우
        # # 소수점 000101101...은 자리수가 가수부 크기보다 작으므로
        # # 자리수 차이를 비교하여 
        # # 가수부를 올려주고 그만큼 지수에서 빼준다
        # # 결과: 101101......
        digits = self.countDigits(M)
        diff = self.NUM_MENTISSA - digits
        M = M << diff
        E -= diff
        
        # # 위의 계산은 1.M을 전제한 것임
        # # 즉, 1.을 만족하려면 num이 최소한 1이상되어야 함
        # # 그러나 num=0이라면 0.M이 됨
        # # 이대로는 정규화가 안된 상태
        # # 1.0을 붙여주기 위해
        # # 소수점 위가 0이라면
        # # M의 가장 상위비트를 0으로 만들어줍니다
        # # 그리고 E를 1뺀다
        if num == "0":
            M -= 2 ** (self.NUM_MENTISSA - 1)
            E -= 1
        # 라운딩
        if point[self.NUM_MENTISSA] == "1":
            M += 1
        return S, E, M

    # 2진수 고정 소수점을 10진수 소수점으로 변환
    def convBinPoint2DecimalPoint(self, value):
        bin_point = value
        digits = self.countDigits(value)
        # 자리수의 차이를 계산한다
        diff = self.NUM_MENTISSA - digits

        # 2진수 고정 소수 첫재짜리가 500000000~
        # 2진수 고정 소수 둘재짜리가 250000000~
        # 10진수로 표기할 자리수
        ten_digits = 30
        multiplier = 500000000000000000000000000000
        multiplier //= (2 ** diff)
        result = 0
        count = 0
        while True:
            shift_size = (self.NUM_MENTISSA - diff - 1) - count
            if shift_size > 0:
                result += ((bin_point >> shift_size) & 1) * (multiplier // (2 ** count))
                count += 1
            else:
                break
        result = str(result)
        # 10진수로 0의 자리수를 맞춰준다
        result = result.zfill(ten_digits)
        # 쓸모없는 뒷자리 00000을 지우기 위한 후처리 
        # 소수점 끄트머리의 0을 모두 지운다
        result = result[::-1]
        result = str(int(result))[::-1]
        return result


    # 정수에서 2진수로 자릿수를 계산한다
    def countDigits(self, value):
        count = 0
        while True:
            temp = (value >> count)
            # 자리수가 한자리인 경우
            if temp == 0 or temp == 1:
                count += 1
                break
            else:
                count += 1
        return count


    # 부동 소수 덧셈 연산자
    def __add__(self, other):

        s1 = self.S
        s2 = other.S
        e1 = self.E
        e2 = other.E
        m1 = self.M
        m2 = other.M

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

        s3 = s1
        e3 = e1
 

        add_type = PLUS_PLUS
        if s1 == 0 and s2 == 1:
            add_type = PLUS_MINUS
        elif s1 == 1 and s2 == 0:
            add_type = MINUS_PLUS
        elif s1 == 1 and s2 == 1:
            add_type = MINUS_MINUS


        # 덧셈의 부호가 서로 다를때 전처리하는 부분
        # 지수가 큰쪽이나
        # 지수가 같을 경우 가수부를 비교하는 식으로
        # 두수의 절대 크기를 비교한다
     
        # 계산의 부호는 절대 크기가 큰쪽을 따르기 때문에
        # 결과값을 저장할 부동소수의 부호는 
        # 절대크기가 큰 쪽의 부동소수를 따른다
        # 뒤에 있는 수가 음수일 경우
        if add_type == PLUS_MINUS:
            if self.compare(other):
                s3 = s1
            else:
                s3 = s2
            # 뒤에 있는 수를 2의 보수를 취해 음수로 만든후
            # 두 수를 더한다
            m3 = m1 + self.negate(m2)
            # 원래 가수부의 크기를 비교해서
            # 뒤에 있는 수의 가수가 더 크면
            # 결과값이 2의 보수가 나오므로
            # 그 값을 다시 2의 보수를 취해
            # 정상적인 값으로 복원한다
            # ieee754에서 부호는 sign_bit로만 구분하기 때문에
            if m1 < m2:
                m3 = self.negate(m3)

        # 앞에 있는 수가 음수일 경우
        elif add_type == MINUS_PLUS:
            if self.compare(other):
                s3 = s1
            else:
                s3 = s2
            # 앞에 있는 수를 2의 보수를 취해 음수로 만든후
            # 두 수를 더한다
            m3 = self.negate(m1) + m2
            # 원래 가수부의 크기를 비교해서
            # 앞에 있는 수의 가수가 더 크면
            # 결과값이 2의 보수가 나오므로
            # 그 값을 다시 2의 보수를 취해
            # 정상적인 값으로 복원한다
            # ieee754에서 부호는 sign_bit로만 구분하기 때문에
            if m1 > m2:
                m3 = self.negate(m3)            

        # 음수끼리 덧셈하는 경우
        elif add_type == MINUS_MINUS:  
            s3 = 1
            m3 = m1 + m2

        # 양수끼리 덧셈하는 경우
        else:
            m3 = m1 + m2

        # 계산의 결과 정규화
        # 뺄셈에 해당하는 덧셈의 경우
        # 즉, 두 두호가 다른 덧셈의 결과를 정규화
        if add_type == PLUS_MINUS or add_type == MINUS_PLUS:
            m3_digits = self.countDigits(m3)
            # 뺄셈의 결과로 오버플로를 확인
            num_overflow_bits = m3_digits - (self.NUM_MENTISSA + 1)
            # 먼저 뺄셈의 결과로 오버플로가 없는 경우
            # 계산 결과가 0.M의 형태가 나왔을 때
            if num_overflow_bits < 0:
                # 0.~~M형태이므로 
                # 1.M형태로 변환해주기 위해 가수를 쉬프트해서 올려줌
                m3 = m3 << abs(num_overflow_bits)
                # M의 자리를 올려준만큼 반대로 지수를 빼줌
                e3 -= abs(num_overflow_bits)
                # 1.M에서 M만 남기기 위해 1.을 빼주는 연산을 수행
                m3 -= 2 ** (self.NUM_MENTISSA) 
            # 계산 결과에서 오버플로가 발생
            elif num_overflow_bits > 0:
                # 뺄셈의 결과에서 오버플로는 무시해야 함
                # 따라서 가수에서 오버플로를 제거하기위해
                # 오버플로된 자리는 2^mentissa에 있는 1을 빼줌
                overflow_number = 2 ** (self.NUM_MENTISSA + 1)
                m3 -= overflow_number
                # 그리고나서 나머지 가수의 자리수를 다시 계산
                # 가수 유효자리수에서 실제 자리수가
                # 얼마나 모자라는지 다시 계산한 후
                # 가수를 쉬프트해서 올려주고
                # 그만큼 지수에서 다시 빼줌
                m3_digits = self.countDigits(m3)
                digits = m3_digits - (self.NUM_MENTISSA + 1)
                m3 = m3 << abs(digits)
                e3 -= abs(digits)


        # 두 부호가 같은 덧셈의 결과를 정규화
        else:
            # 가수의 모든 자리수가 1로 채워지는, 가장 큰수
            # 11111111111111111111111111
            max_mentissa = 2 ** (self.NUM_MENTISSA + 1) - 1
            # max_mentissa를 넘기면 오버플로우로 간주
            if m3 > max_mentissa:
                # 자리수 유지
                m3 = m3 >> 1
                # 지수를 한자리 올려줌
                e3 += 1
            # 덧셈하기 위해 더해준 1. 비트를 삭제하기 위해
            # 2^mentissa승만큼 빼준다
            m3 -= 2 ** (self.NUM_MENTISSA)

        
        result = IEEE754_Float("0.0", precision=self.precision)
        result.S = s3
        result.E = e3
        result.M = m3
        return result



    # 부동 소수 뺄셈 연산자
    def __sub__(self, other):
        a = self
        b = other
        # 뺄셈을 다른 부호의 덧셈으로 변환한다
        # (+a) - (+b) ==> (+a) + (-b)
        if self.S == 0 and other.S == 0:
            a.S = 0
            b.S = 1   
        # (+a) - (-b) ==> (+a) + (+b)
        elif self.S == 0 and other.S == 1:
            a.S = 0
            b.S = 0           
        # (-a) - (+b) ==> (-a) + (-b)
        elif self.S == 1 and other.S == 0:
            a.S = 1
            b.S = 1   
        # (-a) - (-b) ==> (-a) + (+b)
        else:
            a.S = 1
            b.S = 0   

        return a+b


    # 두수의 크기를 비교한다
    def compare(self, other):
        e1 = self.E
        e2 = other.E
        m1 = self.M
        m2 = other.M
        # 지수의 차이를 우선 비교
        diff_e = e1 - e2
        if diff_e > 0:
            return True
        elif diff_e < 0:
            return False
        # 지수의 차이가 없다면
        # 가수를 비교한다
        else:
            if m1 > m2:
                return True
            else:
                return False

    
    # 2의 보수 (음수)를 취해주는 함수
    def negate(self, val):
        # 마스크비트를 val의 자리수만큼(가수부 자리수)
        # 1로 채운 후
        mask  = 2 ** (self.NUM_MENTISSA + 1) - 1
        # val과 xor 연산을 취하면
        # 1의 보수가 된다
        res = val ^ mask
        # 그 결과에 1을 더하면
        # 2의 보수가 된다
        res += 1
        return res


            




        

        





    
