from Tests.test_domain import tests_domain
from Tests.test_functionalitati import test_all_functionalitati
from Tests.test_repository import test_repository
from Tests.test_service import test_service
from Tests.test_undoRedo import test_undo, test_redo


def test_all():
    """
    Functia ce cuprinde toate functile de test
    """
    test_repository()
    tests_domain()
    test_service()
    test_all_functionalitati()
    test_undo()
    test_redo()
