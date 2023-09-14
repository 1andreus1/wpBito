"""
<h1>
Образец договора аренды квартиры с мебелью и бытовой техникой.
Коммунальные платежи включены в стоимость аренды квартиры.
Договор заключается между физическими лицами
/h1>

<embed
src="https://normativ24.ru/wp-content/uploads/2023/07/test.pdf"
type="application/pdf"
width="100%"
height="800px">
</embed>

<p>
Обратите внимание, что договор аренды квартиры составлен и проверен
юристами и является примерным, он может быть доработан с учетом конкретных
условий сделки. Администрация Сайта не несет ответственности за
действительность данного договора аренды квартиры, а также за его
соответствие требованиям законодательства Российской Федерации.
</p>

<h2>Скачать</h2>
<a class="download-link" href="download.docx">Скачать DOCX</a>
<a class="download-link" href="download.pdf">Скачать PDF</a>
"""
from typing import Optional

from bs4 import BeautifulSoup

from new_project.models import Contract

TEXT_WARNING = \
    'Обратите внимание, что {title} составлен и проверен ' \
    'юристами и является примерным, он может быть доработан с учетом конкретных ' \
    'условий сделки. Администрация Сайта не несет ответственности за действительность ' \
    'данного договора, а также за его соответствие требованиям ' \
    'законодательства Российской Федерации.'


class HTMLGeneratorBase:
    def __init__(self, contract: Contract):
        self.html_result = BeautifulSoup()
        self.contract = contract

    def new(self, name: str, **kwargs: dict):
        tag = self.html_result.new_tag(
            name,
            **kwargs
        )
        return tag

    def add(self, tag):
        self.html_result.append(tag)

    def add_tag(
            self,
            name: str,
            text: Optional[str] = None,
            **kwargs: dict
    ):
        tag = self.new(name, **kwargs)
        if text is not None:
            tag.string = text
        self.add(tag)

    def add_h(self, n: int, text: str):
        self.add_tag(f'h{n}', text=text)

    def add_p(self, text: str):
        self.add_tag('p', text=text)

    def add_a(self, link: str, text: str):
        self.add_tag(
            'a',
            text=text,
            href=link
        )

    def add_iframe(
            self,
            link: str,
            **kwargs: dict
    ):
        link = f"https://docs.google.com/gview?url={link}&embedded=true"
        self.add_tag(
            'iframe',
            src=link,
            **kwargs,
        )


class HTMLGenerator(HTMLGeneratorBase):
    def add_description_section(self):
        if self.contract.description:
            self.add_h(2, 'Описание документа:')
            self.add_p('. '.join(self.contract.description.split('. ')[1:]))

    def add_embedded_pdf(self):
        if self.contract.url_wp_pdf:
            self.add_iframe(
                link=self.contract.url_wp_pdf,
                type='application/pdf',
                width='100%',
                height='800px'
            )

    def add_self_section(self):
        self.add_p(
            TEXT_WARNING.format(
                title=self.contract.title.lower()
            )
        )

    def add_download_section(self):
        self.add_h(2, 'Скачать:')

        if self.contract.url_wp_docx:
            self.add_a(self.contract.url_wp_docx, 'Скачать DOCX')
            self.add_tag('br')

        if self.contract.url_wp_pdf:
            self.add_a(self.contract.url_wp_pdf, 'Скачать PDF')
            self.add_tag('br')

    def generate_html(self):
        self.add_description_section()
        self.add_embedded_pdf()
        self.add_self_section()
        self.add_download_section()
        return str(self.html_result)
