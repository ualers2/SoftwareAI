#!/usr/bin/env python3
"""
Script para adicionar docstrings padrão a todos os módulos, classes e funções
do pacote softwareai_engine_library, sem alterar a lógica existente.
"""
import os
import ast


def ensure_docstrings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        src = f.read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return

    changed = False
    # Adiciona docstring de módulo se ausente
    if ast.get_docstring(tree) is None:
        module_doc = ast.Expr(
            value=ast.Constant(
                value=f"Módulo {os.path.basename(file_path)[:-3]}. TODO: adicionar descrição.",
                kind=None
            )
        )
        tree.body.insert(0, module_doc)
        changed = True

    for node in ast.walk(tree):
        # Classes, funções normais e assíncronas
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node) is None:
                name = getattr(node, 'name', '<anon>')
                kind = 'Classe' if isinstance(node, ast.ClassDef) else 'Função'
                doc = ast.Expr(
                    value=ast.Constant(
                        value=f"{kind} {name}. TODO: adicionar descrição.",
                        kind=None
                    )
                )
                # Insere docstring como primeiro elemento do corpo
                node.body.insert(0, doc)
                changed = True

    if changed:
        try:
            new_src = ast.unparse(tree)
        except AttributeError:
            # Para versões de Python sem ast.unparse
            import astor

            new_src = astor.to_source(tree)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_src)


def main():
    root = 'softwareai_engine_library'
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.endswith('.py'):
                path = os.path.join(dirpath, file)
                ensure_docstrings(path)


if __name__ == '__main__':
    main()