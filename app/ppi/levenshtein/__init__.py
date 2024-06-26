# from PyLog.logger import Logger

# logger = Logger()

def init_dp(x: int, y: int) -> list[int]:
    dp = [[0] * (x + 1) for _ in range(y + 1)]
    for i in range(y + 1): dp[i][0] = i
    for j in range(x + 1): dp[0][j] = j
    return dp

def lev(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = init_dp(n, m)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[m][n]


def test_lev() -> bool:
    with open('big_ass_words.txt', 'r') as words:
        split = words.read().split('\n')
        longest_word_ever = split[0]
        longest_german_word = split[1]
    test_cases = [
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("saturday", "sunday", 3),
        ("hello", "world", 4),
        ("", "abc", 3),
        ("abc", "", 3),
        ("", "", 0),
        ("abcdef", "ghijklmno", 9),
        (longest_word_ever, longest_german_word, 65761)
    ]
    failed = False
    for i, (str1, str2, expected_distance) in enumerate(test_cases):
        distance = lev(str1, str2)
        if distance == expected_distance:
            pass
            # logger.info(f"Test {i + 1}: Passed ✅")
        else:
            # logger.warning(f"Test case {i + 1}: Failed ❌. Expected {expected_distance}, got {distance}.")
            failed = True
    return failed


# if __name__ == '__main__':
#     if test_lev():
#         logger.error('Not all the tests have passed!')
#     else:
#         logger.info('All tests passed successfully!')