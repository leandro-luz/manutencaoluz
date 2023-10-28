def atributo_existe(objeto1, atributo, subatributo):
    """Função que realiza uma busca do objeto e do atributo vinculado ao modelo"""
    if hasattr(objeto1, atributo):
        objeto2 = getattr(objeto1, atributo)
        if hasattr(objeto2, subatributo):
            return getattr(objeto2, subatributo)
    return None
