from re import sub as regex_replace


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "all_true": self.all_true,
            "prepare_letsencrypt": self.prepare_letsencrypt,
            "ensure_list": self.ensure_list,
            "enmod_list": self.enmod_list,
            "mod_list": self.mod_list,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace(r'[^0-9a-zA-Z\.]+', '', key.replace(' ', '_'))

    @staticmethod
    def all_true(data: list) -> bool:
        return all(data)

    @staticmethod
    def prepare_letsencrypt(site: dict, name: str) -> dict:
        domains = [site['domain']]
        domains.extend(site['aliases'])
        return {
            name: {
                'domains': domains,
                'key_size': site['letsencrypt']['key_size'],
                'email': site['letsencrypt']['email'],
                'state': site['state'],
            }
        }

    @classmethod
    def enmod_list(cls, present: list, absent: list) -> str:
        absent_list = cls.ensure_list(absent)
        return ' '.join([mod for mod in cls.ensure_list(present) if mod not in absent_list])

    @classmethod
    def mod_list(cls, mods: (str, list)) -> str:
        return ' '.join(cls.ensure_list(mods))

    @staticmethod
    def ensure_list(data: (str, list)) -> list:
        # if user supplied a string instead of a list => convert it to match our expectations
        if type(data) == list:
            return data

        else:
            return [data]
