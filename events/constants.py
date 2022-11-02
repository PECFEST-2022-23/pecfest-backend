from djchoices import ChoiceItem, DjangoChoices


class EventTypes(DjangoChoices):
    individual = ChoiceItem(value="INDIVIDUAL", label=("individual event"))
    team = ChoiceItem(value="TEAM", label=("team event"))


class ClubTypes(DjangoChoices):
    cultural = ChoiceItem(value="CULTURAL", label=("cultural club"))
    technical = ChoiceItem(value="TECHNICAL", label=("technical club"))


class EventSubTypes(DjangoChoices):
    dance = ChoiceItem(value="DANCE", label=("dance event"))
