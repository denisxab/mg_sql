from useconf import export_path

name_proj = "mg_sql"
version = "0.0.1"
auth = "Denis Kustov <denis-kustov@rambler.ru>"

EXPORT_PATH = (
    export_path(
        namefile='pyproject_toml',
        path="./",
        template=f"""
[tool.poetry]
name = "{name_proj}"
version = "{version}"
description = "Создание файлов конфигурация"
repository = "https://github.com/denisxab/{name_proj}.git"
documentation = "https://{name_proj}.readthedocs.io/ru/latest/index.html"
authors = ["{auth}"]
readme = "README.md"
exclude = [
    "{name_proj}/.idea",
    "{name_proj}/venv",
    "{name_proj}/.git",
    "{name_proj}/.gitignore",
    "{name_proj}/test",
    "{name_proj}/Makefile"
]

[tool.poetry.dependencies]
python = "^3.10"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"    
"""
    ),
    export_path(
        namefile='.gitignore',
        path="./",
        template=f"""
/.idea
/venvs
/dist
/__pycache__/
/{name_proj}/__pycache__/
{name_proj}.bin
/{name_proj}/main.build  
"""
    )
    , export_path(
        namefile='main.py',
        path=f"./{name_proj}",
        template=f"""
if __name__ == "__main__":
    print("{name_proj}")
"""
    )
    , export_path(
        namefile='README.md',
        path=f"./",
        template=f""""""
    )

)
