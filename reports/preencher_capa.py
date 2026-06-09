from pathlib import Path

from docx import Document


path = Path(__file__).resolve().parent / "Relatorio_Projeto_A3_Comite_Classificadores.docx"
doc = Document(path)

replacements = {
    "Integrantes: [Preencher nomes dos integrantes]": (
        "Integrante: Gustavo Fernandes Borrelly dos Santos - RA: 824213782"
    ),
    "Professor(a): [Preencher nome do(a) professor(a)]": (
        "Professor: Marcelo Duduchi Feitosa"
    ),
}

for paragraph in doc.paragraphs:
    if paragraph.text in replacements:
        new_text = replacements[paragraph.text]
        if paragraph.runs:
            paragraph.runs[0].text = new_text
            for run in paragraph.runs[1:]:
                run.text = ""
        else:
            paragraph.text = new_text
    elif paragraph.text == "Turma: [Preencher turma]":
        element = paragraph._element
        element.getparent().remove(element)

doc.save(path)
print(path)
