jams = ["jam_1"]

jam = jams[int(input(f"Select a jam number, from 1 to {len(jams)}: ")) - 1]
exec(f"import {jam} as run_jam")
