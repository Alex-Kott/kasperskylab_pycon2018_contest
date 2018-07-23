from typing import Dict, Tuple, Union, List
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


def compare(person: Person):
    return person.stress_resistance


def swap_persons(list_a: List[Person],
                 list_b: List[Person],
                 person_a: Person,
                 person_b: Person) -> Tuple[Dict[int, Person], Dict[int, Person]]:
    core_group = {person.id:person for person in list_a}
    spare_group = {person.id:person for person in list_b}
    for person in list_a:
        if person.id == person_a.id:
            core_group.pop(person.id)
            spare_group[person.id] = person

    for person in list_b:
        if person.id == person_b.id:
            core_group[person.id] = person
            spare_group.pop(person.id)

    return {person.id: person for i, person in core_group.items()}, \
           {person.id: person for i, person in spare_group.items()}




def get_more_brave_specialists(core_group: Dict[int, Person], spare: Dict[int, Person]):
    general_group = [person for i, person in core_group.items()]
    spare_group = [person for i, person in spare.items()]
    for person in sorted(general_group, key=compare, reverse=True):
        for spare_person in sorted(spare_group, key=compare, reverse=True):
            if person.profession == spare_person.profession \
                    and person.stress_resistance < spare_person.stress_resistance:

                """сохраним состав групп перед очередным свопом и, если мужчин будет меньше 30%, 
                вернём сохранённые группы"""
                reserve_groups = (copy.deepcopy(general_group),
                                  copy.deepcopy(spare_group))

                general_group, spare_group = swap_persons(general_group,
                                                          spare_group,
                                                          person,
                                                          spare_person)
                ratio = get_men_women_ratio(general_group)
                if ratio[0] < 30:
                    return {person.id: person for person in reserve_groups[0]}, \
                           {person.id: person for person in reserve_groups[1]}

                return get_more_brave_specialists(general_group, spare_group)
                # return get_more_brave_women(general_group, spare_group)

    return {person.id: person for person in general_group},\
           {person.id: person for person in spare_group}


def count_stress_resistance(persons: Dict[int, Person]):
    stress_resistence_total = 0
    for i, person in persons.items():
        stress_resistence_total += person.stress_resistance

    return stress_resistence_total


def sum_stress_resist(persons):
    ids_string = '1;10;12;19;25;27;31;49;59;85;76;80;104;105;84;48;82;117;81;2;98;35;91;54;100;17;26;106;118;109;39;56;8;22;101;41;45;90;20;108;'
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

    # print(sum_stress_resist(persons))
    # exit()


    brave_persons = get_brave_persons(persons)

    favorites, spare = naive_filter_favourites(brave_persons, necessary_profs)

    # тут мы узнаём, что соотношение м/ж -- 50/50
    # print(get_men_women_ratio(favorites))

    # просто разменяем куна на тянку
    favorites, spare = rebalance_person_groups(favorites, spare)
    favorites, spare = get_more_brave_women(favorites, spare)
    favorites, spare = get_more_brave_specialists(favorites, spare)

    # print('')
    # print(count_stress_resistance(favorites))
    # print(get_men_women_ratio(favorites))

    for i, person in favorites.items():
        print("{};".format(person.id), end='')


