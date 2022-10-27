from djchoices import ChoiceItem, DjangoChoices


class UserAuthStatus(DjangoChoices):
    message = ChoiceItem(value="1")
    verified = ChoiceItem(value="2")
    completed = ChoiceItem(value="3")
