import streamlit as st
from openai import OpenAI
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gerador Maple Bear - Beta", layout="wide")

# CARREGAMENTO DA CHAVE (No site, configuramos nos 'Secrets' do Streamlit)
# Se estiver testando localmente, ele pegará do seu ambiente.
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# DADOS DAS DISCIPLINAS
DADOS_DISCIPLINAS = {
    "Matemática Aplicada": {
        "Resolução de problemas": ["Praticar interpretação de dados", "Validar estratégias", "Usar esquemas visuais", "Revisar cálculos", "Modelar situações reais"],
        "Compreensão de conceitos": ["Revisitar registros", "Usar manipulativos", "Relacionar com cotidiano", "Explicar conceitos", "Pesquisar fundamentos"],
        "Aplicação de procedimentos": ["Praticar algoritmos", "Organizar etapas", "Automatizar básicos", "Verificar fórmulas", "Atenção a sinais"],
        "Comunicação matemática": ["Usar vocabulário técnico", "Explicar em voz alta", "Estruturar respostas", "Legendar gráficos", "Justificar raciocínio"]
    },
    "História": {
        "Conhecimento e compreensão de conceitos": ["Revisitar termos históricos", "Relacionar eventos e épocas", "Identificar causas e consequências", "Analisar contextos sociais", "Consultar o glossário da unidade"],
        "Pesquisa e comunicação": ["Diversificar fontes de pesquisa", "Organizar referências bibliográficas", "Sintetizar informações colhidas", "Melhorar a clareza textual", "Utilizar mapas e documentos"],
        "Pensamento crítico e cidadania": ["Analisar diferentes perspectivas", "Argumentar com base em evidências", "Relacionar passado e presente", "Participar de debates em sala", "Refletir sobre impactos sociais"]
    }
}

st.title("🐻 Gerador de Report Card - Maple Bear")
st.info("Versão Beta para Testes - Matemática Aplicada & História")

# SIDEBAR - DADOS DO ALUNO
with st.sidebar:
    st.header("Dados do Aluno")
    nome_aluno = st.text_input("Nome completo")
    disc_selecionada = st.selectbox("Selecione a Disciplina", list(DADOS_DISCIPLINAS.keys()))
    senha_acesso = st.text_input("Senha de Acesso", type="password")

# CORPO DO SITE
st.subheader(f"Critérios de Avaliação: {disc_selecionada}")

col1, col2 = st.columns(2)
selecoes_pf = []
selecoes_nm = []
sugestoes_finais = []

# Gerar as opções dinamicamente
for i, (crit, sugs) in enumerate(DADOS_DISCIPLINAS[disc_selecionada].items()):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.write(f"**{crit}**")
        status = st.radio(f"Status - {crit}", ["Não avaliado", "Ponto Forte", "A aperfeiçoar"], key=f"rad_{crit}", horizontal=True)
        
        if status == "Ponto Forte":
            selecoes_pf.append(crit)
        elif status == "A aperfeiçoar":
            selecoes_nm.append(crit)
            st.caption("Selecione as sugestões de melhoria:")
            for s in sugs:
                if st.checkbox(s, key=f"sug_{s}_{crit}"):
                    sugestoes_finais.append(s)
        st.divider()

# BOTÃO GERAR
if st.button("GERAR COMENTÁRIO OFICIAL"):
    if not nome_aluno:
        st.error("Por favor, preencha o nome do aluno.")
    elif senha_acesso != "MAPLE2026": # Defina sua senha aqui
        st.error("Senha de acesso incorreta.")
    else:
        with st.spinner('A IA está redigindo o texto conforme o Manual 2019...'):
            try:
                prompt = (
                    f"Professor de {disc_selecionada}. Aluno: {nome_aluno}. "
                    f"Sucessos: {selecoes_pf}. Desafios (A aperfeiçoar): {selecoes_nm}. "
                    f"Sugestões práticas escolhidas: {sugestoes_finais}."
                )
                
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Manual Maple Bear 2019: Use apenas o tempo passado. Parágrafo único. Sem saudações. Termos obrigatórios: 'evidenciou', 'consolidou', 'revisita'. Foco no desempenho acadêmico."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4
                )
                
                comentario = res.choices[0].message.content.strip()
                st.subheader("Texto Gerado:")
                st.success(comentario)
                st.info("Dica: Clique no ícone de copiar no canto superior direito do bloco abaixo.")
                st.code(comentario, language="text")
                
            except Exception as e:
                st.error(f"Erro ao gerar: {e}")
