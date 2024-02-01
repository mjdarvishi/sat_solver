class ProofGenerator:
    def __init__(self):
        self.proof_steps = []

    def add_proof_step(self, p1, p2, child):
        new_proof_pass = [p1, p2, child]
        self.proof_steps.append(new_proof_pass)

    def generate(self):
        pass_to_remove = []
        while True:
            for i in range(len(self.proof_steps) - 1):
                for j in range(i + 1, len(self.proof_steps)):
                    if (
                        self.proof_steps[j][0] == self.proof_steps[i][2]
                        or self.proof_steps[j][1] == self.proof_steps[i][2]
                    ):
                        continue
                    pass_to_remove.append(self.proof_steps[i])

            self.proof_steps = [proof for proof in self.proof_steps if proof not in pass_to_remove]

            if not pass_to_remove:
                break

        return self.proof_steps