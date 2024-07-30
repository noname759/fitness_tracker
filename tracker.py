from datetime import datetime

CALORIES = 0.05
DISTANCE = 0.0008

storage_data = {}

def check_correct_data(packet):
    if len(packet) != 2:
        return False
    
    time_str, steps = packet
    
    if not time_str or not steps:
        return False
    
    try:
        datetime.strptime(time_str, "%H:%M:%S")
        steps = int(steps)
    except ValueError:
        return False
    
    if steps < 0:
        return False

    if time_str in storage_data:
        last_time = max(storage_data.keys())
        if time_str <= last_time:
            return False
    
    return True

def process_packet(packet):
    time_str, steps = packet
    storage_data[time_str] = int(steps)

def calculate_summary():
    total_steps = sum(storage_data.values())
    last_time = max(storage_data.keys(), default="00:00:00")

    total_distance = total_steps * DISTANCE
    total_calories = total_steps * CALORIES
    
    print("\nВремя:", last_time)
    print("Количество шагов за сегодня:", total_steps)
    print("Дистанция составила {:.2f} км.".format(total_distance))
    print("Вы сожгли {:.2f} ккал.".format(total_calories))
    
    if total_distance >= 6.5:
        print("Отличный результат! Цель достигнута.")
    elif total_distance >= 3.9:
        print("Неплохо! День был продуктивный.")
    elif total_distance >= 2:
        print("Завтра наверстаем!")
    else:
        print("Лежать тоже полезно. Главное участие, а не победа!")

def accept_package(packet):
    if check_correct_data(packet):
        process_packet(packet)
        calculate_summary()
    else:
        print("Неверные данные пакета")

def reset_data():
    global storage_data
    storage_data = {}
    print("Все данные были сброшены.")

if __name__ == "__main__":
    print("Программа для отслеживания шагов и расчёта калорий")
    
    while True:
        time_str = input("Введите время (в формате Час:Мин:Сек) или 'exit' для выхода: ")
        if time_str.lower() == 'exit':
            break
        
        steps = input("Введите количество шагов: ")
        
        packet = (time_str, steps)
        accept_package(packet)
    
    reset_data()
