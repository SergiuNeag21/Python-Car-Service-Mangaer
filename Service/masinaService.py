import random


from Domain.MasinaValidator import MasinaValidator
from Domain.addOperation import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.masina import Masina
from Domain.modifyOperation import ModifyOperation

from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class MasinaService:
    def __init__(self, masinaRepository: Repository,
                 masinaValidator: MasinaValidator,
                 undoRedoService: UndoRedoService):
        self.__masinaRepository = masinaRepository
        self.__masinaValidator = masinaValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        """
        :return:
        """
        return self.__masinaRepository.read()

    def adauga(self, idMasina, model, anAchizitie, km, garantie):
        """
        Adauga o masina.
        :param idMasina: id-ul masinii
        :param model: modelul masinii
        :param anAchizitie: anul de achizitie al masinii
        :param km: nr de km ai masinii
        :param garantie: da, nu daca masina are garantie
        :return: masina adaugata in dictionarul de masini
        """
        masina = Masina(idMasina, model, anAchizitie, km, garantie)
        self.__masinaValidator.valideaza(masina)
        self.__masinaRepository.adauga(masina)
        self.__undoRedoService.addUndoOperation(AddOperation(
            self.__masinaRepository, masina))

    def sterge(self, idMasina):
        """
        Sterge o masina.
        :param idMasina: id ul masinii
        :return: Stergerea masinii din dictionarul de masini
        """
        def help_tool(x): return self.__masinaRepository.sterge(x)

        masina_stearsa = self.__masinaRepository.read(idMasina)
        help_tool(idMasina)

        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__masinaRepository, masina_stearsa))

    def modifica(self, idMasina, model, anAchizitie, km, garantie):
        """
        Modifica o masina.
        :param idMasina: id-ul masinii de modificat
        :param model: modelul masinii nou
        :param anAchizitie: anul de achizitie al masinii  nou
        :param km: nr de km ai masinii noi
        :param garantie: da, nu daca masina are garantie
        :return: masina modificata in dictionarul de masini
        """
        masina_veche = self.__masinaRepository.read(idMasina)
        masina = Masina(idMasina, model, anAchizitie, km, garantie)
        self.__masinaValidator.valideaza(masina)
        self.__masinaRepository.modifica(masina)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__masinaRepository, masina_veche, masina))

    def show_all_cars(self):
        """
        Functie afisare toate masinile
        :return:
        """
        return self.__masinaRepository.read()

    def show_car(self, carId):
        """
        Functie afisare masina
        :param carId:
        :return:
        """
        return self.__masinaRepository.read(carId)

    def actualizareGarantie(self):
        """
        Actualizeaza garantia masinilor. O masina este in garantie
        daca are maxim 3 ani sau maxim 60.000 km
        :return: Garantia actualizata
        """
        for masina in self.__masinaRepository.read():
            masina_veche = self.__masinaRepository.read(masina.idEntitate)
            if masina.km <= 60000 and masina.anAchizitie >= 2018:
                masina.garantie = "da"
            else:
                masina.garantie = "nu"
            self.__masinaRepository.modifica(masina)
            self.__undoRedoService.addUndoOperation(
                ModifyOperation(self.__masinaRepository, masina_veche,
                                masina))
        return self.getAll()

    def generareMasini(self, n):
        """
        Genereaza n masini.
        :param n: numarul de masini.
        :return: n masini random create.
        """
        i = 1
        while i <= n:
            id_masina = str(random.randrange(100))

            lstmodel = ["ford", "audi", "mercedes", "vw"]
            model = random.choice(lstmodel)

            lstan = [2000, 2001, 2009, 2008, 2003, 2020]
            an_achizitie = random.choice(lstan)

            lstnr_km = [100, 3, 0, 1000, 23.6, 34, 3]
            nr_km = random.choice(lstnr_km)

            lstin_garantie = ["da", "nu"]
            in_garantie = random.choice(lstin_garantie)

            masina = Masina(id_masina,
                            model,
                            an_achizitie,
                            nr_km,
                            in_garantie)

            if self.__masinaRepository.read(id_masina) is None:
                self.__masinaRepository.adauga(masina)
                i = i + 1
            else:
                i = i - 1
