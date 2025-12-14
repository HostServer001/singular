class Lol:
    @property
    def get(self):
        return {
            "lol":"first lol",
            "lol2":"second lol"
        }

l = Lol()
print(l.get["lol2"])