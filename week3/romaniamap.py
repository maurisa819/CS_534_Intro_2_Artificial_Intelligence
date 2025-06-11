from search import *

def main():
    print(romania_map.nodes())
    print()

    print(romania_map.get('Arad', 'Bucharest'))
    print()

    print(romania_map.get('Fagaras', 'Bucharest'))
    print()

    print(romania_map.locations)

if __name__ == "__main__":
    main()