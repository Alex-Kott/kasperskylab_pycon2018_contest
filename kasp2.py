from typing import Dict, Tuple, Union
import copy


class Person:
    def __init__(self, id, profession, sex, stress_resistance):
        self.id = int(id)
        self.profession = profession
        self.sex = int(sex)
        self.stress_resistance = int(stress_resistance)


def read_persons() -> Dict[int, Person]:
    """считаем сколько людишек у нас есть"""
    persons = {}
    for i in range(120):
        line = input()
        person = Person(*line.split(';'))
        persons[int(person.id)] = person

    return persons


def naive_filter_favourites(persons: Dict[int, Person],
                            profs: Dict[str, int]) -> Tuple[Dict[int, Person], Dict[int, Person]]:
    """мы знаем сколько специалистов каждого профиля нам нужны. просто отфильтруем их из тех,
    которые остались"""
    result_persons = {}
    spare = {person.id: person for person_id, person in persons.items()}
    for person_id, person in persons.items():
        if profs[person.profession] > 0:
            profs[person.profession] -= 1
            result_persons[person.id] = person
            spare.pop(person.id)

    return result_persons, spare


def get_brave_persons(persons: Dict[int, Person]) -> Dict[int, Person]:
    """в топку всех ссыкунов"""
    return {person.id: person for pid, person in persons.items() if person.stress_resistance >= 60}


def get_men_women_ratio(persons: Dict[int, Person]) -> Tuple[float, float]:
    """получим соотношение мужчины/женщины"""
    men = 0
    women = 0
    for id, person in persons.items():
        if person.sex == 1:
            men += 1
        elif person.sex == 0:
            women += 1

    men_percent = men / (len(persons) / 100)
    women_percent = 100 - men_percent

    return men_percent, women_percent


def get_woman_specialis(spare: Dict[int, Person], man_specialist: Person) -> Union[Person, None]:
    profession = man_specialist.profession
    for i, person in spare.items():
        if person.profession == man_specialist.profession:
            return person


def rebalance_person_groups(favorites, spare):
    """можно было бы упороться и написать какую-то универсальную ребалансировку (на данном этапе
    на основе предоставленных данных соотношение мужчин/женщин 50/50), но мне лень, и я бухой, так
    что просто заменую одного специалиста мужчину на специалиста-женщину"""
    result_persons = {p.id: p for i, p in favorites.items()}
    for i, person in favorites.items():
        if person.sex == 1:
            if get_woman_specialis(spare, person) is not None:
                woman_specialist = get_woman_specialis(spare, person)
                result_persons[woman_specialist.id] = woman_specialist
                result_persons.pop(person.id)
                spare[person.id] = person
                spare.pop(woman_specialist.id)
                return result_persons, spare
            else:
                continue


def get_more_brave_women(core_group: Dict[int, Person], spare: Dict[int, Person]):
    """отберём более стрессоустойчивых женщин"""
    general_group = copy.deepcopy(core_group)
    spare_group = copy.deepcopy(spare)
    for pid, person in core_group.items():
        for spare_id, spare_person in spare.items():
            if person.sex == spare_person.sex \
                    and person.profession == spare_person.profession \
                    and person.stress_resistance < spare_person.stress_resistance:
                general_group.pop(pid)
                general_group[spare_id] = spare_person
                spare_group.pop(spare_id)
                spare_group[pid] = person
                return get_more_brave_women(general_group, spare_group)

    return general_group, spare_group


# def get_more_brave_specialists(core_group: Dict[int, Person], spare: Dict[int, Person]):
#     general_group = [person for person in core_group]
#     spare_group = [person for person in spare]
#     for person in core_group:
#         for spare_person in spare:
#             if person.sex == spare_person.sex \
#                     and person.profession == spare_person.profession \
#                     and person.stress_resistance < spare_person.stress_resistance:
#                 general_group.pop(pid)
#                 general_group[spare_id] = spare_person
#                 spare_group.pop(spare_id)
#                 spare_group[pid] = person
#                 return get_more_brave_women(general_group, spare_group)
#
#     return general_group, spare_group


def count_stress_resistance(persons: Dict[int, Person]):
    stress_resistence_total = 0
    for i, person in persons.items():
        stress_resistence_total += person.stress_resistance

    return stress_resistence_total


def sum_stress_resist(persons):
    ids_string = '64;1;2;5;6;7;9;10;11;12;13;78;77;80;17;18;19;20;85;86;57;15;28;29;30;95;96;34;27;36;70;40;45;46;47;76;53;56;84;31;'
    ids = [int(i) for i in ids_string.split(';') if i != '']

    stress_resistence_total = 0
    for i, person in persons.items():
        if i in ids:
            stress_resistence_total += person.stress_resistance

    return stress_resistence_total


if __name__ == "__main__":
    necessary_profs = {
        "manager": 1,
        "cook": 3,
        "electrical engineer": 4,
        "computers specialist": 5,
        "doctor": 5,
        "mechanic": 8,
        "scientist": 14
    }

    persons = read_persons()


    brave_persons = get_brave_persons(persons)

    favorites, spare = naive_filter_favourites(brave_persons, necessary_profs)

    # тут мы узнаём, что соотношение м/ж -- 50/50
    # print(get_men_women_ratio(favorites))

    # просто разменяем куна на тянку
    favorites, spare = rebalance_person_groups(favorites, spare)
    favorites, spare = get_more_brave_women(favorites, spare)

    # print('')
    # print(count_stress_resistance(favorites))
    # print(get_men_women_ratio(favorites))

    for i, person in favorites.items():
        print("{};".format(person.id), end='')


