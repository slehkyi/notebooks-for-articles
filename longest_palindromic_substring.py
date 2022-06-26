class Solution:
    def longest_palindrome(self, s):
        if s == s[::-1]:
            return s
        max_len = 2
        winners = []
        for i in range(len(s)):
            for ln in range(i+1, len(s)+1):
                ss = s[i:ln]
                if ss == ss[::-1]:
                    if len(ss) >= max_len:
                        max_len = len(ss)
                        winners.append(ss)

        winners = [x for x in winners if len(x) == max_len]

        return winners

st = "aamamamnaa"
print(Solution().longest_palindrome(st))

