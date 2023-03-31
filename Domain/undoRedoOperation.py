from abc import ABC


class UndoRedoOperation(ABC):
    def doUndo(self):
        ...

    def doRedo(self):
        ...
