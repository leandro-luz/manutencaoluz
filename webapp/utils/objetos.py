def atributo_existe(objeto1, atributo, subatributo):
    """Função que realiza uma busca do objeto e do atributo vinculado ao modelo"""
    if hasattr(objeto1, atributo):
        objeto2 = getattr(objeto1, atributo)
        if hasattr(objeto2, subatributo):
            return getattr(objeto2, subatributo)
    return None


def atribuir_none_id(valor):
    """Função que retorna none ou o valor do id"""
    if valor == 0:
        return None
    else:
        return valor
