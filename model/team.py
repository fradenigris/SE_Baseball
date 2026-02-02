from dataclasses import dataclass

@dataclass
class Team:
    id : int
    name : str
    team_code : str
    year : int
    total_salary : float

    def __str__(self):
        return f"{self.id}, name: {self.name}, team code: {self.team_code}, year: {self.year}, total salary: {self.total_salary}"

    def __repr__(self):
        return f"{self.id}, name: {self.name}, team code: {self.team_code}, year: {self.year}, total salary: {self.total_salary}"

    def __lt__(self, other):
        return self.total_salary < other.total_salary

    def __hash__(self):
        return hash(self.id)