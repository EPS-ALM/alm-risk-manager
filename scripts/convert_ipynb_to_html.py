import os
from nbconvert import HTMLExporter
from nbformat import read

def convert_notebooks_to_html(notebook_dir, output_dir):
    """Converte todos os notebooks Jupyter de um diretório para HTML, sobrescrevendo se necessário."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for notebook_name in os.listdir(notebook_dir):
        if notebook_name.endswith(".ipynb"):
            notebook_path = os.path.join(notebook_dir, notebook_name)
            output_path = os.path.join(output_dir, notebook_name.replace(".ipynb", ".html"))

            # Validar se o arquivo está vazio
            if os.path.getsize(notebook_path) == 0:
                print(f"Arquivo vazio: {notebook_name}. Ignorando...")
                continue

            try:
                # Ler o notebook e convertê-lo em HTML
                with open(notebook_path, 'r', encoding='utf-8') as nb_file:
                    notebook = read(nb_file, as_version=4)

                html_exporter = HTMLExporter()
                html_data, _ = html_exporter.from_notebook_node(notebook)

                # Verificar se o arquivo HTML já existe e se o conteúdo é igual
                if os.path.exists(output_path):
                    with open(output_path, 'r', encoding='utf-8') as existing_html_file:
                        existing_html_data = existing_html_file.read()

                    # Se o conteúdo for idêntico, ignore
                    if html_data == existing_html_data:
                        print(f"Conteúdo inalterado: {output_path}. Ignorando...")
                        continue

                # Salvar o novo conteúdo
                with open(output_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_data)
                print(f"[NEW] Convertido: {notebook_name} -> {output_path}")

            except Exception as e:
                print(f"Erro ao converter {notebook_name}: {e}")

# Diretórios para notebooks e saída
notebook_dir = os.path.join("notebooks")
output_dir = os.path.join("notebooks", "notebooks_html")

convert_notebooks_to_html(notebook_dir, output_dir)
