import agents4e as agents
""" def ReflexVacuumAgent(): It is a higher order function
        def program(percept):
            location, status = percept
            if status == 'Dirty':
                return 'Suck'
            elif location == loc_A:
                return 'Right'
            elif location == loc_B:
                return 'Left'
        return Agent(program)
""" # loc_A, loc_B = (0, 0), (1, 0)  # The two locations for the Vacuum world
def main():
    percept = [(0,0), 'Dirty']
    print(agents.ReflexVacuumAgent().program(percept))

if __name__ == "__main__":
    main()