import queue
import re
from ptrlib import Socket

sock = Socket('35.221.81.216', 65532)
sock.recvuntil("Choice: ")
cnt = 0

def query(intervals):
    global cnt
    conditions = []
    for left, right in intervals:
        conditions.append(f'({left} <= N && N < {right})')
    conditions_txt = ' || '.join(conditions)
    program = f'({conditions_txt}) ? N % 10 : 100'
    sock.send(b'1\n')
    sock.send(program + '\n')
    data = sock.recvuntil("cases.").decode()
    cnt += 1
    print(cnt)
    num = int(re.search(r'(\d+) test', data).group(1))
    return num


def find_numbers():
    que = queue.SimpleQueue()
    singles = queue.SimpleQueue()
    que.put((0, 2**32, 50))

    while not que.empty():
        (left, right, size) = que.get_nowait()
        middle = (left + right) // 2
        left_size = query([(left, middle)])
        right_size = size - left_size
        if left_size == 1:
            singles.put_nowait((left, middle))
        elif left_size != 0:
            que.put_nowait((left, middle, left_size))
        if right_size == 1:
            singles.put_nowait((middle, right))
        elif right_size != 0:
            que.put_nowait((middle, right, right_size))

    answer = []

    # True if left
    def determine(left, right):
        def push_interval(left, right):
            if right - left <= 1:
                answer.append(left)
            else:
                singles.put_nowait((left, right))

        middle = (left + right) // 2
        in_left = None
        if singles.empty():
            in_left = query([(left, middle)]) == 1
        else:
            (left2, right2) = singles.get_nowait()
            middle2 = (left2 + right2) // 2
            lefts = query([(left, middle), (left2, middle2)])
            if lefts == 2:
                in_left = True
                push_interval(left2, middle2)
            elif lefts == 0:
                in_left = False
                push_interval(middle2, right2)
            else:
                in_left = not determine(left2, right2)

        (new_left, new_right) = (left, middle) if in_left else (middle, right)
        push_interval(new_left, new_right)
        return in_left

    while not singles.empty():
        (left, right) = singles.get_nowait()
        # print(left, right)
        determine(left, right)

    return answer


def main():
    answer = find_numbers()
    print(f"answer: {answer}")
    sock.send(b'2\n')
    sock.send(' '.join(map(str, answer)) + '\n')
    while True:
        data = sock.recvline().decode()
        print(data)


if __name__ == '__main__':
    main()
