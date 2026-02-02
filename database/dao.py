from database.DB_connect import DBConnect
from model.team import Team

class DAO:
    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT year
                    FROM team
                    WHERE year >= 1980 """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_teams_specific_year(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT s.team_id, t.name, s.team_code, t.year, SUM(s.salary) as total_salary
                    FROM team t, salary s
                    WHERE t.id = s.team_id and t.year = %s
                    GROUP BY s.team_id, t.name, s.team_code """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(
                id=row["team_id"],
                name=row["name"],
                team_code=row["team_code"],
                year=row["year"],
                total_salary=row["total_salary"]
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_teams_not_object(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT name, team_code
                    FROM team
                    WHERE year = %s """

        cursor.execute(query, (year,))

        for row in cursor:
            tupla = (str(row["name"]), str(row["team_code"]))
            result.append(tupla)

        cursor.close()
        conn.close()
        return result