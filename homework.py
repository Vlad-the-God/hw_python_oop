class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration,
                 distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def show_training_info(self):
        return self.get_message()


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()

        return InfoMessage(training_type, duration,
                           distance, mean_speed,
                           spent_calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035  # Для множителя веса спортсмена
    K_2 = 0.029  # Для множителя
    KMH_TO_MS = 0.278  # для перевода значений из км/ч в м/с
    M_TO_SM = 100  # Метры в сантиметры

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        minutes = self.duration * self.M_IN_H
        speed_ms = mean_speed * self.KMH_TO_MS
        height_m: float = self.height / self.M_TO_SM
        return ((self.K_1 * self.weight + (speed_ms**2 / height_m)
                 * self.K_2 * self.weight) * minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    value_1: float = 1.1  # Для смещения значения средней скорости
    value_2: int = 2  # Для множителя скорости

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        mean_speed = Swimming.get_mean_speed(self)
        return ((mean_speed + self.value_1)
                * self.value_2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    exercise_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    if workout_type in exercise_types and data:
        return exercise_types[workout_type](*data)

    return 'Unexpected type'


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.show_training_info(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
