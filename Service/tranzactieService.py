import datetime

from Domain.addOperation import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Domain.multiDelete import MultiDelete
from Domain.tranzactie import Tranzactie
from Repository.repository import Repository
from Service.masinaService import MasinaService
from Service.undoRedoService import UndoRedoService
from utils import my_sorted


class TranzactieService:
    def __init__(self, tranzactieRepository: Repository,
                 masinaRepository: Repository,
                 cardClientRepository: Repository,
                 undoRedoService: UndoRedoService,
                 masinaService: MasinaService):
        self.__tranzactieRepository = tranzactieRepository
        self.__masinaRepository = masinaRepository
        self.__cardClientRepository = cardClientRepository
        self.__undoRedoService = undoRedoService
        self.__masinaService: masinaService

    def getAll(self):
        """
        Introduce
        """
        return self.__tranzactieRepository.read()

    def adauga(self, id_tranzactie, id_masina,
               id_card, suma_piese, suma_manopera, data):
        """
        Adauga o tranzactie.
        Dacă există un card client, atunci aplicați o reducere de `10%`
        pentru manoperă.
        Dacă mașina este în garanție, atunci piesele sunt gratis.
        Se tipărește prețul plătit și reducerile acordate.
        :param id_tranzactie: id-ul tranzactiei
        :param id_masina: id-ul masinii
        :param id_card: id-ul cardului client
        :param suma_piese: suma pieselor masinii
        :param suma_manopera: suma manoperei pentru masina
        :param data: data si ora tranzactiei
        :return: tranzactia adaugata in dicitonarul de tranzactii.
        """
        if id_card:
            suma_manopera = suma_manopera - 0.1 * suma_manopera

        masina = self.__masinaRepository.read(id_masina)

        if masina.garantie == "da":
            suma_piese = 0

        tranzactie = Tranzactie(id_tranzactie, id_masina,
                                id_card, suma_piese, suma_manopera, data)
        self.__tranzactieRepository.adauga(tranzactie)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__tranzactieRepository, tranzactie))

    def sterge(self, id_tranzactie):
        tranzactie_stearsa = self.__tranzactieRepository.read(id_tranzactie)
        self.__tranzactieRepository.sterge(id_tranzactie)
        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__tranzactieRepository, tranzactie_stearsa))

    def modifica(self, id_tranzactie, id_masina, id_card,
                 suma_piese, suma_manopera, data):
        """
        Modifica o tranzactie.
        Dacă există un card client, atunci aplicați o reducere de `10%`
        pentru manoperă.
        Dacă mașina este în garanție, atunci piesele sunt gratis.
        Se tipărește prețul plătit și reducerile acordate.
        :param id_tranzactie: id-ul tranzactiei de modificat
        :param id_masina: id-ul noii masini
        :param id_card: id-ul noului card client
        :param suma_piese: noua suma a pieselor
        :param suma_manopera: noua suma a manoperei
        :param data: noua data a tranzactei
        :return: tranzactia modificata in dictionarul de tranzactii.
        """
        tranzactie_veche = self.__tranzactieRepository.read(id_tranzactie)
        if self.__masinaRepository.read(id_masina) is None:
            raise KeyError("Nu exista masina cu id-ul dat")

        exista_id_card = self.__cardClientRepository.read(id_card)

        if exista_id_card:
            suma_manopera = suma_manopera - 0.1 * suma_manopera
        print(f"Ati platit {suma_manopera} pentru manopera. ")

        masina = self.__masinaRepository.read(id_masina)

        if masina.in_garantie == "da":
            suma_piese = 0
            print("Masina este in garantie si piesele sunt gratis. ")
        else:
            print(f"Ati platit {suma_piese} pentru piese. ")
        tranzactie = Tranzactie(id_tranzactie, id_masina,
                                id_card, suma_piese, suma_manopera, data)
        self.__tranzactieRepository.modifica(tranzactie)
        self.__tranzactieRepository.modifica(tranzactie)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(
                self.__tranzactieRepository, tranzactie_veche, tranzactie))

    def show_transaction(self, id: str):
        return self.__tranzactieRepository.read(id)

    def show_all_transactions(self):
        """
        Functie afisare toate tranzactii
        :return:
        """
        return self.__tranzactieRepository.read()

    def del_all_trans(self, a, b):
        """
        Șterge toate tranzacțiile dintr-un anumit interval de zile.
        :param a: ziua de la care sa inceapa stergerea
        :param b: ziua pana la care sa se stearga
        :return: tranzactiile fara cele care au ziua
        in interiorul [a,b]
        """
        tranzactie_stearsa = []
        for tranzactie in self.__tranzactieRepository.read():
            data_completa = tranzactie.data
            data_formatata = datetime.datetime\
                .strptime(str(data_completa), "%d.%m.%Y.%H.%M")
            zi = data_formatata.day
            if a <= zi <= b:
                tranzactie_stearsa.append(tranzactie)
                self.__tranzactieRepository.\
                    sterge(tranzactie.idEntitate)
            self.__undoRedoService.addUndoOperation(
                MultiDelete(self.__tranzactieRepository,
                            tranzactie_stearsa))

        return self.getAll()

    def stergeInCascada(self, masina_sters):
        """
        Cand sterg o entitate sa stearga toate
        tranzactiile care implica acea entitate.
        :param masina_sters: entitatea de sters
        :return: tranzactiile fara cele care contin masina respectiva.
        """
        for tranzactie in self.__tranzactieRepository.read():
            if tranzactie.id_masina == masina_sters:
                tranzactie_stearsa = \
                    self.__tranzactieRepository.read(tranzactie.idEntitate)
                self.__tranzactieRepository.sterge(tranzactie.idEntitate)
                self.__undoRedoService.addUndoOperation(
                    DeleteOperation(self.__tranzactieRepository,
                                    tranzactie_stearsa)
                )

    # filter
    def cautareFullText(self, cuv):
        """
        Cauta stringul 'cuv' in caracteristicile masinilor
        si ale cardurilor client.
        :param cuv: stringul de cautat
        :return: obiectele care contin stringul dat.
        """
        masini = self.__masinaRepository.read()
        listaMasini = list(filter(lambda x:
                           cuv in x.model or cuv in x.garantie or
                           cuv in str(x.km) or cuv in
                           str(x.anAchizitie), masini))

        carduri = self.__cardClientRepository.read()
        listaCarduri = list(filter(lambda x:
                                   cuv in x.prenume or cuv in str(x.CNP) or cuv
                                   in str(x.dataNasterii) or cuv in
                                   str(x.dataInregistrarii), carduri))

        return listaMasini + listaCarduri

    # list comprehension
    def afisareTranzSumaInInterval(self, start, finish):
        """
        Afisare tranzactii cu suma manoperei + suma pieselor
         cuprinsa in interval
        :param start: capatul stang al intervalului
        :param finish: capatul drept al intervalului
        :return: lista de tranzactii ce respecta proprietatea data
        """
        tranzactii = self.getAll()
        rezultat = [tranzactie for tranzactie in
                    tranzactii if start < (tranzactie.suma_manopera
                                           + tranzactie.suma_piese) < finish]
        return rezultat

    # Recursivitate
    def ordonareMasiniDupaManoperaRecursiv(self):
        trans = self.__tranzactieRepository.read()
        masini = self.__masinaRepository.read()

        def inner(cars):
            if not cars:
                return []

            masina = cars[0]

            suma_manopera_list = [tran.suma_manopera for tran in trans
                                  if masina.idEntitate == tran.id_masina]
            total_sum_manopera = sum(suma_manopera_list)
            return[(masina.idEntitate, total_sum_manopera)] + inner(cars[1:])

        masini_manopera = inner(masini)

        return my_sorted(masini_manopera, key=lambda x: x[1], reverse=True)

    def orodonareMasiniDupaManopera(self):
        """
        Ordoneaza masinile dupa suma manoperei.
        :return: lista sortata descrescator cu dictionare care au chei masina
        si valoarea suma platita pentru manopera.
        """
        rezultat = []
        sumaPerMasini = {}

        for masina in self.__masinaRepository.read():
            sumaPerMasini[masina.idEntitate] = 0

        for tranzactie in self.__tranzactieRepository.read():
            sumaPerMasini[tranzactie.id_masina] += tranzactie.suma_manopera

        for id_masina in sumaPerMasini:
            rezultat.append({
                "masina": self.__masinaRepository.read(id_masina),
                "suma manopera": sumaPerMasini[id_masina]
            })

        return my_sorted(rezultat, key=lambda suma: suma["suma manopera"],
                         reverse=True)

    def afisareCarduriDupaReduceri(self):
        """
        Afișarea cardurilor client ordonate descrescător "
        "după valoarea reducerilor obținute
        :return: lista ordonata cu dictionare care au chei cardul client
        si reducerile respective.
        """
        reduceri = {}
        rezultat = []

        for cardClient in self.__cardClientRepository.read():
            reduceri[cardClient.idEntitate] = 0
        for tranzactie in self.__tranzactieRepository.read():
            reduceri[tranzactie.id_card_client] += \
                10/9*tranzactie.suma_manopera - tranzactie.suma_manopera

        for id_card in reduceri:
            rezultat.append({
                "Card Client": self.__cardClientRepository.read(id_card),
                "Reduceri": reduceri[id_card]
            })
        return my_sorted(rezultat, key=lambda reducere: reducere["Reduceri"],
                         reverse=True)
