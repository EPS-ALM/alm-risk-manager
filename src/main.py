from fastapi import FastAPI

import notebook

app = FastAPI()

app.include_router(notebook.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "mensagem": "APP IS RUNNING"
    }
