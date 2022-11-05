from djchoices import ChoiceItem, DjangoChoices


class EventTypes(DjangoChoices):
    individual = ChoiceItem(value="INDIVIDUAL", label=("individual event"))
    team = ChoiceItem(value="TEAM", label=("team event"))


class CategoryTypes(DjangoChoices):
    cultural = ChoiceItem(value="CULTURAL", label=("cultural event"))
    technical = ChoiceItem(value="TECHNICAL", label=("technical event"))
    megashows = ChoiceItem(value="MEGASHOWS", label=("megashows event"))
    worshops = ChoiceItem(value="WORKSHOPS", label=("workshops"))


class ClubTypes(DjangoChoices):
    cultural = ChoiceItem(value="CULTURAL", label=("cultural club"))
    technical = ChoiceItem(value="TECHNICAL", label=("technical club"))


class CategorySubTypes(DjangoChoices):
    dance = ChoiceItem(value="DANCE", label=("dance event"))
    music = ChoiceItem(value="MUSIC", label=("music event"))
    coding = ChoiceItem(value="CODING", label=("coding event"))
    hardware = ChoiceItem(value="HARDWARE", label=("hardware event"))
