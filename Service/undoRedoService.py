from Domain.undoRedoOperation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.__undoOperations = []
        self.__redoOperations = []

    def addUndoOperation(self, undoRedoOperation: UndoRedoOperation):
        self.__undoOperations.append(undoRedoOperation)
        self.__redoOperations.clear()

    def undo(self):
        if self.__undoOperations:
            undoOperation = self.__undoOperations.pop()
            self.__redoOperations.append(undoOperation)
            undoOperation.doUndo()

    def redo(self):
        if self.__redoOperations:
            redoOperation = self.__redoOperations.pop()
            self.__undoOperations.append(redoOperation)
            redoOperation.doRedo()
