
A = [1, 2, 3, 4, 5]

def read_matrix():
    size = len(A)
    matrix = []
    print("각 행에 0 또는 1을 다섯 개씩 공백으로 구분해 입력하세요.")
    while len(matrix) < size:
        values = input(f"{len(matrix)+1}행:").split()
        if len(values) != size or any(value not in ("0", "1") for value in values):
            print(f"입력 오류: 0 또는 1을 다섯 개 입력해야 합니다.")
            continue
        matrix.append([int(value) for value in values])
    return matrix

def reflexive_failure(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            return i
    return None

def symmetric_failure(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1 and matrix[j][i] == 0:
                return i, j
    return None

def transitive_failure(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                if matrix[i][j] and matrix[j][k] and not matrix[i][k]:
                    return i, j, k
    return None

def is_reflexive(matrix):
    return reflexive_failure(matrix) is None

def is_symmetric(matrix):
    return symmetric_failure(matrix) is None

def is_transitive(matrix):
    return transitive_failure(matrix) is None

def equivalance_class(matrix, element):
    row = matrix[A.index(element)]
    return [value for value, related in zip(A, row) if related]

def reflexive_closure(matrix):
    result = [row[:] for row in matrix]
    for i in range(len(result)):
        result[i][i] = 1
    return result

def symmetric_closure(matrix):
    result = [row[:] for row in matrix]
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            related = matrix[i][j] | matrix[j][i]
            result[i][j] = related
            result[j][i] = related
    return result

def transitive_closure(matrix):
    result = [row[:] for row in matrix]
    size = len(result)

    for k in range(size):
        for i in range(size):
            for j in range(size):
                if result[i][k] and result[k][j]:
                    result[i][j] = 1
    return result

def print_matrix(matrix):
    print("   " + " ".join(str(i) for i in A))
    for value, row in zip(A, matrix):
        print(f"{value} | " + " ".join(map(str, row)))

def print_failure_examples(matrix):
    i = reflexive_failure(matrix)
    if i is not None:
        print(f"- 반사 위반:({A[i]}, {A[i]})이 관계에 없습니다.")

    pair = symmetric_failure(matrix)
    if pair is not None:
        i, j = pair
        print(f"- 대칭 위반: ({A[i]}, {A[j]})은 있지만 ({A[j]}, {A[i]})은 없습니다.")
    triple = transitive_failure(matrix)
    if triple is not None:
        i, j, k = triple
        print(
            f"- 추이 위반: ({A[i]}, {A[j]})와 ({A[j]}, {A[k]})은 있지만"
            f"({A[i]}, {A[k]})은 없습니다."
        )

def print_analysis(matrix):
    reflexive = is_reflexive(matrix)
    symmetric = is_symmetric(matrix)
    transitive = is_transitive(matrix)

    print(f"반사: {'만족' if reflexive else '불만족'}")
    print(f"대칭: {'만족' if symmetric else '불만족'}")
    print(f"추이: {'만족' if transitive else '불만족'}")

    if reflexive and symmetric and transitive:
        print("동치 관계입니다")
        for element in A:
            members = ", ".join(map(str, equivalance_class(matrix, element)))
            print(f"[{element}] = {{{members}}}")

    else:
        print("동치 관계가 아닙니다.")
        print_failure_examples(matrix)

def show_closure(name, before, after):
    print(f"\n=== {name} ===")
    print("변환 전")
    print_matrix(before)
    print("변환 후")
    print_matrix(after)
    print_analysis(after)

def main():
    matrix = read_matrix()
    print("\n=== 입력 관계 ===")
    print_matrix(matrix)
    print_analysis(matrix)

    closures = (
        ("반사 폐포", is_reflexive, reflexive_closure),
        ("대칭 폐포", is_symmetric, symmetric_closure),
        ("추이 폐포", is_transitive, transitive_closure),
    )
    for name, satisfies, make_closure in closures:
        if not satisfies(matrix):
            show_closure(name, matrix, make_closure(matrix))

    if not (is_reflexive(matrix) and is_symmetric(matrix) and is_transitive(matrix)):
        result = reflexive_closure(matrix)
        result = symmetric_closure(result)
        result = transitive_closure(result)
        show_closure("동치 폐포", matrix, result)

if __name__ == "__main__":
    main()

