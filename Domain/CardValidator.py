from Domain.CardClient import CardClient


class CardClientValidationError(Exception):
    pass


class CardClientValidator:
    def valideaza(self, card: CardClient):
        """
        Functia verifica daca datele introduse sunt
        corecte si returneaza erorile
        """
        if len(str(card.CNP)) != 13:
            raise ValueError("CNP trebuie sa aiba 13 cifre! ")
