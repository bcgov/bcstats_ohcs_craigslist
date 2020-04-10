import unittest

# string tokenizer in C/C++ style, useful for parsing
def strtok(s, delim):
    j, s_len = -1, len(s)
    for i in range(0, s_len):
        if s[i] == delim:
            j = i
            break
    if j < 0:
        return [s, None]
    return[s[0: j], s[j + 1: ]]

# unit test for string tokenizer
class test_methods(unittest.TestCase):
    def test_strtok(self):
        s0 = "abc,def,ghi"
        s1, s0 = strtok(s0, ',')
        s2, s0 = strtok(s0, ',')
        s3, s0 = strtok(s0, ',')
        self.assertTrue(s1 == 'abc')
        self.assertTrue(s2 == 'def')
        self.assertTrue(s3 == 'ghi')

if __name__ == '__main__':
    unittest.main()