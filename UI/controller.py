import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_year = None
        self._current_team = None
        self._is_graph_created = False

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO

        self._model.build_graph(self._current_year)

        self._view.show_alert('Grafo creato!')
        self._is_graph_created = True

        if self._current_team:
            self._view.pulsante_dettagli.disabled = False
            self._view.update()

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO

        self._view.txt_risultato.controls.clear()

        if not self._is_graph_created:
            self._view.show_alert('Crea prima il grafo!')
            return

        if not self._current_team:
            self._view.show_alert('Seleziona una squadra!')
            return

        result = self._model.team_details(self._current_team)

        for item in result:
            peso = item[1]
            testo = f'{item[0][1].team_code} ({item[0][1].name}) - peso {peso}'
            self._view.txt_risultato.controls.append(ft.Text(testo))

        self._view.pulsante_percorso.disabled = False

        self._view.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO

        self._view.txt_risultato.controls.clear()

        diz, totale = self._model.definitivo()

        for item in diz.keys():
             self._view.txt_risultato.controls.append(ft.Text(f'{item[0].team_code} ({item[0].name}) -> {item[1].team_code} ({item[1].name}) ({diz[item]})'))

        self._view.txt_risultato.controls.append(ft.Text(f'Peso totale: {totale}'))

        self._view.update()


    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO

    def popola_dd_anno(self):

        self._view.dd_anno.options.clear()

        years = self._model.get_years()

        if years:
            for year in years:
                self._view.dd_anno.options.append(ft.dropdown.Option(str(year)))
        else:
            self._view.show_alert("Errore nel caricamento degli anni.")

        self._view.update()

    def on_year_change(self, e):

        selected_option = e.control.value
        if not selected_option:
            self._current_year = None
            self._view.show_alert("Errore nella selezione dell'anno.")
            return

        self._view.pulsante_crea_grafo.disabled = False

        self._current_year = selected_option

        self._is_graph_created = False
        self._view.pulsante_dettagli.disabled = True

        self._view.txt_out_squadre.controls.clear()
        self._view.dd_squadra.options.clear()

        teams = self._model.get_teams(int(selected_option))

        if not teams:
            self._view.show_alert("Errore nel caricamento di lettura dei teams.")
            self._view.update()
            return

        self._view.txt_out_squadre.controls.append(ft.Text(f'Numero squadre: {len(teams)}'))

        for team in teams:
            visivo = f'{team[1]} ({team[0]})'
            self._view.txt_out_squadre.controls.append(ft.Text(visivo))
            self._view.dd_squadra.options.append(ft.dropdown.Option(key=str(team[1]),text=visivo))

        self._view.update()

    def on_team_change(self, e):

        selected_option = e.control.value
        if not selected_option:
            self._current_team = None
            self._view.show_alert("Errore nella selezione della squadra.")
            return

        self._current_team = selected_option

        if self._is_graph_created:
            self._view.pulsante_dettagli.disabled = False

        self._view.update()