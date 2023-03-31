from Domain.CardClient import CardClient
from Domain.masina import Masina
from Domain.tranzactie import Tranzactie


def test_car_domain():
    """
    Functie test domain car
    """

    car = Masina('1', 'audi', 2011, 12000, 'da')

    assert car.idEntitate == '1'
    assert car.model == 'audi'
    assert car.anAchizitie == 2011
    assert car.km == 12000
    assert car.garantie == 'da'


def test_card_domain():
    """
    Functie test domain card
    """

    card_client = CardClient('1', 'Neag', 'Sergiu',
                             1234567890111, '21.05.2002', '05.02.2021')

    assert card_client.idEntitate == '1'
    assert card_client.nume == 'Neag'
    assert card_client.prenume == 'Sergiu'
    assert card_client.CNP == 1234567890111
    assert card_client.dataNasterii == '21.05.2002'
    assert card_client.dataInregistrarii == '05.02.2021'


def test_tranzactie_domain():
    """
    Functie test domain tranzactie
    """

    trazactie = Tranzactie('1', '1', '1', 1000, 1000, '12.12.2012.12.12')

    assert trazactie.idEntitate == '1'
    assert trazactie.id_masina == '1'
    assert trazactie.id_card_client == '1'
    assert trazactie.suma_piese == 1000
    assert trazactie.suma_manopera == 1000
    assert trazactie.data == '12.12.2012.12.12'


def tests_domain():
    """
    Funcite test tot domain-ul
    """
    test_car_domain()
    test_card_domain()
    test_tranzactie_domain()
