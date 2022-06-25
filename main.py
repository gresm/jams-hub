import game_jams

selected = input("Select a jam id: ")

# check if the selected id is a valid int.
if not selected.isdigit():
    print("Not a number.")
    exit()


jam_id = int(selected)

if not 1 <= jam_id <= len(game_jams.game_jams):
    print("Invalid jam id.")
    print("Available jam ids: 1-" + str(len(game_jams.game_jams)))
    exit()

game_jams.game_jams[jam_id - 1]()
