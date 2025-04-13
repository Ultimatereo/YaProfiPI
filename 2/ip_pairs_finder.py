import csv
import logging
import platform
import random
import socket
import subprocess
from abc import ABC, abstractmethod

# Логгирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


# Интерфейсы

class IIPAvailabilityChecker(ABC):
    """Контракт: метод для проверки доступности IP-адреса."""

    @abstractmethod
    def is_available(self, ip: str) -> bool:
        pass


class IIPGenerator(ABC):
    """Контракт: получение списка IP-адресов."""

    @abstractmethod
    def generate_ip_addresses(self) -> list:
        pass


class IIPPropertyExtractor(ABC):
    """
    Контракт: извлечь некоторое целочисленное свойство из IP-адреса
    и сгенерировать случайный IP, обладающий данным свойством.
    """

    @abstractmethod
    def extract_property(self, ip: str) -> int:
        pass

    @abstractmethod
    def generate_candidate(self, prop_value: int) -> str:
        pass


class IIPPairFinder(ABC):
    """Контракт: найти пары IP, для которых извлечённое свойство совпадает."""

    @abstractmethod
    def find_pairs(self, ips: list, prop_extractor: IIPPropertyExtractor) -> list:
        pass


class ICSVWriter(ABC):
    """Контракт: записать данные в CSV-файл."""

    @abstractmethod
    def write_csv(self, header: list, rows: list) -> None:
        pass


# Реализации

