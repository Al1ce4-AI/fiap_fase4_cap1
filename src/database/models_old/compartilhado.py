from enum import StrEnum


class TipoCultura(StrEnum):
    CANA_DE_ACUCAR = "cana"

    def __str__(self):

        if self.value == "cana":
            return "Cana-de-Açúcar"

        return super().name

class FormatoArea(StrEnum):
    RETANGULO = "retangulo"
    TRIANGULO = "triangulo"

    def __str__(self):

        if self.value == "retangulo":
            return "Retângulo"

        if self.value == "triangulo":
            return "Triângulo Retângulo"

        return super().name

class UnidadesInsumo(StrEnum):
    TONELADA = "t"
    KILO = "kg"
    GRAMAS = "g"
    LITRO = "l"
    ML = "ml"

    def __str__(self):

        if self.value == "t":
            return "Tonelada"

        if self.value == "kg":
            return "Quilo"

        if self.value == "g":
            return "Gramas"

        if self.value == "l":
            return "Litro"

        if self.value == "ml":
            return "Mililitro"

        return super().name