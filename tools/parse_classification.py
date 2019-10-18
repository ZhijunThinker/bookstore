def parse_classification(classification):
    classification_form = {0: '未标记', 1: '玄幻', 2: '奇幻', 4: '武侠', 8: '仙侠', 16: '都市', 32: '现实', 64: '军事', 128: '历史',
                           256: '游戏', 512: '科幻', 1024: '悬疑', 2048: '轻小说', 4096: '古言', 8192: '现言', 16384: '青春',
                           32768: '幻情'}
    res = ''
    n = 32768
    if classification == 0:
        return classification[0]
    while n > 0:
        if classification & n == n:
            res += classification_form[n]
            classification ^= n
        else:
            n >>= 1
    return res