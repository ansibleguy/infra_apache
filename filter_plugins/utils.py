from re import sub as regex_replace


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "all_true": self.all_true,
            "prepare_letsencrypt": self.prepare_letsencrypt,
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
