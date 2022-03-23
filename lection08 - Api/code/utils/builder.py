from dataclasses import dataclass

import faker

fake = faker.Faker()


class Builder:

    @staticmethod
    def topic(title=None, text=None):
        @dataclass
        class Topic:
            title: str = ''
            text: str = ''
            id: int = 0

        if title is None:
            title = fake.lexify(text='???? ??? ???')
        if text is None:
            text = fake.lexify(text='???? ???? ??? ??????')

        return Topic(title=title, text=text)
