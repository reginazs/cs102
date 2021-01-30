import argparse
import pathlib
import typing as tp

Node = tp.Tuple[str, str]


def pas_(graph: tp.List[Node]):
    i = -1
    ref: tp.List[tp.Tuple[Node, int]] = []
    for link in graph:
        i += 1
        if link[0] == link[1]:
            ref.append((link, i))

    if len(ref) != 0:
        return (ref[0][0][0], graph[ref[0][1] + 1][0])

    if graph[i][1] != graph[0][0]:
        graph[i] = (graph[i][0], graph[0][0])

    return graph[i]


def load_tasks(taskfile: str = "tasks.txt") -> tp.List[tp.List[Node]]:
    res: tp.List[tp.List[Node]] = []
    exclude: tp.List[int] = []
    way = pathlib.Path(taskfile)
    with open(way, "r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines()):
            if line[:4] == "task":
                pos = line[4]
                res.insert(int(pos), [])
                exclude.append(i)
        f.seek(0)
        skip = -1
        for i, line in enumerate(f.readlines()):
            if i in exclude:
                skip += 1
                continue
            if "->" in line:
                res[skip].append((line[0], line[5]))

    return res


def flat_letters(graph: tp.List[Node]) -> tp.List[str]:
    letters = [[letter for letter in line] for line in graph]
    return [j for i in letters for j in i]


def find_broken_link(graph: tp.List[Node]) -> int:
    letters: tp.Dict[str, int] = {}
    letters_count = len(set(flat_letters(graph)))
    broken_links: tp.List[Node] = []
    if not letters_count == len(graph):
        raise ValueError("Malformed quest line.")
    broken = 0
    for link in graph:
        if link[0] == link[1]:
            broken_links.append(link)
            broken += 1
        for letter in link:
            if not letter in letters.keys():
                letters[letter] = 0
            letters[letter] += 1

    for i, count in enumerate(letters.values()):
        if i == 0:
            continue
        if count > 2:
            broken += 1

    return broken


def main():
    parser = argparse.ArgumentParser(description="Bugged quests")
    parser.add_argument(
        "quest_log", help="Path to questlog", default="tasks.txt", nargs="?", type=str
    )
    args = parser.parse_args()
    tasks = load_tasks(args.quest_log)
    for graph in tasks:
        broken = find_broken_link(graph)
        if broken != 1:
            print("V, V, V...")
        else:
            fix = pas_(graph)
            print(f"{fix[0]} -> {fix[1]}")

    return


main()
