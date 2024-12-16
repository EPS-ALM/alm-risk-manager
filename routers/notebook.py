import logging
import os

from fastapi import APIRouter, status, Response

router = APIRouter()

@router.get("/notebook/{notebook_name}", tags=["Notebook"],status_code=status.HTTP_200_OK)
def get_notebook(notebook_name: str):
    try:
        if notebook_name.endswith(".ipynb"): notebook_name = notebook_name.replace(".ipynb", ".html")
        elif not notebook_name.endswith(".html"): notebook_name += ".html"

        if notebook_name in os.listdir("notebooks_html"):
            with open(f"notebooks_html/{notebook_name}", "r") as f:
                notebook_html = f.read()
            return Response(content=notebook_html, media_type="text/html")
        else:
            logging.warning(f"Notebook {notebook_name} not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)