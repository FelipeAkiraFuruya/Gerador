import streamlit as st
from openai import OpenAI
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gerador Maple Bear - High School & Middle Years", layout="wide")

# CARREGAMENTO DA CHAVE (Configurada nos Secrets do Streamlit Cloud)
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# DADOS DAS DISCIPLINAS E SUGESTÕES EXPANDIDAS
DADOS_DISCIPLINAS = {
    "Matemática": { # High School
        "Resolução de problemas": [
            "Praticar a interpretação de dados e enunciados", 
            "Validar as estratégias de resolução encontradas", 
            "Utilizar esquemas visuais para modelagem", 
            "Revisar cálculos para evitar erros de atenção", 
            "Modelar situações reais através de funções",
            "Desenvolver métodos de prova e verificação",
            "Explorar diferentes caminhos para o mesmo problema",
            "Identificar variáveis críticas em problemas complexos"
        ],
        "Compreensão de conceitos": [
            "Revisitar registros e definições teóricas", 
            "Usar materiais manipulativos ou softwares gráficos", 
            "Relacionar conceitos abstratos com o cotidiano", 
            "Explicar fundamentos para consolidar o aprendizado", 
            "Pesquisar a origem histórica dos teoremas",
            "Aprofundar o estudo em propriedades fundamentais",
            "Sintetizar conceitos através de mapas mentais",
            "Estabelecer conexões entre diferentes tópicos da disciplina"
        ],
        "Aplicação de procedimentos": [
            "Praticar algoritmos e sequências lógicas", 
            "Organizar as etapas de resolução detalhadamente", 
            "Automatizar processos algébricos básicos", 
            "Verificar fórmulas e suas deduções", 
            "Ter atenção aos sinais e propriedades operatórias",
            "Sistematizar a conferência de resultados parciais",
            "Aprimorar o manejo de ferramentas tecnológicas",
            "Desenvolver maior rigor na escrita matemática"
        ],
        "Comunicação matemática": [
            "Utilizar vocabulário técnico com precisão", 
            "Explicar o raciocínio em voz alta para validação", 
            "Estruturar melhor as respostas dissertativas", 
            "Legendar gráficos e tabelas corretamente", 
            "Justificar o raciocínio utilizado em cada etapa",
            "Empregar notação matemática formal de forma correta",
            "Apresentar argumentos de forma lógica e sequencial",
            "Refinar a clareza na exposição de ideias complexas"
        ]
    },
    "Matemática Aplicada": { # Middle Years (mesmos critérios)
        "Resolução de problemas": ["Praticar interpretação de dados", "Validar estratégias", "Usar esquemas visuais", "Revisar cálculos", "Modelar situações reais", "Analisar resultados obtidos", "Fragmentar problemas complexos", "Testar hipóteses"],
        "Compreensão de conceitos": ["Revisitar registros", "Usar materiais manipulativos", "Relacionar com o cotidiano", "Explicar conceitos", "Pesquisar fundamentos", "Comparar definições", "Construir exemplos próprios", "Identificar padrões"],
        "Aplicação de procedimentos": ["Praticar algoritmos", "Organizar etapas", "Automatizar básicos", "Verificar fórmulas", "Atenção a sinais", "Corrigir exercícios anteriores", "Seguir fluxogramas", "Manter o rigor nos passos"],
        "Comunicação matemática": ["Usar vocabulário técnico", "Explicar em voz alta", "Estruturar respostas", "Legendar gráficos", "Justificar raciocínio", "Interpretar textos matemáticos", "Escrever resoluções passo a passo", "Debater estratégias com pares"]
    },
    "História": {
        "Conhecimento e compreensão de conceitos": ["Revisitar termos históricos", "Relacionar eventos e épocas", "Identificar causas e consequências", "Analisar contextos sociais", "Consultar o glossário da unidade", "Diferenciar conceitos políticos e econômicos", "Explicar a importância de marcos históricos", "Contextualizar fontes primárias"],
        "Pesquisa e comunicação": ["Diversificar as fontes de pesquisa", "Organizar referências bibliográficas", "Sintetizar as informações colhidas", "Melhorar a clareza textual", "Utilizar mapas e documentos de época", "Estruturar argumentos em ensaios", "Citar fontes corretamente", "Elaborar roteiros de investigação"],
        "Pensamento crítico e cidadania": ["Analisar diferentes perspectivas", "Argumentar com base em evidências", "Relacionar o passado com o presente", "Participar de debates em sala", "Refletir sobre impactos sociais", "Avaliar o impacto de decisões históricas", "Debater direitos e deveres na história", "Reconhecer a pluralidade cultural"]
    }
}

st.title("🐻 Gerador de Report Card - Maple Bear")
st.caption("Versão 2.0: Matemática (HS), Matemática Aplicada (MY) e História")

# SIDEBAR
with st.sidebar:
    st.header("Identificação")
    nome_aluno = st.text_input("Nome do Aluno")
    disc_selecionada = st.selectbox("Disciplina", list(DADOS_DISCIPLINAS.keys()))
    senha_acesso = st.text_input("Senha de Acesso", type="password")

# CORPO
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
            st.markdown("*Sugestões específicas (selecione):*")
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
                system_instruction = (
                    "Você é um professor experiente da Maple Bear. Escreva de forma humana e fluida.\n"
                    "1. ESTILO: Parágrafo único, sem listas, tom empático e profissional.\n"
                    "2. PASSADO (Desempenho): Use o passado para descrever o que o aluno realizou (ex: 'demonstrou', 'evidenciou').\n"
                    "3. PRESENTE (Sugestões): Use o presente para as recomendações (ex: 'Sugiro que...', 'Recomendo a...').\n"
                    "4. HUMANIZAÇÃO: Não comece todas as frases com o nome do aluno. Varie a estrutura."
                )
                
                user_input = f"Aluno: {nome_aluno}. Disciplina: {disc_selecionada}. Sucessos: {selecoes_pf}. Desafios: {selecoes_nm}. Sugestões no presente: {sugestoes_finais}."
                
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_input}],
                    temperature=0.6
                )
                
                texto = res.choices[0].message.content.strip()
                st.subheader("Resultado Final:")
                st.success(texto)
                st.code(texto, language="text")
                
            except Exception as e:
                st.error(f"Erro: {e}")
