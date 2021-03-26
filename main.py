import time

up_arrow = u'\u2191'
left_arrow = u'\u2190'
diag_arrow = u'\u2196'

dp_count = 0
dp_count_ed = 0
rec_count = 0
rec_count_ed = 0


def print_lcs(b, word_1, i, j):
    if i == 0 or j == 0:
        return
    if b[i][j] == diag_arrow:
        print_lcs(b, word_1, i - 1, j - 1)
        print(word_1[i - 1])
    elif b[i][j] == up_arrow:
        print_lcs(b, word_1, i - 1, j)
    else:
        print_lcs(b, word_1, i, j - 1)


def lcs_find_and_print(word_1, word_2):
    global dp_count
    m = len(word_1) + 1
    n = len(word_2) + 1

    c = [[0 for i in range(n)] for j in range(m)]  # stores count
    b = [[0 for i in range(n)] for j in range(m)]  # stores arrows

    for i in range(1, m):
        for j in range(1, n):
            # print('i, j:', i,  j)  # debug
            dp_count = dp_count + 1
            if word_1[i-1] == word_2[j-1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = diag_arrow
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = up_arrow
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = left_arrow
    print_lcs(b, word_1, i, j)

    # code for printing matrices:
    # for i in range(n):
    #      print(c[i])
    # print('-----')
    # for i in range(n):
    #      print(b[i])


def naive_lcs(word_1, word_2, m, n):
    global rec_count
    rec_count = rec_count + 1
    if m == 0 or n == 0:
        return 0
    elif word_1[m - 1] == word_2[n - 1]:
        return 1 + naive_lcs(word_1, word_2, m - 1, n - 1)
    else:
        return max(naive_lcs(word_1, word_2, m, n - 1), naive_lcs(word_1, word_2, m - 1, n))


def print_edit(b, word_1, word_2, i, j):
    if i == 0 or j == 0:
        return
    if b[i][j] == diag_arrow:
        print_edit(b, word_1, word_2, i - 1, j - 1)
        if not word_1[i - 1] == word_2[j - 1]:
            print("repl:", word_1[i - 1], ", ", word_2[j - 1])
        else:
            print(word_1[i - 1])
    elif b[i][j] == up_arrow:
        print_edit(b, word_1, word_2, i - 1, j)
        print("del:", word_1[i - 1])
    else:
        print_edit(b, word_1, word_2, i, j - 1)
        print("ins:", word_2[j - 1])


def edit_distance(word_1, word_2):
    # c_idr = 1
    global dp_count_ed
    m = len(word_1) + 1
    n = len(word_2) + 1
    distance = [[0 for i in range(n)] for j in range(m)]
    solution = [[0 for i in range(n)] for j in range(m)]

    # preparing the table:
    for i in range(1, m):
        distance[i][0] = i
        solution[i][0] = up_arrow
    for j in range(1, n):
        distance[0][j] = j
        solution[0][j] = left_arrow

    for i in range(1, m):
        for j in range(1, n):
            dp_count_ed = dp_count_ed + 1
            del_c = distance[i - 1][j] + 1
            ins_c = distance[i][j - 1] + 1
            if word_1[i - 1] == word_2[j - 1]:
                sub_c = distance[i - 1][j - 1] + 0
            else:
                sub_c = distance[i - 1][j - 1] + 1
            distance[i][j] = min(del_c, sub_c, ins_c)
            if distance[i][j] == del_c:
                solution[i][j] = up_arrow
            elif distance[i][j] == ins_c:
                solution[i][j] = left_arrow
            else:
                solution[i][j] = diag_arrow
    print_edit(solution, word_1, word_2, i, j)

    print("ed:")
    print("result:", distance[m-1][n-1])
    # code for printing matrices:
    # for i in range(m):
    #     print(distance[i])
    # print('-----')
    # for i in range(m):
    #     print(solution[i])


def naive_edit_distance(word_1, word_2, m, n):
    global rec_count_ed
    rec_count_ed = rec_count_ed + 1
    if m == 0:
        return n
    if n == 0:
        return m
    if word_1[m - 1] == word_2[n - 1]:
        return naive_edit_distance(word_1, word_2, m - 1, n - 1)

    return 1 + min(naive_edit_distance(word_1, word_2, m, n-1),  # ins, del, repl
                   naive_edit_distance(word_1, word_2, m - 1, n),
                   naive_edit_distance(word_1, word_2, m - 1, n - 1))


print("********* LONGEST COMMON SUBSEQUENCE *********")
x = ['ABCDGH', 'AGGTAB', 'ABCBDAB', 'XMJYAUZ', 'KATA', 'POTATO', 'TELEGRAM', 'WALKINGONTHESUN']
y = ['AEDFHR', 'GXTXAYB', 'BDCABA', 'MZJAWXU', 'TATRA', 'TOMATO', 'SIGNAL', 'SOMEBODYONCETOLDME']
a = 1
x = x[a]
y = y[a]
start = time.perf_counter_ns()
lcs_find_and_print(x, y)
stop = time.perf_counter_ns()
t_lcs_fap = stop - start
start = time.perf_counter_ns()
naive_lcs(x, y, len(x), len(y))
stop = time.perf_counter_ns()
print("DP time LCS:", t_lcs_fap, "ns | REC LCS:", stop - start, "ns")
print("dp count:", dp_count, "| rec count:", rec_count)

print("********* EDIT DISTANCE *********")
x = ['INTENTION', 'SUNDAY', 'CART', 'QUARANTINE', 'KATA', 'MAMMA', 'INDECISIVE', 'QUACK']
y = ['EXECUTION', 'SATURDAY', 'MERCH', 'RUNTIME', 'TATRA', 'MIA', 'INVASIVE', 'QUAKE']
a = 7
x = x[a]
y = y[a]
start = time.perf_counter_ns()
edit_distance(x, y)
stop = time.perf_counter_ns()
t_lcs_fap = stop - start
start = time.perf_counter_ns()
naive_edit_distance(x, y, len(x), len(y))
stop = time.perf_counter_ns()
print("DP time ED:", t_lcs_fap, "ns | REC LCS:", stop - start, "ns")
print("dp count:", dp_count_ed, "| rec count:", rec_count_ed)
