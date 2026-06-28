import hashlib


class BloomFilter:
    """
    Реалізація фільтра Блума.
    """

    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item):
        """
        Генерує кілька хешів
        для одного елемента.
        """

        for i in range(self.num_hashes):

            data = f"{item}{i}".encode()

            digest = hashlib.md5(data).hexdigest()

            yield int(digest, 16) % self.size

    def add(self, item):
        """
        Додає елемент
        до фільтра.
        """

        if not isinstance(item, str):
            return

        for index in self._hashes(item):
            self.bit_array[index] = 1

    def contains(self, item):
        """
        Перевіряє,
        чи може елемент
        бути у множині.
        """

        if not isinstance(item, str):
            return False

        for index in self._hashes(item):

            if self.bit_array[index] == 0:
                return False

        return True


def check_password_uniqueness(bloom_filter, passwords):
    """
    Перевірка списку паролів.
    """

    results = {}

    for password in passwords:

        if not isinstance(password, str) or password == "":
            results[str(password)] = "некоректне значення"
            continue

        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results


if __name__ == "__main__":

    bloom = BloomFilter(
        size=1000,
        num_hashes=3
    )

    existing_passwords = [
        "password123",
        "admin123",
        "qwerty123"
    ]

    for password in existing_passwords:
        bloom.add(password)

    new_passwords = [
        "password123",
        "newpassword",
        "admin123",
        "guest",
        "",
        None
    ]

    results = check_password_uniqueness(
        bloom,
        new_passwords
    )

    print("=" * 60)
    print("Перевірка унікальності паролів")
    print("=" * 60)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")