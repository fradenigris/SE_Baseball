import copy
import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._nodes = None
        self._edges = None
        self._team = None

    @staticmethod
    def get_years():

        years = []
        for item in DAO.get_years():
            years.append(item['year'])

        return years

    @staticmethod
    def get_teams(year):
        return DAO.get_teams_not_object(year)


    def build_graph(self, year: int):
        self.G.clear()

        self._nodes = [item for item in DAO.get_teams_specific_year(year)]

        self.G.add_nodes_from(self._nodes)

        for node1 in self._nodes:
            for node2 in self._nodes:
                if node1 != node2:
                    salary = node1.total_salary + node2.total_salary
                    self.G.add_edge(node1, node2, weight = salary)

    def team_details(self, team):

        for node in self._nodes:
            if team == node.team_code:
                self._team = node
                break

        diz = {}
        neighbors = self.G.neighbors(self._team)

        for n in neighbors:
            diz[(self._team, n)] = self.G[n][self._team]['weight']

        return sorted(diz.items(), key=lambda x: x[1], reverse=True)

    def percorso(self):

        self._best_percorso = []
        self._best_score = 0

        if not self._team:
            return None

        parziale = [self._team]

        self._ricorsione(parziale)

        return self._best_percorso, self._best_score


    def _ricorsione(self, parziale):

        score_attuale = self.get_score(parziale)

        if score_attuale > self._best_score:
            self._best_score = score_attuale
            self._best_percorso = copy.deepcopy(parziale)

        last_node = parziale[-1]

        if len(parziale) == 1:
            peso_precedente = float('inf')
        else:
            peso_precedente = self.G[parziale[-2]][last_node]['weight']

        all_neighbors = list(self.G.neighbors(last_node))

        ammissibili = []
        for n in all_neighbors:
            peso_arco_potenziale = self.G[n][last_node]['weight']
            if (peso_arco_potenziale < peso_precedente) and (n not in parziale):
                ammissibili.append(n)

        ammissibili_ordinati = sorted(ammissibili, reverse=True)  # metodo __lt__

        for n in ammissibili_ordinati[:3]:
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

    def get_score(self, parziale):

        score = 0
        for i in range(0, len(parziale)-1):
            u = parziale[i]
            v = parziale[i+1]
            weight = self.G[u][v]['weight']
            score += weight

        return score

    def definitivo(self):

        lista, score = self.percorso()

        diz = {}
        for i in range(0, len(lista)-1):
            u = lista[i]
            v = lista[i+1]
            diz[(u, v)] = self.G[u][v]['weight']

        return diz, score

