class Debug:
    def __init__(self, is_on):
        if is_on == 1:
            self.DEBUG_FLAG = True

    def console(self, data):
        if self.DEBUG_FLAG is True:
            print(data)

