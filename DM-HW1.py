
EPSILON = 1e-10

def input_matrix():

    while True:
        try:
            n = int(input("정방행렬의 크기를 입력하세요 (1~4):"))

            if 1 <= n <= 4:
                break

            print("1 이상 4 이하의 정수를 입력해주세요.")

        except ValueError:
            print("정수를 입력해주세요.")

    matrix = []

    print(f"{n} x {n} 행렬의 원소를 입력해주세요.")
    print("각 행의 원소는 공백으로 구분해서 입력합니다.")
    print()

    for i in range(n):

        while True:
            try:
                row = list(
                    map(float, input(f"{i + 1}번째 행 입력: ").split())
                )

                if len(row) != n:
                    print(f"원소를 정확히 {n}개 입력해주세요.")
                    continue

                matrix.append(row)
                break

            except ValueError:
                print("숫자만 입력해주세요.")

    return matrix


def print_matrix(matrix, title=""):

    if title:
        print(title)

    for row in matrix:
        for value in row:

            if abs(value) < EPSILON:
                value = 0.0

            print(f"{value:10.4f}", end=" ")

        print()

    print()

def get_minor(matrix, remove_row, remove_col):

    minor = []

    for i in range(len(matrix)):

        if i == remove_row:
            continue

        row = []

        for j in range(len(matrix)):

            if j == remove_col:
                continue

            row.append(matrix[i][j])

        minor.append(row)

    return minor

def determinant(matrix):

    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:

        return (
            matrix[0][0] * matrix[1][1] 
              - matrix[0][1] * matrix[1][0]
        )

    if n == 3:
        return (
            matrix[0][0] * matrix[1][1] * matrix[2][2]
            + matrix[0][1] * matrix[1][2] * matrix[2][0]
            + matrix[0][2] * matrix[1][0] * matrix[2][1]
            - matrix[0][2] * matrix[1][1] * matrix[2][0]
            - matrix[0][0] * matrix[1][2] * matrix[2][1]
            - matrix[0][1] * matrix[1][0] * matrix[2][2]
        )

    det = 0

    for col in range(n):

        minor = get_minor(matrix, 0, col)

        det += (
            ((-1) ** col)
            * matrix[0][col]
            * determinant(minor)
        )

    return det

def inverse_by_determinant(matrix):

    n = len(matrix)

    print()
    print("==========================================")
    print(" [1] 행렬식을 이용한 역행렬 계산")
    print("==========================================")

    det = determinant(matrix)

    print(f"\ndet(A) = {det:.4f}")

    if abs(det) < EPSILON:

        print("\n행렬식이 0이므로 역행렬이 존재하지 않습니다.")

        return None

    if n == 1:

        inverse = [[1 / matrix[0][0]]]

        return inverse

    cofactor_matrix = []

    for i in range(n):
        row = []

        for j in range(n):
            minor = get_minor(matrix, i, j)
            minor_det = determinant(minor)
            row.append(((-1) ** (i + j)) * minor_det)

        cofactor_matrix.append(row)

    print()
    print_matrix(cofactor_matrix, "[여인수 행렬]")

    adjugate = [
        [cofactor_matrix[j][i] for j in range(n)]
        for i in range(n)
    ]
    print_matrix(adjugate, "[수반행렬]")

    return [
        [adjugate[i][j] / det for j in range(n)]
        for i in range(n)
    ]

def make_identity_matrix(n):

    identity = []

    for i in range(n):

        row = []

        for j in range(n):

            if i == j:
                row.append(1.0)

            else:
                row.append(0.0)

        identity.append(row)

    return identity

def print_augmented_matrix(augmented, n):

    for i in range(n):

        for j in range(n):

            value = augmented[i][j]

            if abs(value) < EPSILON:
                value = 0.0

            print(
                f"{value:9.4f}" ,
                end=""
            )

        print(" | ", end="")

        for j in range(n, 2 * n):

            value = augmented[i][j]

            if abs(value) < EPSILON:
                value = 0.0

            print(
                f"{value:9.4f}",
                end=""
            )

        print()

    print()


