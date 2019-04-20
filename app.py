from constants import PLAYERS, TEAMS
import textwrap
import shutil


def clean_player_list():
    """Takes player list from constants.PLAYERS and returns new list of
    dictionaries with guardians split into a list of names, experience converted
    to a boolean, and height turned into an integer."""
    players = []
    for player in PLAYERS:
        name = player['name']
        guardians = player['guardians'].split(' and ')
        experience = True if player['experience'] == 'YES' else False
        height = int(player['height'].split()[0])
        clean_player = {'name': name, 'guardians': guardians, 'experience': experience, 'height': height}
        players.append(clean_player)
    return players


def clean_team_list():
    """Takes team list from constants.TEAMS and returns new list of teams
    ready to be populated with player data."""
    teams = []
    for teamname in TEAMS:
        team = {'teamname': teamname, 'players': []}
        teams.append(team)
    return teams


def populate_teams():
    """Populates teams with formatted data to include an equal number of
    experienced and inexperienced players for each team, and then returns teams
    as a list with nested dictionaries of teams and players."""
    player_list = clean_player_list()
    teams = clean_team_list()
    experienced_players = [player for player in player_list if player['experience']]
    inexperienced_players = [player for player in player_list if not player['experience']]

    for team in teams:
        players = team['players']
        while len(players) < len(player_list) // len(teams):
            players.append(experienced_players.pop())
            players.append(inexperienced_players.pop())
    return teams


def welcome():
    welcome_message = "Basketball Team Stats Tool"
    print(welcome_message)
    print('-' * len(welcome_message))


def main_menu():
    """Displays menu to display statistics for teams"""
    teams = populate_teams()
    welcome()

    while True:
        print("\nChoose a team to display statistics. Enter 'q' at any time to quit.\n")
        print("Teams:")
        for i in range(len(teams)):
            print("  {}) {}".format(i+1, teams[i]['teamname']))

        choice = input("\nEnter an option: ")
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        else:
            try:
                choice = int(choice)
            except ValueError:
                print("Choice must be a number between 1 and {}.".format(len(teams)))
                continue
            if 1 <= choice <= len(teams):
                team = teams[choice-1]
            else:
                print("{} is an invalid choice. Choice must between 1 and {}.".format(choice, len(teams)))
                continue
            display_stats(team)
            input("\nPress ENTER to continue...")
            print("\n")


def display_stats(team):
    try:
        terminal_width = shutil.get_terminal_size(fallback=(100, 20)).columns
    except OSError:
        terminal_width = 100

    teamname = team['teamname']
    players = team['players']
    experienced_players = [player for player in players if player['experience']]
    inexperienced_players = [player for player in players if not player['experience']]
    guardians = [guardian for guardianlist in [player['guardians'] for player in players] for guardian in guardianlist]
    avg_height = sum([player['height'] for player in players]) / len(players)

    header = "Team Statistics for {}:".format(teamname)
    player_names = ', '.join([player['name'] for player in players])
    guardian_names = ', '.join(guardians)
    print("\n" + header)
    print("-" * len(header))

    print("\nTotal Players:", len(players))
    print("\nPlayer Names:\n")
    print('\n'.join(textwrap.wrap(player_names, width=terminal_width)))

    print("\nGuardian Names:\n")
    print('\n'.join(textwrap.wrap(guardian_names, width=terminal_width)))

    print("\nNumber of experienced players on team:", len(experienced_players))
    print("Number of inexperienced players on team:", len(inexperienced_players))
    print("Average height of player on team:", round(avg_height*10)/10, 'inches')


if __name__ == "__main__":
    main_menu()
