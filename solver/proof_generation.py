class ProofConstructor:

    def __init__(self):
        self.return_proof = []

    def add_proof_step(self, first, second, child):
        new_proof_pass = [first, second, child]

        if new_proof_pass not in self.return_proof:
            self.return_proof.append(new_proof_pass)

    def __str__(self):
        pass_to_remove = []

        while True:
            pass_to_remove = []

            for i in range(len(self.return_proof) - 1):
                for j in range(i + 1, len(self.return_proof)):
                    if self.return_proof[j][0] == self.return_proof[i][2] or self.return_proof[j][1] == self.return_proof[i][2]:
                        continue

                pass_to_remove.append(self.return_proof[i])

            for item in pass_to_remove:
                self.return_proof.remove(item)

            if not pass_to_remove:
                break

        return_string = ""

        for pass_proof in self.return_proof:
            return_string += f"({pass_proof[0]} {pass_proof[1]}) -> {pass_proof[2]}\n"

        return return_string

    def size(self):
        return len(self.return_proof)