def inverse_by_gauss_jordan(matrix):
    n = len(matrix)

    print()
    print("==========================================")
    print(" [2] 가우스-조던 소거법")
    print("==========================================")

    identity = make_identity_matrix(n)
    augmented = [
        [float(value) for value in matrix[i]] + identity[i][:]
        for i in range(n)
    ]

    print("\n[초기 확대행렬 A | I]")
    print_augmented_matrix(augmented, n)

    step = 1

    for col in range(n):
        pivot_row = max(range(col, n), key=lambda row: abs(augmented[row][col]))

        if abs(augmented[pivot_row][col]) < EPSILON:
            print("\n0이 아닌 피벗을 찾을 수 없으므로 역행렬이 존재하지 않습니다.")
            return None

        if pivot_row != col:
            augmented[col], augmented[pivot_row] = (
                augmented[pivot_row],
                augmented[col],
            )
            print(f"[단계 {step}] R{col + 1} <-> R{pivot_row + 1}")
            print_augmented_matrix(augmented, n)
            step += 1

        pivot = augmented[col][col]
        for j in range(2 * n):
            augmented[col][j] /= pivot

        print(
            f"[단계 {step}] R{col + 1} <- R{col + 1} / ({pivot:.4f})"
        )
        print_augmented_matrix(augmented, n)
        step += 1

        for row in range(n):
            if row == col:
                continue

            factor = augmented[row][col]
            if abs(factor) < EPSILON:
                continue

            for j in range(2 * n):
                augmented[row][j] -= factor * augmented[col][j]

            print(
                f"[단계 {step}] R{row + 1} <- "
                f"R{row + 1} - ({factor:.4f}) x R{col + 1}"
            )
            print_augmented_matrix(augmented, n)
            step += 1

    inverse = [
        [augmented[i][j] for j in range(n, 2 * n)]
        for i in range(n)
    ]

    print("가우스-조던 소거가 완료되었습니다.")
    print("왼쪽 행렬이 단위행렬 I가 되었으므로 오른쪽 행렬이 A의 역행렬입니다.\n")
    return inverse


def compare_matrices(matrix1, matrix2, tolerance=1e-6):
    if matrix1 is None or matrix2 is None:
        return False

    if len(matrix1) != len(matrix2):
        return False

    return all(
        abs(matrix1[i][j] - matrix2[i][j]) <= tolerance
        for i in range(len(matrix1))
        for j in range(len(matrix1[i]))
    )


def main():
    print("===========================================")
    print(" [역행렬 계산 프로그램]")
    print("===========================================")
    print("정방행렬의 크기는 1~4까지 입력 가능합니다.")
    print()

    matrix = input_matrix()

    print()
    print_matrix(matrix, "[입력된 행렬 A]")

    det = determinant(matrix)
    print(f"입력된 행렬의 행렬식 det(A) = {det:.4f}")

    inverse_det = inverse_by_determinant(matrix)
    if inverse_det is not None:
        print()
        print_matrix(inverse_det, "[행렬식을 이용하여 계산한 역행렬]")

    inverse_gauss = inverse_by_gauss_jordan(matrix)
    if inverse_gauss is not None:
        print_matrix(inverse_gauss, "[가우스-조던 소거법으로 계산한 역행렬]")

    print("===========================================")
    print("[두 방법의 결과 비교]")
    print("===========================================")

    if inverse_det is None and inverse_gauss is None:
        print("두 방법 모두 역행렬이 존재하지 않는다고 판단했습니다.")
    elif inverse_det is None or inverse_gauss is None:
        print("두 방법의 결과가 다릅니다. 계산 과정을 확인해주세요.")
    elif compare_matrices(inverse_det, inverse_gauss):
        print("두 방법으로 계산한 역행렬이 동일합니다.")
    else:
        print("두 방법으로 계산한 역행렬이 서로 다릅니다.")


if __name__ == "__main__":
    main()