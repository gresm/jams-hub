import sys
import game_jams


def run_jam(jam_id: int):
    game_jams.game_jams[jam_id]()


if len(sys.argv) > 1:
    run_jam(int(sys.argv[1]))
else:
    selected = input("Select a jam id: ")

    # check if the selected id is a valid int.
    if not selected.isdigit():
        print("Not a number.")
        exit()

    selected = int(selected)

    if not 1 <= selected <= len(game_jams.game_jams):
        print("Invalid jam id.")
        print("Available jam ids: 1-" + str(len(game_jams.game_jams)))
        exit()

    run_jam(selected)
