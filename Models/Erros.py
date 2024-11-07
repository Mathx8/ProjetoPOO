class DataNascFuturaException(Exception):
    def __init__(self, message="Data não pode ser no futuro."):
        self.message = message
        super().__init__(self.message)
        
class DataNascFormatException(Exception):
    def __init__(self, message="Data de nascimento inválida. Use o formato DD/MM/YYYY."):
        self.message = message
        super().__init__(self.message)
        
        
class IdadeInvalidaException(Exception):
    def __init__(self, message="Idade inválida. O número deve ser positivo e inteiro."):
        self.message = message
        super().__init__(self.message)

class IdadeMinimaException(Exception):
    def __init__(self, message="Idade mínima para cadastro é 18 anos."):
        self.message = message
        super().__init__(self.message)
        
class CpfInvalidoException(Exception):
    def __init__(self, message="CPF inválido, deve conter 11 dígitos."):
        self.message = message
        super().__init__(self.message)

class CpfExistenteException(Exception):
    def __init__(self, message="Erro: CPF já está cadastrado."):
        self.message = message
        super().__init__(self.message)
