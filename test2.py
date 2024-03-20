class PrimeNumbers:
    def __init__(self, n):
        self.n = n
    
    def __iter__(self):
        self.cur_num = 2
        return self
    
    def __next__(self):
        while True:
            if self.is_prime(self.cur_num):
                prime = self.cur_num
                if prime <= n:
                    self.cur_num += 1
                    return prime
                else:
                    raise StopIteration
            else:
                self.cur_num += 1

    def is_prime(self, number):
        ok = True
        for i in range(2, int(self.cur_num**0.5)+1):
            if self.cur_num % i == 0:
                return False
        return True

n = int(input())
prime_number_iterator = PrimeNumbers(n)
for num in prime_number_iterator:
    print(num)