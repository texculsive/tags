from random import shuffle
from tkinter import Canvas, Tk

BOARD_SIZE = 4
SQUARE_SIZE = 80
EMPTY_SQUARE = BOARD_SIZE ** 2

root = Tk()
root.title("Pythonicway Fifteen")

c = Canvas(root, width=BOARD_SIZE * SQUARE_SIZE,
           height=BOARD_SIZE * SQUARE_SIZE, bg='#808080')
c.pack()


def get_inv_count():
    """ Функція, яка вважає кількість переміщень """
    inversions = 0
    inversion_board = board[:]
    inversion_board.remove(EMPTY_SQUARE)
    for i in range(len(inversion_board)):
        first_item = inversion_board[i]
        for j in range(i+1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions


def is_solvable():
    """ Функція визначальна чи має головоломка """
    num_inversions = get_inv_count()
    if BOARD_SIZE % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = BOARD_SIZE - (board.index(EMPTY_SQUARE) // BOARD_SIZE)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0


def get_empty_neighbor(index):
    # отримуємо індекс порожньої клітини у списку
    empty_index = board.index(EMPTY_SQUARE)
    # дізнаємося відстань від порожньої клітини до клітини якою клікнули
    abs_value = abs(empty_index - index)
    # Якщо порожня клітка над або під клектою, на яку клікнули
    # повертаємо індекс порожньої клітини
    if abs_value == BOARD_SIZE:
        return empty_index
    # Якщо порожня клітина ліворуч чи праворуч
    elif abs_value == 1:
        # Перевіряємо, щоб блоки були в одному ряді
        max_index = max(index, empty_index)
        if max_index % BOARD_SIZE != 0:
            return empty_index
    # Поруч із блоком не було порожнього поля
    return index


def draw_board():
    # прибираємо все, що намальовано на полотні
    c.delete('all')
    # Наше завдання згрупувати цятки зі списку в квадрат
    # зі сторонами BOARD_SIZE x BOARD_SIZE
    # i та j будуть координатами для кожної окремої цятки
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # отримуємо значення, яке ми маємо намалювати 
            # на квадраті
            index = str(board[BOARD_SIZE * i + j])
            # якщо це не клітина, яку ми хочемо залишити порожньою
            if index != str(EMPTY_SQUARE):
                # малюємо квадрат за заданими координатами
                c.create_rectangle(j * SQUARE_SIZE, i * SQUARE_SIZE,
                                   j * SQUARE_SIZE + SQUARE_SIZE,
                                   i * SQUARE_SIZE + SQUARE_SIZE,
                                   fill='#43ABC9',
                                   outline='#FFFFFF')
                # пишемо число у центрі квадрата
                c.create_text(j * SQUARE_SIZE + SQUARE_SIZE / 2,
                              i * SQUARE_SIZE + SQUARE_SIZE / 2,
                              text=index,
                              font="Arial {} italic".format(int(SQUARE_SIZE / 4)),
                              fill='#FFFFFF')


def show_victory_plate():
    # Малюємо чорний квадрат по центру поля
    c.create_rectangle(SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 - 10 * BOARD_SIZE,
                       BOARD_SIZE * SQUARE_SIZE - SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 + 10 * BOARD_SIZE,
                       fill='#000000',
                       outline='#FFFFFF')
    # Пишемо червоним текст Перемога
    c.create_text(SQUARE_SIZE * BOARD_SIZE / 2, SQUARE_SIZE * BOARD_SIZE / 1.9,
                  text="ПОБЕДА!", font="Helvetica {} bold".format(int(10 * BOARD_SIZE)), fill='#DC143C')


def click(event):
    # Отримуємо координати кліка
    x, y = event.x, event.y
    # Конвертуємо координати з пікселів у клітини
    x = x // SQUARE_SIZE
    y = y // SQUARE_SIZE
    # Отримуємо індекс у списку об'єкта за яким ми натиснули
    board_index = x + (y * BOARD_SIZE)
    # Отримуємо індекс порожньої клітки у списку. Цю функцію ми напишемо пізніше
    empty_index = get_empty_neighbor(board_index)
    # Змінюємо місцями порожню клітку і клітку, якою клікнули
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    # Перемальовуємо ігрове поле
    draw_board()
    # Якщо поточний стан дошки відповідає правильному – малюємо повідомлення про перемогу
    if board == correct_board:
        # Цю функцію ми додамо пізніше
        show_victory_plate()


c.bind('<Button-1>', click)
c.pack()


board = list(range(1, EMPTY_SQUARE + 1))
correct_board = board[:]
shuffle(board)

while not is_solvable():
    shuffle(board)

draw_board()
root.mainloop()