class IPAvailabilityChecker(IIPAvailabilityChecker):
    """
    Класс для проверки доступности IP-адреса.

    Реализует контракт IIPAvailabilityChecker, используя метод ping для проверки доступности.
    """

    @staticmethod
    def _check_ping(ip: str) -> bool:
        """
        Выполняет проверку доступности IP через команду ping.

        :param ip: IP-адрес для проверки.
        :return: True, если ping выполнен успешно, иначе False.
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ["ping", param, "1", ip]
        logging.info(f"Проверка IP (ping): {ip}")
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                logging.info(f"IP {ip} доступен по ping.")
                return True
            else:
                logging.info(f"IP {ip} не отвечает (код {result.returncode}).")
                return False
        except Exception as e:
            logging.error(f"Ошибка ping для {ip}: {e}")
            return False

    def is_available(self, ip: str) -> bool:
        """
        Проверяет доступность IP-адреса.

        :param ip: IP-адрес для проверки.
        :return: True, если IP доступен, иначе False.
        """
        return self._check_ping(ip)


class IPGenerator(IIPGenerator):
    """
    Класс для получения IP-адресов.

    Реализует контракт IIPGenerator, разрешая доменные имена популярных сайтов.
    """

    def generate_ip_addresses(self) -> list:
        """
        Разрешает доменные имена из предопределённого списка в IP-адреса.

        :return: Список полученных IP-адресов.
        """
        domains = [
            "google.com",
            "youtube.com",
            "facebook.com",
            "instagram.com",
            "x.com",
            "whatsapp.com",
            "chatgpt.com",
            "wikipedia.org",
            "reddit.com",
            "yahoo.com",
            "yahoo.co.jp",
            "yandex.ru",
            "amazon.com",
            "tiktok.com",
            "baidu.com",
            "microsoftonline.com",
            "linkedin.com",
            "netflix.com",
            "pornhub.com",
            "dzen.ru",
            "naver.com",
            "bet.br",
            "live.com",
            "office.com",
            "bing.com",
            "bilibili.com",
            "pinterest.com",
            "microsoft.com",
            "xvideos.com",
            "twitch.tv",
            "xhamster.com",
            "temu.com",
            "vk.com",
            "mail.ru",
            "news.yahoo.co.jp",
            "sharepoint.com",
            "weather.com",
            "samsung.com",
            "fandom.com",
            "globo.com",
            "canva.com",
            "t.me",
            "duckduckgo.com",
            "xnxx.com",
            "xhamster43.desi",
            "nytimes.com",
            "deepseek.com",
            "zoom.us",
            "stripchat.com",
            "quora.com"
        ]
        ips = []
        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                ips.append(ip)
                logging.info(f"{domain} -> {ip}")
            except Exception as e:
                logging.error(f"Не удалось получить IP для {domain}: {e}")
        logging.info(f"Получено {len(ips)} IP из доменов.")
        return ips


class SumOctetsExtractor(IIPPropertyExtractor):
    """
    Класс для извлечения свойства суммы октетов из IP-адреса.

    Реализует контракт IIPPropertyExtractor:
      - extract_property возвращает сумму всех октетов.
      - generate_candidate генерирует случайный IP с заданной суммой октетов.
    """

    def extract_property(self, ip: str) -> int:
        """
        Вычисляет сумму октетов IP-адреса.

        :param ip: IP-адрес в формате строки.
        :return: Сумма октетов.
        """
        return sum(int(octet) for octet in ip.split('.'))

    def generate_candidate(self, prop_value: int) -> str:
        """
        Генерирует случайный IP-адрес, сумма октетов которого равна prop_value.

        :param prop_value: Желаемая сумма октетов.
        :return: Сформированный IP-адрес.
        """
        while True:
            a = random.randint(0, 255)
            b = random.randint(0, 255)
            c = random.randint(0, 255)
            d = prop_value - (a + b + c)
            if 0 <= d <= 255:
                candidate = f"{a}.{b}.{c}.{d}"
                return candidate


class CountOnesExtractor(IIPPropertyExtractor):
    """
    Класс для извлечения свойства количества единиц в битовом представлении IP-адреса.

    Реализует контракт IIPPropertyExtractor:
      - extract_property возвращает количество установленных бит (1) в IP.
      - generate_candidate генерирует случайный IP с требуемым количеством единиц.
    """

    def extract_property(self, ip: str) -> int:
        """
        Преобразует IP в 32-битное число и считает количество единиц в двоичном представлении.

        :param ip: IP-адрес.
        :return: Количество единиц в его бинарном виде.
        """
        ip_int = int.from_bytes(socket.inet_aton(ip), byteorder='big')
        return bin(ip_int).count("1")

    def generate_candidate(self, prop_value: int) -> str:
        """
        Генерирует случайный IP до тех пор, пока количество единиц в его двоичном представлении не равно prop_value.

        :param prop_value: Требуемое количество единиц.
        :return: Сформированный IP-адрес.
        """
        while True:
            ip_int = random.randint(0, 2 ** 32 - 1)
            if bin(ip_int).count("1") == prop_value:
                candidate = socket.inet_ntoa(ip_int.to_bytes(4, byteorder='big'))
                return candidate


class IPPairFinder(IIPPairFinder):
    """
    Класс для поиска пар IP-адресов по совпадению извлечённого свойства.

    Для каждого доступного IP, извлекается его свойство, затем производится несколько попыток
    сгенерировать кандидат-адрес с таким же свойством. Если кандидат также доступен, пара добавляется в результат.
    """

    def __init__(self, checker: IIPAvailabilityChecker, attempts: int = 10):
        """
        Инициализация класса.

        :param checker: Объект, реализующий IIPAvailabilityChecker для проверки доступности IP.
        :param attempts: Количество попыток найти кандидата для каждой проверки.
        """
        self.checker = checker
        self.attempts = attempts

    def find_pairs(self, ips: list, prop_extractor: IIPPropertyExtractor) -> list:
        """
        Находит пары IP с совпадающим свойством.

        :param ips: Список исходных IP-адресов.
        :param prop_extractor: Объект, реализующий IIPPropertyExtractor для работы со свойством IP.
        :return: Список пар в формате (ip1, "Доступен", ip2, "Доступен", "Свойство=...").
        """
        pairs = []
        for ip in ips:
            if self.checker.is_available(ip):
                prop = prop_extractor.extract_property(ip)
                found = False
                for _ in range(self.attempts):
                    candidate = prop_extractor.generate_candidate(prop)
                    if candidate == ip:
                        continue
                    if self.checker.is_available(candidate):
                        pairs.append((ip, "Доступен", candidate, "Доступен", f"Свойство={prop}"))
                        logging.info(f"Пара найдена: {ip} и {candidate} (свойство={prop})")
                        found = True
                if not found:
                    logging.info(f"Ни для {ip} не найден кандидат с собственностью {prop}")
            else:
                logging.info(f"{ip} недоступен – пропускаем.")
        logging.info(f"Всего пар: {len(pairs)}")
        return pairs


class CSVWriter(ICSVWriter):
    """
    Класс для записи данных в CSV-файл.

    Реализует контракт ICSVWriter, записывая данные в указанный файл с кодировкой UTF-8.
    """

    def __init__(self, file_name: str):
        """
        Инициализирует объект для записи в CSV-файл.

        :param file_name: Имя файла для записи.
        """
        self.file_name = file_name

    def write_csv(self, header: list, rows: list) -> None:
        """
        Записывает данные в CSV-файл.

        :param header: Список заголовков столбцов.
        :param rows: Список строк данных.
        """
        try:
            with open(self.file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
            logging.info(f"Результаты записаны в {self.file_name}")
        except Exception as e:
            logging.error(f"Ошибка записи файла {self.file_name}: {e}")


class IPApp:
    """
    Основное приложение для поиска пар IP-адресов.

    Объединяет компоненты проверки доступности, генерации IP-адресов,
    извлечения свойства и поиска пар, а также записи результатов в CSV.
    """

    def __init__(self,
                 checker: IIPAvailabilityChecker,
                 generator: IIPGenerator,
                 pair_finder: IIPPairFinder,
                 csv_writer: ICSVWriter,
                 prop_extractor: IIPPropertyExtractor):
        """
        Инициализация приложения.

        :param checker: Объект проверки доступности IP.
        :param generator: Объект генерации IP-адресов.
        :param pair_finder: Объект поиска пар IP по свойству.
        :param csv_writer: Объект для записи результатов в CSV.
        :param prop_extractor: Объект извлечения свойства IP.
        """
        self.checker = checker
        self.generator = generator
        self.pair_finder = pair_finder
        self.csv_writer = csv_writer
        self.prop_extractor = prop_extractor

    def run(self):
        """
        Запускает процесс: генерирует IP-адреса, находит пары с совпадающим свойством,
        записывает результаты в CSV-файл.
        """
        logging.info("Начало работы приложения.")
        ips = self.generator.generate_ip_addresses()
        pairs = self.pair_finder.find_pairs(ips, self.prop_extractor)
        header = ["IPv4-адрес 1", "Критерий 1", "IPv4-адрес 2", "Критерий 2", "Свойство"]
        self.csv_writer.write_csv(header, pairs)
        logging.info("Работа приложения завершена.")


def main() -> None:
    # Можно легко подменить реализацию свойства.
    # Для проверки по сумме октетов:
    prop_extractor_sum = SumOctetsExtractor()
    # Для проверки по количеству единиц в IP:
    prop_extractor_ones = CountOnesExtractor()

    checker = IPAvailabilityChecker()
    generator = IPGenerator()
    pair_finder = IPPairFinder(checker)

    app_sum = IPApp(checker, generator, pair_finder, CSVWriter("pair_results_sum.csv"), prop_extractor_sum)
    app_sum.run()

    app_ones = IPApp(checker, generator, pair_finder, CSVWriter("pair_results_ones.csv"), prop_extractor_ones)
    app_ones.run()


if __name__ == "__main__":
    main()
