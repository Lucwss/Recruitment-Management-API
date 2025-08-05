from abc import abstractmethod, ABC

class IPDFGenerator(ABC):
    """
    Interface responsible for PDFGenerator methods.
    """

    @abstractmethod
    def generate_pdf(self, *args, **kwargs) -> None:
        """Generate a PDF from a content."""
        raise NotImplementedError()