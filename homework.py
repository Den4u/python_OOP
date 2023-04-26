class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TRAINING_TYPE = ''
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    TRAINING_TYPE = 'RUN'

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * self.duration * self.MIN_IN_HOUR)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_WLK_1 = 0.035
    COEFF_WLK_2 = 0.029
    KM_H_IN_M_S = 0.278
    SM_IN_M = 100
    TRAINING_TYPE = 'WLK'

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_WLK_1
                    * self.weight
                    + ((self.get_mean_speed() * self.KM_H_IN_M_S)**2
                     / (self.height / self.SM_IN_M))
                    * self.COEFF_WLK_2 * self.weight)
                    * (self.duration * self.MIN_IN_HOUR))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_SWM_1 = 1.1
    COEFF_SWM_2 = 2
    LEN_STEP = 1.38
    TRAINING_TYPE = 'SWM'

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    """Получить среднюю скорость движения."""
    def get_mean_speed(self) -> float:
        speed = ((self.length_pool
                  * self.count_pool) / super().M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + 1.1)
                    * 2 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
