import logging

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from webapp.usuario.models import PerfilAcesso, Senha, Usuario, TelaPerfilAcesso, PerfilManutentor
from webapp.empresa.models import Interessado, Tipoempresa, Empresa
from webapp.equipamento.models import Equipamento, Grupo, Subgrupo, Pavimento, Setor, Local
from webapp.contrato.models import Contrato, Tela, Telacontrato
from webapp.plano_manutencao.models import TipoData, Unidade, Periodicidade, PlanoManutencao, Atividade, \
    TipoParametro, ListaAtividade, TipoBinario
from webapp.ordem_servico.models import TipoSituacaoOrdem, FluxoOrdem, OrdemServico, TramitacaoOrdem, TipoOrdem, \
    TipoStatusOrdem, TipoSituacaoOrdemPerfilManutentor

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

from webapp import db


def criar_contrato(lista: List[dict]) -> List[Contrato]:
    """
       Cria novos contratos a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novos contratos.
       Returns:
           List[Contrato]: Lista de novos contratos criados e adicionados na base de dados.
       """

    novos_contratos = []

    for item in lista:
        if item['nome'] not in {c.nome for c in Contrato.query.all()}:
            empresa = Empresa.query.filter_by(razao_social=item['empresa']).one_or_none()

            if not empresa:
                empresa = Empresa()
                empresa.id = None

            contrato = Contrato(nome=item['nome'],
                                ativo=item['ativo'],
                                empresa_gestora_id=empresa.id
                                )
            novos_contratos.append(contrato)

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_contratos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_contratos)} contratos inseridos com sucesso.')

        # Retornando a lista de novos contratos adicionados
        return novos_contratos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir contratos: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_telas(lista: List[dict]) -> List[Tela]:
    """
          Cria novas telas a partir de uma lista de dicionários.
          Args:
              lista (List[dict]): Lista de dicionários contendo informações das novas telas.
          Returns:
              List[Tela]: Lista de novas telas criadas e adicionadas na base de dados.
          """
    # Criando uma lista de novas telas para serem adicionadas
    novas_telas = [Tela(nome=item['nome'],
                        icon=item['icon'],
                        url=item['url'],
                        posicao=item['posicao'])
                   for item in lista if item['nome'] not in {t.nome for t in Tela.query.all()}]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novas_telas)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_telas)} telas inseridas com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novas_telas
    except SQLAlchemyError as e:
        log.error(f'Erro ao inserir telas: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_telascontrato(lista: List[dict]) -> List[Telacontrato]:
    """
    Cria as relações entre as telas e os contratos na base de dados.
    Args:
        lista: Uma lista de dicionários contendo os dados das telas e dos contratos.
    Returns:
        Uma lista de objetos Telacontrato que foram adicionados à base de dados.
    """

    telascontratos_existentes = set((tc.tela_id, tc.contrato_id) for tc in Telacontrato.query.all())
    novas_telascontrato = []

    for item in lista:
        tela = Tela.query.filter_by(nome=item['tela']).first()
        contrato = Contrato.query.filter_by(nome=item['contrato']).first()

        if (tela.id, contrato.id) not in telascontratos_existentes:
            telacontrato = Telacontrato(tela=tela, contrato=contrato, ativo=True)
            novas_telascontrato.append(telacontrato)

    try:
        db.session.add_all(novas_telascontrato)
        db.session.commit()
        log.info(f'{len(novas_telascontrato)} telascontrato inseridas com sucesso.')
    except SQLAlchemyError as e:
        log.error(f'Erro ao inserir telacontrato: {e}')
        db.session.rollback()

    return novas_telascontrato


def criar_interessados(lista: List[dict]) -> List[Interessado]:
    """
   Cria novos tipos de empresas a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novos tipos.
   Returns:
       List[Interessado]: Lista de novos tipos de empresa criados e adicionados na base de dados.
   """
    # Criando a lista de novos interessados a serem adicionadas
    novos_interessados = [Interessado(nome_fantasia=item['nome_fantasia'],
                                      cnpj=item['cnpj'],
                                      email=item['email'],
                                      telefone=item['telefone'])
                          for item in lista if item['nome_fantasia'] not in [i.nome_fantasia
                                                                             for i in Interessado.query.all()]]

    try:
        # Adicionando as novos interessados na sessão e realizando o commit
        db.session.add_all(novos_interessados)
        db.session.commit()
        log.info(f'{len(novos_interessados)} Interessados inseridas com sucesso.')

        # Retornando a lista de novas interessados adicionadas
        return novos_interessados
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Interessados: {e}')
        db.session.rollback()
        return []


def criar_tipos_empresa(lista: List[dict]) -> List[Tipoempresa]:
    """
   Cria novos tipos de empresas a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novos tipos.
   Returns:
       List[Tipoempresa]: Lista de novos tipos de empresa criados e adicionados na base de dados.
   """

    # Criando a lista de novas periodicidades a serem adicionadas
    novos_tipos_empresa = [Tipoempresa(nome=item['nome'])
                           for item in lista if item['nome'] not in [tp.nome
                                                                     for tp in Tipoempresa.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novos_tipos_empresa)
        db.session.commit()
        log.info(f'{len(novos_tipos_empresa)} Tipos de empresas inseridas com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novos_tipos_empresa
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tipo de empresa: {e}')
        db.session.rollback()
        return []


def criar_empresas(lista: List[dict]) -> List[PerfilAcesso]:
    empresas_existentes = {emp.razao_social for emp in Empresa.query.all()}
    tipos_empresas = {tipo.nome: tipo for tipo in Tipoempresa.query.all()}
    contratos = {contrato.nome: contrato for contrato in Contrato.query.all()}

    empresas = [
        Empresa(
            razao_social=item['razao_social'],
            nome_fantasia=item['nome_fantasia'],
            cnpj=item['cnpj'],
            cep=item['cep'],
            logradouro=item['logradouro'],
            bairro=item['bairro'],
            municipio=item['municipio'],
            uf=item['uf'],
            numero=item['numero'],
            complemento=item['complemento'],
            email=item['email'],
            telefone=item['telefone'],
            ativo=True,
            data_cadastro=item['data_cadastro'],
            contrato=contratos[item['contrato']],
            tipoempresa=tipos_empresas[item['tipo']],
            empresa_gestora_id=Empresa.query.filter_by(razao_social=item['empresa_gestora']).first()
        )
        for item in lista
        if item['razao_social'] not in empresas_existentes
    ]

    try:
        db.session.add_all(empresas)
        db.session.commit()
        # log.info(f'{len(empresas)} Empresas inseridas com sucesso.')
        return empresas
    except Exception as e:
        log.error(f'Erro ao inserir Empresas: {e}')
        db.session.rollback()
        return []


def criar_perfis(lista: List[dict]) -> List[PerfilAcesso]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[PerfilAcesso]: Lista de novos perfis criados e adicionados na base de dados.
   """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando a lista de novas perfis a serem adicionadas
    novos_perfis = [PerfilAcesso(nome=item['nome'],
                                 descricao=item['descricao'],
                                 ativo=item['ativo'],
                                 empresa_id=empresas[item['empresa']])
                    for item in lista if item['nome'] not in [pe.nome
                                                              for pe in PerfilAcesso.query.all()]]

    try:
        # Adicionando as novas perfis na sessão e realizando o commit
        db.session.add_all(novos_perfis)
        db.session.commit()
        log.info(f'{len(novos_perfis)} Perfis inseridas com sucesso.')

        # Retornando a lista de novos perfis
        return novos_perfis
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir PerfilAcesso: {e}')
        db.session.rollback()
        return []


def criar_telasperfil(lista: List[dict]) -> List[TelaPerfilAcesso]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[PerfilAcesso]: Lista de novos perfis criados e adicionados na base de dados.
   """

    telasperfis = []

    for item in lista:
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one_or_none()
        perfilacesso = PerfilAcesso.query.filter_by(nome=item['role'], empresa_id=empresa.id).one_or_none()
        tela = Tela.query.filter_by(nome=item['tela']).one_or_none()
        telaperfil = TelaPerfilAcesso.query.filter_by(tela_id=tela.id, perfilacesso_id=perfilacesso.id).one_or_none()

        if not telaperfil:
            telasperfis.append(TelaPerfilAcesso(perfilacesso_id=perfilacesso.id, tela_id=tela.id, ativo=True))

    try:
        db.session.add_all(telasperfis)
        db.session.commit()
        log.info(f'{len(telasperfis)} TelasPerfil inseridas com sucesso.')
        return telasperfis
    except Exception as e:
        log.error(f'Erro ao inserir telaperfil: {e}')
        db.session.rollback()
        return []


def criar_senhas(lista: List[dict]) -> List[Senha]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[PerfilAcesso]: Lista de novos perfis criados e adicionados na base de dados.
   """

    # Criando a lista de novas perfis a serem adicionadas
    senhas_existentes = {se.senha for se in Senha.query.all()}
    novas_senhas = [Senha(senha=item['senha'],
                          data_expiracao=item['data_expiracao'],
                          senha_temporaria=item['senha_temporaria'],
                          senha_expira=item['senha_expira'])
                    for item in lista if item['senha'] not in senhas_existentes]

    try:
        db.session.add_all(novas_senhas)
        db.session.commit()
        log.info(f'{len(novas_senhas)} Senhas inseridas com sucesso.')
        # Retornando a lista de novas senhas
        return novas_senhas
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Senha: {e}')
        db.session.rollback()
        return []


def criar_usuarios(lista: List[dict]) -> List[Usuario]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}
    senhas = {s.senha: s.id for s in Senha.query.all()}
    usuarios = {u.nome: u.id for u in Usuario.query.all()}

    novos_usuarios = []
    for item in lista:
        if item['nome'] not in usuarios:
            perfis = {p.nome: p.id for p in PerfilAcesso.query.filter_by(empresa_id=empresas[item['empresa']])}

            usuario = Usuario(nome=item['nome'],
                              email=item['email'],
                              data_assinatura=item['data_assinatura'],
                              ativo=True,
                              senha_id=senhas[item['senha']],
                              perfilacesso_id=perfis[item['perfil']],
                              empresa_id=empresas[item['empresa']])

            novos_usuarios.append(usuario)

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_usuarios)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_usuarios)} Usuários inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_usuarios
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir usuario: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
    return []


def criar_perfil_manutentor(lista: List[dict]) -> List[PerfilManutentor]:
    # Criando a lista de novos perfis
    perfis_existentes = {pm.nome for pm in PerfilManutentor.query.all()}
    novos_perfis = [PerfilManutentor(nome=item['nome'])
                    for item in lista if item['nome'] not in perfis_existentes]

    try:
        db.session.add_all(novos_perfis)
        db.session.commit()
        log.info(f'{len(novos_perfis)} Perfis Manutentores inseridos com sucesso.')
        # Retornando a lista de novas senhas
        return novos_perfis
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Perfil Manutentor: {e}')
        db.session.rollback()
        return []


def criar_grupo(lista: List[dict]) -> List[Grupo]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_grupos = [Grupo(nome=item['nome'],
                          empresa_id=empresas[item['empresa']])
                    for item in lista if item['nome'] not in [gr.nome for gr in Grupo.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_grupos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_grupos)} Grupos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_grupos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir grupos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_subgrupo(lista: List[dict]) -> List[Subgrupo]:
    """
       Cria novos subgrupos.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações subgrupos.
       Returns:
           List[TipoData]: Lista subgrupos adicionados na base de dados.
       """

    grupos = {g.nome: g.id for g in Grupo.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_subgrupos = [Subgrupo(nome=item['nome'],
                                grupo_id=grupos[item['grupo']])
                       for item in lista if item['nome'] not in [sg.nome for sg in Subgrupo.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_subgrupos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_subgrupos)} Subgrupos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_subgrupos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Subgrupos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_pavimento(lista: List[dict]) -> List[Pavimento]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_pavimentos = [Pavimento(nome=item['nome'],
                                  sigla=item['sigla'],
                                  empresa_id=empresas[item['empresa']])
                        for item in lista if item['nome'] not in [pav.nome for pav in Pavimento.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_pavimentos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_pavimentos)} Pavimentos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_pavimentos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir pavimentos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_setor(lista: List[dict]) -> List[Setor]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_setores = [Setor(nome=item['nome'],
                           sigla=item['sigla'],
                           empresa_id=empresas[item['empresa']])
                     for item in lista if item['nome'] not in [s.nome for s in Setor.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_setores)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_setores)} Setores inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_setores
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir setores: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_locais(lista: List[dict]) -> List[Local]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_locais = [Local(nome=item['nome'],
                          sigla=item['sigla'],
                          empresa_id=empresas[item['empresa']])
                    for item in lista if item['nome'] not in [lo.nome for lo in Local.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_locais)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_locais)} Locais inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_locais
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir locais: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_equipamento(lista: List[dict]) -> List[Equipamento]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    subgrupos = {sg.nome: sg.id for sg in Subgrupo.query.all()}
    setores = {st.nome: st.id for st in Setor.query.all()}
    locais = {lo.nome: lo.id for lo in Local.query.all()}
    pavimentos = {p.nome: p.id for p in Pavimento.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_equipamentos = [Equipamento(cod=item['cod'],
                                      descricao_curta=item['short'],
                                      tag=item['tag'],
                                      subgrupo_id=subgrupos[item['subgrupo']],
                                      setor_id=setores[item['setor']],
                                      local_id=locais[item['local']],
                                      pavimento_id=pavimentos[item['pavimento']]
                                      )
                          for item in lista if item['cod'] not in [si.cod for si in Equipamento.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_equipamentos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_equipamentos)} Equipamentos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_equipamentos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir equipamentos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tipodata(lista: List[dict]) -> List[TipoData]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_tipodata = [TipoData(nome=item['nome'])
                      for item in lista if item['nome'] not in [tp.nome for tp in TipoData.query.all()]]
    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_tipodata)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_tipodata)} Tipo de data inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_tipodata
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir contratos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_unidades(lista: List[dict]) -> List[Unidade]:
    """
       Cria novas unidades a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das novas unidades.
       Returns:
           List[Unidade]: Lista de novas unidades criados e adicionados na base de dados.
       """
    # Criando uma lista de novas unidades para serem adicionados
    novas_unidade = [Unidade(nome=item['nome'])
                     for item in lista if item['nome'] not in [u.nome for u in Unidade.query.all()]]
    try:
        # Adicionando as novas unidades na sessão e realizando o commit
        db.session.add_all(novas_unidade)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_unidade)} unidades inseridas com sucesso.')

        # Retornando a lista de novas unidades adicionados
        return novas_unidade
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir unidades: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_periodicidades(lista: List[dict]) -> List[Periodicidade]:
    """
   Cria novas periodicidades a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novas periodicidades.
   Returns:
       List[Unidade]: Lista de novas periodicidades criados e adicionados na base de dados.
   """

    # Buscando todas as unidades existentes no banco de dados
    unidades = {u.nome: u.id for u in Unidade.query.all()}

    # Criando a lista de novas periodicidades a serem adicionadas
    novas_periodicidades = [Periodicidade(nome=item['nome'],
                                          tempo=item['tempo'],
                                          unidade_id=unidades[item['unidade']])
                            for item in lista if item['nome'] not in [p.nome
                                                                      for p in Periodicidade.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novas_periodicidades)
        db.session.commit()
        log.info(f'{len(novas_periodicidades)} periodicidades inseridas com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novas_periodicidades
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir periodicidades: {e}')
        db.session.rollback()
        return []


def criar_planosmanutencao(lista: List[dict]) -> List[PlanoManutencao]:
    # Buscando os objetos necessários
    tipodatas = {t.nome: t.id for t in TipoData.query.all()}
    periodicidades = {p.nome: p.id for p in Periodicidade.query.all()}
    equipamentos = {e.cod: e.id for e in Equipamento.query.all()}
    tipos_ordem = {to.sigla: to.id for to in TipoOrdem.query.all()}
    listas_atividades = {la.nome: la.id for la in ListaAtividade.query.all()}

    novos_planosmanutencao = [
        PlanoManutencao(nome=item['nome'],
                        codigo=item['codigo'],
                        ativo=item['ativo'],
                        tipodata_id=tipodatas[item['tipodata']],
                        data_inicio=item['data_inicio'],
                        total_tecnico=item['tecnicos'],
                        tempo_estimado=item['tempo'],
                        periodicidade_id=periodicidades[item['periodicidade']],
                        equipamento_id=equipamentos[item['equipamento']],
                        tipoordem_id=tipos_ordem[item['tipo_ordem']],
                        listaatividade_id=listas_atividades[item['lista']]
                        if item['lista'] else None)
        for item in lista if item['codigo'] not in [pm.código for pm in PlanoManutencao.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novos_planosmanutencao)
        db.session.commit()
        log.info(f'{len(novos_planosmanutencao)} planos de manutenção inseridos com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novos_planosmanutencao
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir periodicidades: {e}')
        db.session.rollback()
        return []


def criar_tipos_parametros(lista: List[dict]) -> List[TipoParametro]:
    """
       Cria novos tipos de parametros a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novos tipos de parametros.
       Returns:
           List[Unidade]: Lista de novos tipos de parametros criados e adicionados na base de dados.
       """

    # Criando uma lista de novas unidades para serem adicionados
    novos_tipos = [TipoParametro(nome=item['nome'])
                   for item in lista if item['nome'] not in [t.nome for t in TipoParametro.query.all()]]
    try:
        # Adicionando os novos tipos de atividade na sessão e realizando o commit
        db.session.add_all(novos_tipos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_tipos)} tipos de parametros inseridos com sucesso.')

        # Retornando a lista de novos tipos de atividades adicionados
        return novos_tipos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao tipo de parametros: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_lista_atividades(lista: List[dict]) -> List[ListaAtividade]:
    """
       Cria novas listas de atividades a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das novas listas de atividades
       Returns:
           List[Unidade]: Lista de novas listas de atividadescriados e adicionados na base de dados.
       """

    # Criando uma lista de novas unidades para serem adicionados
    novas_listas = [ListaAtividade(nome=item['nome'],
                                   data=item['data'])
                    for item in lista if item['nome'] not in [la.nome for la in ListaAtividade.query.all()]]
    try:
        # Adicionando as novas listas de atividades na sessão e realizando o commit
        db.session.add_all(novas_listas)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_listas)} Nova listas de atividades inseridas com sucesso.')

        # Retornando a lista de novas listas de atividades adicionados
        return novas_listas
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Nova lista de atividade: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tipo_binarios(lista: List[dict]) -> List[TipoBinario]:
    """
       Cria novas listas de atividades a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das novas listas de atividades
       Returns:
           List[Unidade]: Lista de novas listas de atividadescriados e adicionados na base de dados.
       """

    # Criando uma lista de novas unidades para serem adicionados
    novos_binarios = [TipoBinario(nome=item['nome'])
                      for item in lista if item['nome'] not in [tb.nome for tb in TipoBinario.query.all()]]
    try:
        # Adicionando as novas listas de atividades na sessão e realizando o commit
        db.session.add_all(novos_binarios)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_binarios)} Novos Tipos Binários inseridas com sucesso.')

        # Retornando a lista de novas listas de atividades adicionados
        return novos_binarios
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Novo Tipo Binário: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_atividades(lista: List[dict]) -> List[Atividade]:
    # Buscando os objetos necessários

    tipos = {tp.nome: tp.id for tp in TipoParametro.query.all()}
    listas = {la.nome: la.id for la in ListaAtividade.query.all()}
    tipobinarios = {tb.nome: tb.id for tb in TipoBinario.query.all()}

    novas_listas = [
        Atividade(
            posicao=item['posicao'],
            descricao=item['descricao'],
            valorbinario_id=tipobinarios[item['valorbinario_id']]
            if item['valorbinario_id'] else None,
            valorinteiro=item['valorinteiro'],
            valordecimal=item['valordecimal'],
            valortexto=item['valortexto'],
            tipoparametro_id=tipos[item['tipo']],
            listaatividade_id=listas[item['lista']]) for item in lista]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novas_listas)
        db.session.commit()
        log.info(f'{len(novas_listas)} Atividades inseridos com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novas_listas
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir atividades: {e}')
        db.session.rollback()
        return []


def criar_tipo_ordem(lista: List[dict]) -> List[TipoOrdem]:
    """
   Cria novos tipos de ordem a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novos tipos de ordem.
   Returns:
       List[Unidade]: Lista de novos tipos de ordem criados e adicionados na base de dados.
   """

    # Criando a lista de novas periodicidades a serem adicionadas
    novos_tipos = [TipoOrdem(nome=item['nome'], sigla=item['sigla'], plano=item['plano'])
                   for item in lista if item['nome'] not in [t.nome for t in TipoOrdem.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novos_tipos)
        db.session.commit()
        log.info(f'{len(novos_tipos)} periodicidades inseridas com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novos_tipos
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir novo tipos de ordem de serviço: {e}')
        db.session.rollback()
        return []


def criar_tipo_situacao_ordem(lista: List[dict]) -> List[TipoSituacaoOrdem]:
    """
       Cria novas situações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novas situações.
       Returns:
           List[Contrato]: Lista de novas situações criados e adicionados na base de dados.
       """
    # Criando um conjunto de situações de ordens existentes na base de dados
    situacoes_ordem_existentes = set(so.nome for so in TipoSituacaoOrdem.query.all())
    # Criando uma lista de novas situações de ordens para serem adicionados
    novas_situacoes_ordem = [TipoSituacaoOrdem(nome=item['nome'],
                                               sigla=item['sigla'])
                             for item in lista if item['nome'] not in situacoes_ordem_existentes]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novas_situacoes_ordem)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_situacoes_ordem)} Tipos de situações das ordens inseridas com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novas_situacoes_ordem
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tipo de situações das ordens: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tipo_situacao_ordem_perfil_manutentor(lista: List[dict]) -> List[TipoSituacaoOrdemPerfilManutentor]:
    tipossituacoesordem = {ts.sigla: ts.id for ts in TipoSituacaoOrdem.query.all()}
    perfismanutentor = {pm.nome: pm.id for pm in PerfilManutentor.query.all()}

    # Criando uma lista de novas situações de ordens para serem adicionados
    novos_ts_pm = [TipoSituacaoOrdemPerfilManutentor(tiposituacaoordem_id=tipossituacoesordem[item['situacao']],
                                                     perfilmanutentor_id=perfismanutentor[item['perfil']])
                   for item in lista]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novos_ts_pm)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_ts_pm)} TipoSituacaoOrdemPerfilManutentor inseridos com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novos_ts_pm
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir TipoSituacaoOrdemPerfilManutentor: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tipo_status_ordem(lista: List[dict]) -> List[TipoStatusOrdem]:
    """
       Cria novas situações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novas situações.
       Returns:
           List[Contrato]: Lista de novas situações criados e adicionados na base de dados.
       """
    # Criando um conjunto de situações de ordens existentes na base de dados
    status_ordem_existentes = {so.nome for so in TipoStatusOrdem.query.all()}

    # Criando uma lista de novas situações de ordens para serem adicionados
    novos_status_ordem = [TipoStatusOrdem(nome=item['nome'],
                                          sigla=item['sigla'])
                          for item in lista if item['nome'] not in status_ordem_existentes]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novos_status_ordem)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_status_ordem)} Tipos de status das ordens inseridos com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novos_status_ordem
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tipo de status das ordens: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_ordem_servico(lista: List[dict]) -> List[OrdemServico]:
    """
       Criar ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações de ordens de serviços.
       Returns:
           List[Contrato]: Lista de novas ordens de serviços criadas e adicionados na base de dados.
       """
    # Lista de equipamentos do banco de dados
    equipamentos = {e.cod: e.id for e in Equipamento.query.all()}
    situacoes_ordem = {so.sigla: so.id for so in TipoSituacaoOrdem.query.all()}
    status_ordem = {st.sigla: st.id for st in TipoStatusOrdem.query.all()}
    planosmanutencao = {pm.codigo: pm.id for pm in PlanoManutencao.query.all()}
    solicitantes = {u.nome: u.id for u in Usuario.query.all()}
    tipos_ordem = {t.sigla: t.id for t in TipoOrdem.query.all()}

    # Criando uma lista de novas ordens para serem adicionados
    novas_ordens_servicos = [OrdemServico(codigo=item['codigo'],
                                          descricao=item['descricao'],
                                          data_abertura=item['data_abertura'],
                                          equipamento_id=equipamentos[item['equipamento']],
                                          tiposituacaoordem_id=situacoes_ordem[item['situacaoordem']],
                                          tipostatusordem_id=status_ordem[item['status']],
                                          solicitante_id=solicitantes[item['solicitante']],
                                          tipoordem_id=tipos_ordem[item['tipo']],
                                          planomanutencao_id=planosmanutencao[item['planomanutencao']]
                                          if item['planomanutencao'] else None)
                             for item in lista]

    try:
        # Adicionando as novas ordens de serviços na sessão e realizando o commit
        db.session.add_all(novas_ordens_servicos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_ordens_servicos)} Ordens de Serviços inseridas com sucesso.')

        # Retornando a lista de novas ordens de serviços adicionados
        return novas_ordens_servicos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Ordem de Serviço: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tramitacao(lista: List[dict]) -> List[TramitacaoOrdem]:
    """
       Criar as tramitações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das tramitações.
       Returns:
           List[Tramitação]: Lista de novas tramitações de ordens de serviços criadas e adicionados na base de dados.
       """

    # Listas dos objetos necessários
    usuarios = {u.nome: u.id for u in Usuario.query.all()}
    situacoes_ordem = {so.sigla: so.id for so in TipoSituacaoOrdem.query.all()}

    # Criando uma lista de novas ordens para serem adicionados
    novas_tramitacoes = [TramitacaoOrdem(
        ordemservico_id=item['ordem_servico'],
        usuario_id=usuarios[item['usuario']],
        tiposituacaoordem_id=situacoes_ordem[item['situacaoordem']],
        data=item['data'],
        observacao=item['observacao'])
        for item in lista]

    try:
        # Adicionando as novas ordens de serviços na sessão e realizando o commit
        db.session.add_all(novas_tramitacoes)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_tramitacoes)} Tramitações inseridas com sucesso.')

        # Retornando a lista de novas ordens de serviços adicionados
        return novas_tramitacoes
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tramitação: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_fluxo_ordem(lista: List[dict]) -> List[FluxoOrdem]:
    """
       Cria novas situações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novas situações.
       Returns:
           List[Contrato]: Lista de novas situações criados e adicionados na base de dados.
       """
    # Criando um conjunto de situações de ordens existentes na base de dados
    situacoes_ordem = {so.sigla: so.id for so in TipoSituacaoOrdem.query.all()}

    # Criando uma lista de novas situações de ordens para serem adicionados
    novos_fluxos = [FluxoOrdem(de=situacoes_ordem[item['de']], para=situacoes_ordem[item['para']])
                    for item in lista]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novos_fluxos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_fluxos)} Fluxos de ordem serviço inseridas com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novos_fluxos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Fluxo de ordem de serviço: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []
