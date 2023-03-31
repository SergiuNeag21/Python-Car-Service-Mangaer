from Domain.masina import Masina


class MasinaValidatorError(Exception):
    pass


class MasinaValidator:
    def valideaza(self, masina: Masina):
        """
        Functia verifica daca datele introduse sunt
        corecte si returneaza erorile
        :param masina: o entitate
        """
        erori = []
        if masina.km < 0:
            erori.append("Kilometri masinii trebuie sa fie pozitivi ")
        if masina.anAchizitie <= 0:
            erori.append("Anul achizitiei trebuie sa fie un an pozitiv ")
        if masina.garantie not in ['da', 'nu']:
            erori. append("Garantia poate fi da sau nu")
        if len(erori) > 0:
            raise ValueError(erori)
