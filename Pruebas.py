def find_user(users, target_id):
    for i in range(len(users)):
        for j in range(len(users)):
            if users[i]['id'] == target_id:
                return users[i]
    return None

def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates

def search_sorted_list(sorted_list, target):
    for item in sorted_list:
        if item == target:
            return True
    return False

def multiply_matrices(a, b):
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    result = []
    for i in range(rows_a):
        row = []
        for j in range(cols_b):
            total = 0
            for k in range(cols_a):
                total = total + a[i][k] * b[k][j]
            row.append(total)
        result.append(row)
    return result

def transpose(matrix):
    result = []
    for i in range(len(matrix[0])):
        row = []
        for j in range(len(matrix)):
            row.append(matrix[j][i])
        result.append(row)
    return result

def find_in_matrix(matrix, target):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == target:
                return (i, j)
    return None

def sort_users_by_age(users):
    for i in range(len(users)):
        for j in range(len(users) - 1):
            if users[j]['age'] > users[j + 1]['age']:
                temp = users[j]
                users[j] = users[j + 1]
                users[j + 1] = temp
    return users

def get_top_n(scores, n):
    sorted_scores = []
    for s in scores:
        sorted_scores.append(s)
    for i in range(len(sorted_scores)):
        for j in range(len(sorted_scores) - 1):
            if sorted_scores[j] < sorted_scores[j + 1]:
                temp = sorted_scores[j]
                sorted_scores[j] = sorted_scores[j + 1]
                sorted_scores[j + 1] = temp
    return sorted_scores[:n]

def is_sorted(arr):
    sorted_arr = []
    for item in arr:
        sorted_arr.append(item)
    for i in range(len(sorted_arr)):
        for j in range(len(sorted_arr) - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                temp = sorted_arr[j]
                sorted_arr[j] = sorted_arr[j + 1]
                sorted_arr[j + 1] = temp
    return arr == sorted_arr
