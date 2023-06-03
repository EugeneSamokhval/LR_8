import copy
import random


class DiagonalRep:
    def __init__(self, normal: list):
        diagonal = [[0 for row in range(16)] for column in range(16)]
        step = 0
        for column in range(16):
            row = 0
            while row + step < 16:
                diagonal[row + step][column] = normal[column][row]
                row += 1
            row = 0
            while row < step:
                diagonal[row][column] = normal[column][row]
                row+=1
            step += 1
        self.table = diagonal
        self.current_element = [0, 0]

    def unpack_element(self, position: int):
        unpacked = []
        for signs in range(position, 16):
            unpacked.append(self.table[signs][position])
        for signs in range(0, position):
            unpacked.append(self.table[signs][position])
        return unpacked

    def delete_column(self, position: int):
        copy_of_deletable = self.unpack_element(position)
        for signs in range(position, 16):
            self.table[signs][position] = None
        for signs in range(0, position):
            self.table[signs][position] = None
        return copy_of_deletable

    def overwrite(self, position: int, content: list):
        content_counter = 0
        for signs in range(position, 16):
            self.table[signs][position] = content[content_counter]
            content_counter+=1
        for signs in range(0, position):
            self.table[signs][position] = content[content_counter]
            content_counter += 1

    def not_first(self, index_of_x1):
        result = []
        x1 = copy.deepcopy(self.unpack_element(index_of_x1))
        for logic_var in range(len(x1)):
            if x1[logic_var] == 1:
                result.append(0)
            else:
                result.append(1)
        return result

    def constant_zero(self):
        return [0 for digit in range(16)]

    def constant_one(self):
        return [1 for digit in range(16)]

    def search(self, search_request):
        maximal = [0, 0]
        for index in range(0, 16):
            current_word = self.unpack_element(index)
            current_amount_of_equals = max_equivalence(search_request, current_word)
            if maximal[0] < current_amount_of_equals:
                maximal = [current_amount_of_equals, index]
        return maximal

    def arif_operation(self, search_input):
        result = []
        current_word = []
        for index in range(16):
            current_word = self.unpack_element(index)
            if current_word[0] == search_input[0] and current_word[1] == search_input[1] and\
                    current_word[2] == search_input[2]:
                current_word = binary_sum(current_word)
                result.append(current_word)
                self.overwrite(index, current_word)
        return result

    def view(self):
        array_to_show = []
        for index in range(16):
            array_to_show.append(self.unpack_element(index))
            print(self.unpack_element(index))
        return array_to_show, self.table


def binary_sum(current_word: list):
    memory = 0
    bin_index = 15
    while bin_index > 11:
        if (current_word[bin_index-5] == 1 and current_word[bin_index-9] == 1 and memory == 0) or\
                (current_word[bin_index-5] == 0 and current_word[bin_index-9] == 1 and memory == 1) or\
                (current_word[bin_index-5] == 1 and current_word[bin_index-9] == 0 and memory == 1):
            current_word[bin_index] = 0
            memory = 1
        elif (current_word[bin_index-5] == 0 and current_word[bin_index-9] == 1 and memory == 0) or\
                (current_word[bin_index-5] == 1 and current_word[bin_index-9] == 0 and memory == 0) or\
                (current_word[bin_index-5] == 0 and current_word[bin_index-9] == 0 and memory == 1):
            memory = 0
            current_word[bin_index] = 1
        elif current_word[bin_index-5] == 1 and current_word[bin_index-9] == 1 and memory == 1:
            current_word[bin_index] = 1
            memory = 1
        elif current_word[bin_index-5] == 0 and current_word[bin_index-9] == 0 and memory == 0:
            current_word[bin_index] = 0
        bin_index -= 1
        if memory == 1:
            current_word[11] = 1
    return current_word


def random_words_generator():
    final_form = []
    for index in range(16):
        final_form.append([random.randrange(2) for subindex in range(16)])
    return final_form


def max_equivalence(key, comparable):
    counter = 0
    max_sign = min(len(key), len(comparable))
    for sign in range(max_sign):
        if key[sign] == comparable[sign]:
            counter+=1
    return counter


def main():
    user_input = ''
    search_location = random_words_generator()
    diagonal_form = DiagonalRep(search_location)
    while user_input != 'exit':
        user_input = input('Commands:\n search\nprint on index\nshow\ndelete\nnot\nconst 0\nconst 1\narif operation\n')
        match user_input:
            case 'search':
                user_input = input('\nInput search key\n')
                input_key = user_input.split(' ')
                input_key = [int(input_key[index]) for index in range(16)]
                print(diagonal_form.search(input_key))
            case 'print on index':
                user_input = int(input('Input index'))
                if user_input< 16:
                    print(diagonal_form.unpack_element(user_input))
                else:
                    print('Index out of range')
            case 'show':
                for line in diagonal_form.table:
                    print(line, end='\n')
            case 'delete':
                user_input = int(input('Input index'))
                print(diagonal_form.delete_column(user_input))
            case 'not':
                user_input = int(input('Input index'))
                print(diagonal_form.not_first(user_input))
            case 'const 0':
                print(diagonal_form.constant_zero())
            case 'const 1':
                print(diagonal_form.constant_one())
            case 'arif operation':
                user_input = input('\nInput search key\n')
                input_key = user_input.split(' ')
                input_key = [int(input_key[index]) for index in range(3)]
                print(diagonal_form.arif_operation(input_key))


if __name__ == '__main__':
    main()
