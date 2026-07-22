class ComputerAlreadyExistsError(Exception):
    """Levantada ao tentar registrar um computador com hostname já cadastrado."""

    def __init__(self, hostname: str) -> None:
        self.hostname = hostname
        super().__init__(f"Computador com hostname '{hostname}' já está registrado.")


class ComputerNotFoundError(Exception):
    """Levantada ao referenciar um computador que não existe."""

    def __init__(self, computer_id: int) -> None:
        self.computer_id = computer_id
        super().__init__(f"Computador com id {computer_id} não encontrado.")
