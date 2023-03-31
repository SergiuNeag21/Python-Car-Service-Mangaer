from Domain.CardClient import CardClient
from Domain.CardValidator import CardClientValidator
from Domain.addOperation import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Repository.Exceptions import DublicateCNPError

from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class CardClientService:
    def __init__(self, cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 undoRedoService: UndoRedoService):
        self.__cardClientRepository = cardClientRepository
        self.__cardClientValidator = cardClientValidator
        self.__undoRedoService = undoRedoService

    def cnp_unic(self, cnp=None):
        """
        Verifica daca cnp-ul este unic
        :param cnp: cnp-ul clientului
        :return: True daca cnp-ul este unc si false altfel
        """
        cards = self.__cardClientRepository.read()

        for elem in cards:
            if elem.CNP == cnp:
                return False
        return True

    def getAll(self):
        return self.__cardClientRepository.read()

    def adauga(self, idCard, nume, prenume,
               CNP, dataNasterii, dataInregistrarii):
        """
        Adauga un card in fisier
        :param: Datele cardului
        """
        if self.cnp_unic(CNP) is False:
            raise DublicateCNPError(f'Exista deja un client cu CNP-ul '
                                    f' {CNP}')

        card = CardClient(idCard, nume, prenume,
                          CNP, dataNasterii, dataInregistrarii)
        self.__cardClientValidator.valideaza(card)
        self.__cardClientRepository.adauga(card)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__cardClientRepository, card))

    def sterge(self, idCard):
        """
        Sterege un card
        :param idCard: id-ul cardului de sters
        :return: Stergerea cardului din multimea de carduri
        """
        card_sters = self.__cardClientRepository.read(idCard)
        self.__cardClientRepository.sterge(idCard)
        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__cardClientRepository, card_sters))

    def modifica(self, idCard, nume, prenume,
                 CNP, dataNasterii, dataInregistrarii):
        """
        Modifica un card in fisier
        :param: Datele cardului
        """
        cardVechi = self.__cardClientRepository.read(idCard)
        card = CardClient(idCard, nume, prenume,
                          CNP, dataNasterii, dataInregistrarii)
        self.__cardClientValidator.valideaza(card)
        self.__cardClientRepository.modifica(card)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__cardClientRepository, cardVechi, card))

    def show_card(self, cardId):
        """
        Functia de afisare a unui card
        """
        return self.__cardClientRepository.read(cardId)
