import pandas as pd

people = pd.read_csv(".01_people.csv")
education = pd.read_csv("education.csv")
skills = pd.read_csv("skills.csv")
abilities = pd.read_csv("abilities.csv")
experience = pd.read_csv("experience.csv")
person_skill = pd.read_csv("person_skill.csv")

print(people.head())