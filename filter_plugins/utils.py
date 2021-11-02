from re import sub as regex_replace


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "all_true": self.all_true,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace('[^0-9a-zA-Z]+', '', key.replace(' ', '_'))

    @staticmethod
    def all_true(data: list) -> bool:
        return all(data)
