import random
import sys
import os
WINNING_SCORE = 10

def clear_screen():
    print("\033[2J\033[H", end = "")

class Aircraft:
    def namegen(self):
        A = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        B = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        C = random.randint(0,9)
        D = random.randint(0,9)
        return (f'{A}{B}{C}{D}')

    def __init__(self):
        self.codename = self.namegen()
        self.distance = random.randint(4,10)

        self.speed = random.choice([1,2,3])

        self.fuel = max(random.randint(6,12), (self.distance + self.speed - 1) // self.speed + 1)
        self.holding = False
        self.direction = -1

    ######MOVE########################
    def move(self):
        if not self.holding:
            if self.direction == -1:
                if self.distance > 0 and self.distance - self.speed <= 0:
                    self.distance = 0
                else:
                    self.distance -= self.speed

            else:
                if self.distance < 0 and self.distance + self.speed >= 0:
                    self.distance = 0
                else:
                    self.distance += self.speed

            self.fuel -= 1

        else:
            self.fuel -= 1

######CHECK LANDING##################
    def can_land(self):
        if self.distance == 0:
            return True
        else:
            return False

######PLANE FINDER##################
def find_plane(planes, codename):
    for plane in planes:
        if plane.codename == codename:
            return plane
    return None

######STATUS PRINTER########################
def show_status(planes, score, message):
    print('=' * 60)
    print('                  AIR TRAFFIC CONTROL')
    print('=' * 60)
    print(f'LANDED: {score}')
    print()
    print(message)
    print()
    print(
        f"{'CODENAME':<12}"
        f"{'DISTANCE':<12}"
        f"{'FUEL':<10}"
        f"{'SPEED':<10}"
        f"STATUS"
    )

    print('-' * 60)

    for plane in planes:
        if plane.holding:
            status = 'HOLDING'
        elif plane.direction == 1:
            status = 'RETURNING'
        else:
            status = 'INBOUND'

        print(
            f"{plane.codename:<12}"
            f"{plane.distance:<12}"
            f"{plane.fuel:<10}"
            f"{plane.speed:<10}"
            f"{status}"
        )

    print('-' * 60)
    print()
    print('Commands: ')
    print('  wait')
    print('  inspect CODENAME')
    print('  land CODENAME')
    print('  hold CODENAME')
    print('  resume CODENAME')
    print('  return CODENAME')
    print('  help')

######TURN########################
def turn(planes):
    for plane in planes:
        plane.move()

    new_plane = None

    if len(planes) < 6:
        if random.randint(1,4) == 1:
            new_plane = spawn_plane(planes)

    check_donger(planes)
    return new_plane

######DONGER######################## Donger instead of danger as reference for brooklyn 99
def check_donger(planes):
    reason = None

    for plane in planes:
        if plane.fuel <= 0:
            reason = (
                f'Plane {plane.codename} ran out of fuel mid-air! '
                f'No casualties though, Sully was the captain. '
                f'That was crazy tbh.'
            )
            break

        for plane2 in planes:
            if (plane is not plane2) and (plane.distance == plane2.distance):
                reason = (
                    f'Planes {plane.codename} and {plane2.codename} crashed! '
                    f'Some survivors landed on an island and started the tv show '
                    f'Lost, so all good twin. Dozens other died though.'
                )
                break

    if reason:
        clear_screen()
        print('=' * 60)
        print('                 AIR TRAFFIC CONTROL')
        print('=' * 60)
        print()
        print('                       SHIFT FAILED')
        print()
        print('REASON: ')
        print(reason)
        print('                         GAME OVER')
        print()
        print('=' * 60)
        sys.exit()

######SPAWN PLANE########################
def spawn_plane(planes):
    while True:
        plane = Aircraft()
        valid = True

        for plane2 in planes:
            if plane.distance == plane2.distance or plane.codename == plane2.codename:
                valid = False

        if valid:
            planes.append(plane)
            return plane

###### WINNER WINNER ##################
def check_win(score):
    if score >= WINNING_SCORE:
        clear_screen()
        print('=' * 60)
        print('                      AIR TRAFFIC CONTROL')
        print('=' * 60)
        print()
        print('                      6 AM: SHIFT COMPLETE')
        print()
        print('                   All aircraft landed safely')
        print()
        print(f'                        FINAL SCORE: {score}')
        print()
        print('                            YOU WIN!')
        print()
        print('=' * 60)
        sys.exit()

def main():
    #Create list planes, starting with 3, and score
    planes = []
    for i in range(3):
        spawn_plane(planes)
    score = 0
    message = ''

    while True:
        clear_screen()
        show_status(planes, score, message)
        message = ''

        command = input("ATC > ").split()

        if not command:
            continue

        if command[0] == 'quit':
            sys.exit('Game Finished!')

        elif command[0] == 'wait':
            new_plane = turn(planes)

            if new_plane:
                message = f'NEW AIRCRAFT DETECTED: {new_plane.codename}'

            continue

        elif command[0] == 'inspect':
            if len(command) != 2:
                message = ('You need to specify the aircraft for this command')
                continue

            plane = find_plane(planes, command[1])

            if plane == None:
                message = ('Aircraft not found')
                continue

            else:
                message = (
                    f'Codename: {plane.codename}\n'
                    f'Distance: {plane.distance}\n'
                    f'Fuel: {plane.fuel}\n'
                    f'Speed: {plane.speed}\n'
                )
                continue

        elif command[0] == 'land':
            if len(command) != 2:
                message = ('You need to specify the aircraft for this command')
                continue

            plane = find_plane(planes, command[1])

            if plane == None:
                message = ('Aircraft not found')
                continue

            if plane.can_land():
                message = ('Plane landed!')
                score += 1
                check_win(score)

                planes.remove(plane)

                new_plane = turn(planes)

                if new_plane:
                    message = f'Plane landed!\nNEW AIRCRAFT DETECTED: {new_plane.codename}'

                continue

            else:
                message = ('Plane is too far away from runway')
                continue

        ###### HOLD AND RESUME ##################
        elif command[0] == 'hold':
            if len(command) != 2:
                message = ('You need to specify the aircraft for this command')
                continue

            plane = find_plane(planes, command[1])

            if plane == None:
                message = ('Aircraft not found')
                continue

            if plane.holding == True:
                message = ('Plane already on hold.')
                continue

            plane.holding = True

            new_plane = turn(planes)

            if new_plane:
                message = f'NEW AIRCRAFT DETECTED: {new_plane.codename}'

            continue

        elif command[0] == 'resume':
            if len(command) != 2:
                message = ('You need to specify the aircraft for this command')
                continue

            plane = find_plane(planes, command[1])

            if plane == None:
                message = ('Aircraft not found')
                continue

            if plane.holding == False:
                message = ('Plane already inbound.')
                continue

            plane.holding = False

            new_plane = turn(planes)

            if new_plane:
                message = f'NEW AIRCRAFT DETECTED: {new_plane.codename}'

            continue

        ###### RETURN ##################
        elif command[0] == 'return':
            if len(command) != 2:
                message = ('You need to specify the aircraft for this command')
                continue

            plane = find_plane(planes, command[1])

            if plane == None:
                message = ('Aircraft not found')
                continue

            if plane.distance >= 0:
                message = ('Aircraft has not passed the runway.')
                continue

            if plane.direction == 1:
                message = ('Aircraft already returning.')
                continue

            plane.direction = 1

            new_plane = turn(planes)

            if new_plane:
                message = f'Aircraft returning.\nNEW AIRCRAFT DETECTED: {new_plane.codename}'
            else:
                message = ('Aircraft returning.')

            continue

        elif command[0] == 'help':
            message = (
                'Commands: \n'
                'help\n'
                'wait\n'
                'inspect CODENAME\n'
                'land CODENAME\n'
                'hold CODENAME\n'
                'resume CODENAME\n'
                'return CODENAME'
            )

if __name__ == "__main__":
    main()