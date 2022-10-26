from djchoices import ChoiceItem, DjangoChoices


class UserAuthStatus(DjangoChoices):
    redirect = ChoiceItem(value="1")
    unverified = ChoiceItem(value="2")
    verified = ChoiceItem(value="3")
    completed = ChoiceItem(value="4")
    incorrect_data = ChoiceItem(value="5")
