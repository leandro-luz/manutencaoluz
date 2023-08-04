import pandas as pd
import numpy as np
from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import current_user, login_required
from webapp.empresa.models import Empresa
from webapp.plano_manutencao.models import PlanoManutencao, TipoData, Periodicidade
from webapp.equipamento.models import Equipamento, Grupo, Subgrupo
from webapp.ordem_servico.models import OrdemServico
from webapp.plano_manutencao.forms import PlanoForm
from webapp.usuario import has_view
from webapp.ordem_servico.models import TipoOrdem
from webapp.utils.files import arquivo_padrao
from webapp.utils.erros import flash_errors

plano_manutencao_blueprint = Blueprint(
    'plano_manutencao',
    __name__,
    template_folder='../templates/sistema/plano_manutencao',
    url_prefix="/sistema"
)


@plano_manutencao_blueprint.route('/plano_listar', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_listar():
    """Retorna a lista dos planos de manutenção"""
    planos = PlanoManutencao.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id,
        Equipamento.id == PlanoManutencao.equipamento_id).all()

    # planos = PlanoManutencao.query.filter_by(empresa_id=current_user.empresa_id).all()
    return render_template('plano_manutencao_listar.html', planos=planos)


@plano_manutencao_blueprint.route('/plano_ativar/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_ativar(plano_id):
    plano = PlanoManutencao.query.filter_by(id=plano_id).one_or_none()
    if plano:
        plano.ativar_desativar()
        if not plano.salvar():
            flash("Plano de Manutenção não ativado/desativado", category="danger")
    else:
        flash("Plano de Manutenção não localizado", category="danger")
    return redirect(url_for('plano_manutencao.plano_listar'))


@plano_manutencao_blueprint.route('/plano_editar/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_editar(plano_id):
    new = True
    if plano_id > 0:
        # Atualizar
        plano = PlanoManutencao.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.id == Equipamento.subgrupo_id,
            Equipamento.id == PlanoManutencao.equipamento_id,
            PlanoManutencao.id == plano_id
        ).one_or_none()

        # verifica se o plano existe
        if plano:
            form = PlanoForm(obj=plano)
            new = False
            # Atualizar ou Ler dados
            if form.tipodata.data:
                to_d = form.tipoordem.data
                tp_d = form.tipodata.data
                e_d = form.equipamento.data
                p_d = form.periodicidade.data
            else:
                to_d = plano.tipoordem_id
                tp_d = plano.tipodata_id
                e_d = plano.equipamento_id
                p_d = plano.periodicidade_id
        else:
            flash("Plano de manutenção não localizado", category="danger")
            return redirect(url_for("plano_manutencao.plano_listar"))
    else:
        # Cadastrar
        plano = PlanoManutencao()
        plano.id = 0
        form = PlanoForm()

        tp_d = form.tipodata.data
        e_d = form.equipamento.data
        p_d = form.periodicidade.data
        to_d = form.tipoordem.data

    # Listas
    form.tipoordem.choices = [(0, '')] + [(to.id, to.nome) for to in TipoOrdem.query.filter_by(plano=True)]
    form.tipodata.choices = [(tp.id, tp.nome) for tp in TipoData.query.all()]
    form.periodicidade.choices = [(0, '')] + [(p.id, p.nome) for p in Periodicidade.query.all()]

    form.equipamento.choices = [(0, '')] + [(e.id, e.descricao_curta)
                                            for e in Equipamento.query.filter(Equipamento.subgrupo_id == Subgrupo.id,
                                                                              Subgrupo.grupo_id == Grupo.id,
                                                                              Grupo.empresa_id == Empresa.id,
                                                                              Empresa.id == current_user.empresa_id)
                                            ]
    form.tipoordem.data = to_d
    form.tipodata.data = tp_d
    form.equipamento.data = e_d
    form.periodicidade.data = p_d

    # Validação
    if form.validate_on_submit():
        plano.alterar_atributos(form, new)
        if plano.salvar():
            # case seja um novo plano, gera um ordem para este plano
            if new:
                # recupera o plano salvo
                plano = PlanoManutencao.query.filter_by(nome=form.nome.data).one_or_none()
                ordem = OrdemServico()
                ordem.alterar_atributos_by_plano(plano)
                # salva a nova ordem de serviço
                if ordem.salvar():
                    flash("Ordem de Serviço Cadastrado", category="success")
                else:
                    flash("Ordem de Serviço não Cadastrado", category="success")

            # Mensagens
            if plano_id > 0:
                flash("Plano de manutenção atualizado", category="success")
            else:
                flash("Plano de manutenção cadastrado", category="success")
            return redirect(url_for("plano_manutencao.plano_listar"))
        else:
            flash("Plano de manutenção não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("plano_manutencao_editar.html", form=form, plano=plano)


@plano_manutencao_blueprint.route('/gerar_padrao_planos_manutencao/', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def gerar_padrao_planos_manutencao():
    result, path = arquivo_padrao(nome_arquivo=PlanoManutencao.nome_doc,
                                  valores=[[x] for x in PlanoManutencao.titulos_doc])
    if result:
        flash(f'Foi gerado o arquivo padrão no caminho: {path}', category="success")
    else:
        flash("Não foi gerado o arquivo padrão", category="danger")
    return redirect(url_for("plano_manutencao.plano_listar"))


@plano_manutencao_blueprint.route('/cadastrar_lote_planos_manutencao/', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def cadastrar_lote_planos_manutencao():
    form = PlanoForm()

    # filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=PlanoManutencao.titulos_doc, encoding='latin-1'))

    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in PlanoManutencao.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = [x.codigo for x in PlanoManutencao.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id,
        Equipamento.id == PlanoManutencao.equipamento_id).all()]

    rejeitados_texto = [['CÓDIGO', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []
    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        # verifica se os campo obrigatórios foram preenchidos
        for col_ob in titulos_obrigatorio:
            # caso não seja
            if not df.at[linha, col_ob]:
                # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                rejeitados.append(df.at[linha, 'Código*'])
                rejeitados_texto.append(
                    [df.at[linha, 'Código*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Código*'].upper() in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado por já existir no banco de dados"])

        # Verifica se o equipamento existe para a empresa
        equipamento = Equipamento.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.id == Equipamento.subgrupo_id,
            Equipamento.cod == df.at[linha, 'Equipamento_cod*'].upper()).one_or_none()
        if not equipamento:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido ao equipamento não existir"])

        periodicidade = Periodicidade.query.filter(
            Periodicidade.nome == df.at[linha, 'Periodicidade*'].upper()).one_or_none()
        if not periodicidade:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido a periodicidade não existir"])

        tipo_data = TipoData.query.filter(
            TipoData.nome == df.at[linha, 'Tipo_Data_Inicial*']).one_or_none()
        if not tipo_data:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido ao tipo_data_inicial não existir"])

        tipo_ordem = TipoOrdem.query.filter(
            TipoOrdem.nome == df.at[linha, 'Tipo_Ordem*'].upper()).one_or_none()
        if not tipo_ordem:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido ao tipo_ordem não existir"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Código*'] in aceitos_cod:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido a estar repetido"])

        # Verifica se não foi rejeitado
        if df.at[linha, 'Código*'] not in rejeitados:
            # altera o valor do equipamento,periodicidade,tipo_data,tipo_ordem de nome para id na tabela
            df.at[linha, 'Equipamento_cod*'] = equipamento.id
            df.at[linha, 'Periodicidade*'] = periodicidade.id
            df.at[linha, 'Tipo_Data_Inicial*'] = tipo_data.id
            df.at[linha, 'Tipo_Ordem*'] = tipo_ordem.id

            # cria um plano_manutenção e popula ele
            plano = PlanoManutencao()
            for k, v in plano.titulos_doc.items():
                # recupere o valor
                valor = df.at[linha, k]
                if str(valor).isnumeric() or valor is None:
                    # Salva o atributo se o valor e numerico ou nulo
                    setattr(plano, v, valor)
                else:
                    # Salva o atributo quando texto
                    setattr(plano, v, valor.upper())
            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Código*'])
            # insere o equipamento na lista
            aceitos.append(plano)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        Equipamento.salvar_lote(aceitos)

    flash(f"Total de plano cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        result, path = arquivo_padrao(nome_arquivo="Planos_Manutenção_rejeitados", valores=rejeitados_texto)
        if result:
            flash(f'Foi gerado o arquivo dos planos de manutenções rejeitados no caminho: {path}', category="warning")
        else:
            flash("Não foi gerado o arquivo dos planos de manutenções rejeitados", category="danger")

    return redirect(url_for('plano_manutencao.plano_listar'))
