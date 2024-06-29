from datetime import timedelta
import streamlit as st
import re


def verifica_numeros(texto):
    return bool(re.match('^[0-9]+$', texto))


def setup_session():
    if 'dados_extintor' not in st.session_state:
        st.session_state.dados_extintor = {
            'selo_inmetro': None,
            'tipo': None,
            'capacidade': None,
            'unidade_capacidade': None,
            'data_carga': None
        }


def cadastro_extintor():
    st.header('CADASTRO DE EXTINTORES')

    # Inicialização de variáveis de erro
    erro_inmetro = False
    erro_tipo = False
    erro_capacidade = False
    erro_data = False

    setup_session()

    with st.form(key='incluir_extintor'):

        selo_inmetro = st.text_input(label='Insira o Selo do Inmetro',
                                     value=st.session_state.dados_extintor['selo_inmetro'])

        tipo = st.selectbox('Selecione o tipo do extintor', options=['-', 'AP', 'BC', 'ABC', 'CO2'],
                            index=0 if st.session_state.dados_extintor['tipo'] is None else ['AP', 'BC', 'ABC',
                                                                                             'CO2'].index(
                                st.session_state.dados_extintor['tipo']))

        selecionar_tipo = st.form_submit_button('Selecionar tipo')

        # Configuração automática da capacidade conforme o tipo de extintor selecionado
        unidade_capacidade = None
        capacidade = None

        if selecionar_tipo and tipo == '-':
            st.warning('Selecione um tipo válido de extintor.')
        elif tipo == 'AP':
            unidade_capacidade = 'LT'
            capacidade = 10  # Capacidade padrão para extintores AP é 10 LT
        elif tipo == 'BC':
            unidade_capacidade = 'KG'
            capacidade_option = st.selectbox('Selecione a capacidade', options=['4 KG', '6 KG', '12 KG'])
            capacidade = int(capacidade_option.split()[0])  # Extrai o valor numérico
        elif tipo in ['ABC', 'CO2']:
            unidade_capacidade = 'KG'
            capacidade = 6  # Capacidade padrão para extintores ABC e CO2 é 6 KG

        data_carga = st.date_input(label='Insira a data da carga', value=st.session_state.dados_extintor['data_carga'])

        botao_cadastro = st.form_submit_button('Cadastrar extintor')

        if botao_cadastro:
            # Atualizar dados na session_state
            st.session_state.dados_extintor['selo_inmetro'] = selo_inmetro
            st.session_state.dados_extintor['tipo'] = tipo
            st.session_state.dados_extintor['capacidade'] = capacidade
            st.session_state.dados_extintor['unidade_capacidade'] = unidade_capacidade
            st.session_state.dados_extintor['data_carga'] = data_carga

            # Verificação de erros
            if not verifica_numeros(selo_inmetro):
                erro_inmetro = True
                st.error('Digite somente números para o selo inmetro.')
            elif not (9 <= len(selo_inmetro) <= 12):
                erro_inmetro = True
                st.error('Selo inmetro deve ter entre 9 e 12 dígitos.')

            if tipo == '-':
                erro_tipo = True
                st.error('Selecione o tipo do extintor!')

            if capacidade is None:
                erro_capacidade = True
                st.error('Selecione a capacidade do extintor!')

            if not data_carga:
                erro_data = True
                st.error('Insira a data da carga!')

            if not (erro_inmetro or erro_tipo or erro_capacidade or erro_data):
                data_validade = data_carga + timedelta(days=365) if data_carga else None
                st.success('Extintor cadastrado com sucesso!')

                # Mostrar tabela com extintor cadastrado
                st.subheader('Extintor cadastrado')
                dados_cadastrados = {
                    'Selo Inmetro': selo_inmetro,
                    'Tipo': tipo,
                    'Capacidade': f'{capacidade} {unidade_capacidade}',
                    'Data de Carga': data_carga.strftime('%d/%m/%Y')
                }
                st.table([dados_cadastrados])

                # Limpar dados após cadastro
                st.session_state.dados_extintor = {
                    'selo_inmetro': None,
                    'tipo': None,
                    'capacidade': None,
                    'unidade_capacidade': None,
                    'data_carga': None
                }

        # Mensagens de erro específicas para cada campo não preenchido
        if erro_inmetro:
            st.error('Preencha corretamente o selo do Inmetro!')
        if erro_tipo:
            st.error('Selecione o tipo do extintor!')
        if erro_capacidade:
            st.error('Selecione a capacidade do extintor!')
        if erro_data:
            st.error('Insira a data da carga!')
