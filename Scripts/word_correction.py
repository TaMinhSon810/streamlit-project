import streamlit as st


def lavenshtein_distance(source, target):
    # Tạo ma trận lưu trữ
    len_source = len(source)
    len_target = len(target)

    D = [[0] * (len_target + 1) for _ in range(len_source + 1)]

    # Tạo hàng và cột đầu tiên
    for i in range(len_source + 1):
        D[i][0] = i

    for j in range(len_target + 1):
        D[0][j] = j

    # Tính toán các ô trong ma trận
    del_cost = 0
    ins_cost = 0
    sub_cost = 0

    for i in range(1, len_source + 1):
        for j in range(1, len_target + 1):
            if source[i - 1] == target[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                del_cost = D[i - 1][j]  # Xét ô bên trên
                ins_cost = D[i][j - 1]  # Xét ô bên trái
                sub_cost = D[i - 1][j - 1]  # Xét ô chéo

                D[i][j] = min(del_cost, ins_cost, sub_cost) + 1

    return D[len_source][len_target]


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted([line.strip().lower() for line in lines])

    return words


vocabs = load_vocab('./data/vocab.txt')


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Your word:')

    leven_distances = dict()
    if st.button("Compute"):
        for vocab in vocabs:
            distance = lavenshtein_distance(word, vocab)
            leven_distances[vocab] = distance

        sorted_distances = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))
        corrected_word = list(sorted_distances.keys())[0]
        st.write('Correct: ', corrected_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distances)


if __name__ == "__main__":
    main()
