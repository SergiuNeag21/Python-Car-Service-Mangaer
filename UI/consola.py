from datetime import datetime

from Domain.CardValidator import CardClientValidationError
from Domain.MasinaValidator import MasinaValidatorError
from Repository.Exceptions import NoSuchIDError, \
    DublicateCNPError, DublicateIDError
from Service.cardClientService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService


class Consola:
    def __init__(self, masinaService: MasinaService,
                 cardClientService: CardClientService,
                 tranzactieService: TranzactieService,
                 undoRedoService: UndoRedoService):
        self.__masinaService = masinaService
        self.__cardClientService = cardClientService
        self.__tranzactieService = tranzactieService
        self.__undoRedoService = undoRedoService

    def runMenu(self):
        while True:
            print(" ")
            print("1.CRUD masini")
            print("2.CRUD Card Client")
            print("3.CRUD Tranzactie")
            print("4. Cautare Full Text pentru masini si carduri ")
            print("5. Afisarea tranzactiilor cu suma cuprinsa in interval ")
            print("6. Afisare masini descrescator dupa suma manopera ")
            print("7. Afisare carduri descrescator dupa suma discount ")
            print("8. Sterge tranzactii dintr-un interval de zile ")
            print("9. Actualizeaza garantia")
            print("c. Sterge in cascada ")
            print("u. Undo ")
            print("r. Redo")
            print("x. iesire")
            optiune = input("Dati optiune: ")

            if optiune == "1":
                self.runCRUDMasiniMenu()
            elif optiune == "2":
                self.runCrudCardClientMenu()
            elif optiune == "3":
                self.runCrudTranzactieMenu()
            elif optiune == "4":
                self.uiSearchFullText()
            elif optiune == "5":
                self.handle_show_all_transactions_by_sum()
            elif optiune == "6":
                self.uiAfiseazaDescrescatorMasiniDupaMAnopera()
            elif optiune == "7":
                self.uiAfiseazaDescrescatorCarduriDupaDiscount()
            elif optiune == "8":
                self.uiStergeTranzactiiDinInterval()
            elif optiune == "9":
                self.uiActualizareGarantie()
            elif optiune == "c":
                self.handle_delete_cascada()
            elif optiune == "u":
                self.__undoRedoService.undo()
            elif optiune == "r":
                self.__undoRedoService.redo()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def runCRUDMasiniMenu(self):
        while True:
            print(" ")
            print("1. Adauga masina")
            print("2. Sterge masina")
            print("3. Modifica masina")
            print("g. Generaza masini random")
            print("a. Afiseaza toate masinile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaMasina()
            elif optiune == "2":
                self.uiStergeMasina()
            elif optiune == "3":
                self.uiModificaMasina()
            elif optiune == "g":
                self.runGenerareMasini()
            elif optiune == "a":
                self.showAllMasini()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def uiAdaugaMasina(self):
        try:
            print(" ")
            idMasina = input("Dati id-ul masinii: ")
            model = input("Dati modelul masinii: ")
            anAchizitie = int(input("Dati anul de achitizie al masinii: "))
            km = int(input("Dati km masinii: "))
            garantie = input("(da/nu) daca masina are garantie: ")

            self.__masinaService. \
                adauga(idMasina, model, anAchizitie, km, garantie)
        except MasinaValidatorError as me:
            print("Eroare de validare", me)
        except DublicateIDError as di:
            print("Acest id este deja existent: ", di)
        except Exception as e:
            print(e)

    def uiActualizareGarantie(self):
        self.__masinaService.actualizareGarantie()

    def runGenerareMasini(self):
        try:
            n = int(input("Alegeti un numar de masini: "))
            self.__masinaService.generareMasini(n)
            self.showAllMasini()

        except DublicateIDError as ve:
            print('Eroare', ve)
        except Exception as e:
            print(e)

    def uiStergeMasina(self):
        try:
            print(" ")
            idMasina = input("Dati id-ul masinii de sters: ")
            self.__masinaService.sterge(idMasina)
        except NoSuchIDError as ke:
            print("Nu exista id-ul dat: ", ke)
        except Exception as e:
            print(e)

    def uiModificaMasina(self):
        try:
            print(" ")
            idMasina = input("Dati id-ul masinii de modificat: ")
            model = input("Dati noul model al masinii: ")
            anAchizitie = int(input("Dati noul an de achitizie al masinii: "))
            km = int(input("Dati noii km masinii: "))
            garantie = input("Da sau nu daca masina are garantie: ")

            self.__masinaService.modifica(idMasina,
                                          model,
                                          anAchizitie,
                                          km,
                                          garantie)
        except MasinaValidatorError as me:
            print("Eroare de validare", me)
        except NoSuchIDError as ke:
            print("Nu exista card cu acest id: ", ke)
        except DublicateIDError as di:
            print("Acest id este deja existent: ", di)
        except Exception as e:
            print(e)

    def showAllMasini(self):
        print(' ')
        for masina in self.__masinaService.getAll():
            print(masina)

    def runCrudCardClientMenu(self):
        while True:
            print(" ")
            print("1. Adauga Card")
            print("2. Sterge Card")
            print("3. Modifica Card")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaCard()
            elif optiune == "2":
                self.uiStergeCardClient()
            elif optiune == "3":
                self.uiModificaCardClient()
            elif optiune == "a":
                self.showAllCards()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def uiAdaugaCard(self):
        print(" ")
        try:
            idCard = input("Dati id-ul cardului: ")
            nume = input("Dati numele clientuli: ")
            prenume = input("Dati prenumele clientului: ")
            CNP = int(input("Dati CNP-ul clientului: "))
            dataNasterii = datetime.strptime(
                input("Data nasterii a clientului (dd.mm.yyyy): "),
                "%d.%m.%Y")
            dataInregistraii = datetime.strptime(
                input("Data intregistrarii a clientului (dd.mm.yyyy): "),
                "%d.%m.%Y")

            self.__cardClientService.adauga(idCard,
                                            nume,
                                            prenume,
                                            CNP,
                                            dataNasterii,
                                            dataInregistraii)
        except CardClientValidationError as ve:
            print("Eroare de validare: ", ve)
        except DublicateCNPError as ce:
            print("CNP-ul este dublicat!: ", ce)
        except Exception as e:
            print(e)

    def uiStergeCardClient(self):
        print(" ")
        try:
            idCard = int(input("Dati id-ul cardului de sters: "))
            self.__cardClientService.sterge(idCard)
        except NoSuchIDError as ke:
            print("Nu exista card cu acest id: ", ke)
        except Exception as e:
            print(e)

    def uiModificaCardClient(self):
        try:
            print(' ')
            idCard = input("Dati id-ul cardului de modificat: ")
            nume = input("Dati numele clientuli modificat: ")
            prenume = input("Dati prenumele clientului modificat: ")
            CNP = int(input("Dati CNP-ul clientului modificat: "))
            dataNasterii = datetime.strptime(
                input("Data nasterii a clientului (dd.mm.yyyy): "), "%d.%m.%Y")
            dataInregistraii = datetime.strptime(
                input("Data intregistrarii a clientului (dd.mm.yyyy): "),
                "%d.%m.%Y")

            self.__cardClientService.\
                modifica(idCard, nume, prenume,
                         CNP, dataNasterii, dataInregistraii)
        except CardClientValidationError as ve:
            print("Eroare de validare:", ve)
        except NoSuchIDError as ne:
            print("ID inexistent:", ne)
        except DublicateCNPError as dc:
            print("CNP-ul exista deja: ", dc)
        except Exception as e:
            print("Eroare: ", e)

    def showAllCards(self):
        print(' ')
        for card in self.__cardClientService.getAll():
            print(card)

    def runCrudTranzactieMenu(self):
        while True:
            print(" ")
            print("1. Adauga tranzactie")
            print("2. Sterge tranzactie")
            print("3. Modifica tranzactie")
            print("a. Afiseaza toate tranzactie")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaTranzactie()
            elif optiune == "2":
                self.uiStergeTranzactie()
            elif optiune == "3":
                self.uiModificaTranzactie()
            elif optiune == "a":
                self.showAllTranzactie()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def uiAdaugaTranzactie(self):
        try:
            print(" ")
            id_tranzactie = input("Dati id-ul tranzactiei: ")
            id_masina = input("Dati id-ul masinii: ")
            id_card_client = input("Dati id-ul cardului client: ")
            suma_piese = int(input("Dati suma pieselor: "))
            suma_manopera = int(input("Dati suma manopera: "))
            data = datetime.strptime(
                input("Data si ora la care s-a facut tranzactia"
                      " (dd.mm.yyyy.hh.MM): "),
                "%d.%m.%Y.%H.%M")

            self.__tranzactieService.\
                adauga(id_tranzactie, id_masina, id_card_client,
                       suma_piese, suma_manopera,
                       data.strftime("%d.%m.%Y.%H.%M"))
        except ValueError as ve:
            print(ve)
        except NoSuchIDError as ke:
            print("Id-ul masinii nu exista: ", ke)
        except Exception as e:
            print(e)

    def uiStergeTranzactie(self):
        print(" ")
        try:
            id_tranzactie = input("Dati id-ul tranzactiei de sters: ")
            self.__tranzactieService.sterge(id_tranzactie)
        except NoSuchIDError as ke:
            print("Nu exista acest Id: ", ke)
        except Exception as e:
            print(e)

    def uiModificaTranzactie(self):
        print(" ")
        try:
            id_tranzactie = input("Dati id-ul tranzactiei de modificat: ")
            id_masina = input("Dati noul id al masinii: ")
            id_card_client = int(input("Dati noul card client: "))
            suma_piese = int(input("Dati noua suma a pieselor: "))
            suma_manopera = int(input("Dati noua suma a manoperei: "))
            data = datetime.strptime(
                input("Dati noua data si ora (dd.mm.yyyy.HH.MM): "),
                "%d.%m.%Y.%H.%M")

            self.__tranzactieService.modifica(id_tranzactie, id_masina,
                                              id_card_client, suma_piese,
                                              suma_manopera, data)
        except ValueError as ve:
            print(ve)
        except NoSuchIDError as ke:
            print("Id-ul masinii nu exista: ", ke)
        except Exception as e:
            print(e)

    def showAllTranzactie(self):
        print(' ')
        for tranzactie in self.__tranzactieService.getAll():
            print(tranzactie)

    def handle_show_all_transactions_by_sum(self):
        """
        3.5
        Afisare toate tranzactiile dintr-un interval dat in functie de suma
        """
        try:
            start = float(input('Capul inferior al intervalului: '))
            finish = float(input('Capul superior al intervalului: '))
            lista = self.__tranzactieService.\
                afisareTranzSumaInInterval(start, finish)
            print(lista)
        except ValueError as ve:
            print(ve)
        except NoSuchIDError as ke:
            print("Id-ul masinii nu exista: ", ke)
        except Exception as e:
            print(e)

    def uiSearchFullText(self):
        """
        Cautare full text
        :return:
        """
        try:
            cuv = input("Alegeti un cuvant pentru a-l cauta: ")
            lista = self.__tranzactieService.cautareFullText(cuv)
            for elem in lista:
                print(elem)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiAfiseazaDescrescatorMasiniDupaMAnopera(self):
        """
        Functie afisare masini ordonate desc. dupa suma manopera
        descrescator RECURSIV
        :return: Masinilie afisate descrescator dupa suma manopera
        """
        lista = self.__tranzactieService.ordonareMasiniDupaManoperaRecursiv()
        for elem in lista:
            print(elem)

    def uiAfiseazaDescrescatorCarduriDupaDiscount(self):
        """
        Functie afisare carduri ordonate desc. dupa discount
        :return:
        """
        lista = self.__tranzactieService.afisareCarduriDupaReduceri()
        for elem in lista:
            print(elem)

    def uiStergeTranzactiiDinInterval(self):
        """
        Functie de stergere a tuturor tranzactiilor dintr-un interval de timp
        :return:
        """

        try:
            date1 = int(input('Dati ziua de la care sa se stearga: '))
            date2 = int(input('Dati ziua pana la care sa se stearga '))
            self.__tranzactieService.del_all_trans(date1, date2)

            print()
            print('Tranzactiile au fost sterse!')

        except ValueError as ve:
            print('Eroare de validare: ', ve)
        except DublicateIDError as di:
            print('Eroare de cheie: ', di)
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_delete_cascada(self):
        """
        Functie delete cascada
        :return:
        """
        try:
            id_de_sters = input('Dati id-ul ce doriti sa-l stergeti: ')
            self.__tranzactieService.stergeInCascada(id_de_sters)
            self.__masinaService.sterge(id_de_sters)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
