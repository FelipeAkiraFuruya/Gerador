import streamlit as st
from openai import OpenAI
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gerador Maple Bear - Versão Humanizada", layout="wide")

# CARREGAMENTO DA CHAVE
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# DADOS DAS DISCIPLINAS E SUGESTÕES
DADOS_DISCIPLINAS = {
    "Matemática Aplicada": {
        "Resolução de problemas": ["Praticar a interpretação de dados", "Validar estratégias", "Usar esquemas visuais", "Revisar cálculos", "Modelar situações reais"],
        "Compreensão de conceitos": ["Revisitar registros", "Usar materiais manipulativos", "Relacionar com o cotidiano", "Explicar conceitos", "Pesquisar fundamentos"],
        "Aplicação de procedimentos": ["Praticar algoritmos", "Organizar as etapas de resolução", "Automatizar processos básicos", "Verificar fórmulas", "Ter atenção aos sinais"],
        "Comunicação matemática": ["Utilizar vocabulário técnico", "Explicar o raciocínio em voz alta", "Estruturar melhor as respostas", "Legendar gráficos", "Justificar o raciocínio utilizado"]
    },
    "História": {
        "Conhecimento e compreensão de conceitos": ["Revisitar termos históricos", "Relacionar eventos e épocas", "Identificar causas e consequências", "Analisar contextos sociais", "Consultar o glossário da unidade"],
        "Pesquisa e comunicação": ["Diversificar as fontes de pesquisa", "Organizar referências bibliográficas", "Sintetizar as informações colhidas", "Melhorar a clareza textual", "Utilizar mapas e documentos de época"],
        "Pensamento crítico e cidadania": ["Analisar diferentes perspectivas", "Argumentar com base em evidências", "Relacionar o passado com o presente", "Participar de debates em sala", "Refletir sobre impactos sociais"]
    }
}

st.title("🐻 Gerador de Report Card - Maple Bear")
st.subheader("Foco: Texto Humanizado e Diretrizes 2019")

# SIDEBAR
with st.sidebar:
    st.header("Identificação")
    nome_aluno = st.text_input("Nome do Aluno")
    disc_selecionada = st.selectbox("Disciplina", list(DADOS_DISCIPLINAS.keys()))
    senha_acesso = st.text_input("Senha de Acesso", type="password")

# CORPO
st.info(f"Critérios: {disc_selecionada}")

col1, col2 = st.columns(2)
selecoes_pf = []
selecoes_nm = []
sugestoes_finais = []

for i, (crit, sugs) in enumerate(DADOS_DISCIPLINAS[disc_selecionada].items()):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.write(f"**{crit}**")
        status = st.radio(f"Status - {crit}", ["Não avaliado", "Ponto Forte", "A aperfeiçoar"], key=f"rad_{crit}", horizontal=True)
        
        if status == "Ponto Forte":
            selecoes_pf.append(crit)
        elif status == "A aperfeiçoar":
            selecoes_nm.append(crit)
            for s in sugs:
                if st.checkbox(s, key=f"sug_{s}_{crit}"):
                    sugestoes_finais.append(s)
        st.divider()

if st.button("GERAR COMENTÁRIO HUMANIZADO"):
    if not nome_aluno:
        st.error("Por favor, preencha o nome do aluno.")
    elif senha_acesso != "MAPLE2026":
        st.error("Senha incorreta.")
    else:
        with st.spinner('Redigindo comentário...'):
            try:
                # Prompt Refinado para parecer "menos IA"
                system_instruction = (
                    "Você é um professor experiente da Maple Bear que escreve de forma humana, clara e empática. "
                    "Siga estas regras rigorosamente:\n"
                    "1. ESTILO: Evite frases clichês de IA. Escreva um parágrafo único, fluido e elegante. Não use listas.\n"
                    "2. TEMPO VERBAL DO DESEMPENHO: Use o PASSADO para descrever o que o aluno fez (ex: 'demonstrou', 'consolidou').\n"
                    "3. TEMPO VERBAL DA SUGESTÃO: Use o PRESENTE para as recomendações (ex: 'Para fortalecer esse processo, sugiro que revise...', 'Recomendo que utilize...').\n"
                    "4. VOCABULÁRIO: Use termos do Manual 2019 como 'evidenciou', 'revisita', 'manipulativos'.\n"
                    "5. HUMANIZAÇÃO: Varie o início das frases. Não comece sempre com o nome do aluno."
                )
                
                user_input = (
                    f"Aluno: {nome_aluno}. Disciplina: {disc_selecionada}. "
                    f"O que ele já faz bem: {selecoes_pf}. "
                    f"O que precisa melhorar: {selecoes_nm}. "
                    f"Ações recomendadas (diga no presente): {sugestoes_finais}."
                )
                
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.6 # Aumentado levemente para maior naturalidade
                )
                
                texto = res.choices[0].message.content.strip()
                st.subheader("Comentário Gerado:")
                st.success(texto)
                st.code(texto, language="text")
                
            except Exception as e:
                st.error(f"Erro: {e}")
