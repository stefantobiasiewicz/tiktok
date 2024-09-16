from html2image import Html2Image
from jinja2 import Template


def render_html_to_image(html_content, output_image, width, height):
    # Ustawienie rozmiaru podczas tworzenia instancji
    hti = Html2Image(size=(width, height))

    # Renderowanie HTML do obrazu
    hti.screenshot(html_str=html_content, save_as=output_image)


def main():
    # Wczytaj HTML z pliku
    with open('template.html', 'r') as file:
        template_content = file.read()

    # Tworzenie szablonu Jinja2
    template = Template(template_content)

    # Dane do szablonu
    html_content = template.render(
        name="Jan Kowalski",
        fC="1234",
        lC="5678",
        followingCount="90",
        videoCount="12"
    )

    output_image = "output.png"
    width = 250
    height = 122

    # Renderowanie HTML na obraz
    render_html_to_image(html_content, output_image, width, height)


if __name__ == "__main__":
    main()
