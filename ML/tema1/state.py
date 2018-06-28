from copy import copy

## Class for keeping info about a state
class State:
    def __init__(self, room_no, radius):
        self.room = room_no
        self.radius = radius
        self.is_final = False

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def change_room(self, n):
        self.room = n

    def get_room(self):
        return self.room

    def get_position(self):
        return self.x, self.y

    def get_x_position(self):
        return self.x

    def get_y_position(self):
        return self.y

    def is_final_state(self, val=None):
        if val != None:
            self.is_final = val
        else:
            return self.is_final

    def __serialize_state(self, state):
        return "\n".join(map(lambda row: "".join(row), state))

    ## Get the part of the map that Gigel sees
    def get_visible_field(self):
        room = State.ROOMS[self.room]
        start_x = self.x - self.radius if self.x - self.radius >= 0 else 0
        end_x = self.x + self.radius if self.x + self.radius < len(room) else len(room)
        start_y = self.y - self.radius if self.y - self.radius >= 0 else 0
        end_y = self.y + self.radius if self.y + self.radius < len(room) else len(room)


        field = copy([r[start_y:end_y] for r in room[start_x:end_x]])
        field[self.x - start_x][self.y - start_y] = "G"
        return self.__serialize_state(field)

    # the state to be saved in Q learning
    def save_state(self):
        return ((self.x, self.y), self.room, self.get_visible_field())
