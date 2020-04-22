# string tokenizer in C/C++ style, useful for parsing
def strtok(s, delim):
    j, s_len = -1, len(s)
    for i in range(0, s_len):
        if s[i] == delim:
            j = i
            break
    if j < 0: return [s, None]
    return [s[0: j], s[j + 1: ]]
