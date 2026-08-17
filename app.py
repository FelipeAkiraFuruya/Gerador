import streamlit as st
from openai import OpenAI
import os


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Gerador Maple Bear - High School & Middle Years",
    page_icon="🐻",
    layout="wide"
)


# ============================================================
# CONFIGURAÇÃO DA API OPENAI
# ============================================================

api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "❌ A chave da API da OpenAI não foi encontrada.\n\n"
        "Configure OPENAI_API_KEY nos Secrets do Streamlit Cloud."
    )
    st.stop()

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"❌ Não foi possível inicializar a API da OpenAI: {e}")
    st.stop()


# ============================================================
# DADOS DAS DISCIPLINAS
# ============================================================

DADOS_DISCIPLINAS = {

    "Matemática": {

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


    "Matemática Aplicada": {

        "Resolução de problemas": [
            "Praticar interpretação de dados",
            "Validar estratégias",
            "Usar esquemas visuais",
            "Revisar cálculos",
            "Modelar situações reais",
            "Analisar resultados obtidos",
            "Fragmentar problemas complexos",
            "Testar hipóteses"
        ],

        "Compreensão de conceitos": [
            "Revisitar registros",
            "Usar materiais manipulativos",
            "Relacionar com o cotidiano",
            "Explicar conceitos",
            "Pesquisar fundamentos",
            "Comparar definições",
            "Construir exemplos próprios",
            "Identificar padrões"
        ],

        "Aplicação de procedimentos": [
            "Praticar algoritmos",
            "Organizar etapas",
            "Automatizar procedimentos básicos",
            "Verificar fórmulas",
            "Ter atenção aos sinais",
            "Corrigir exercícios anteriores",
            "Seguir fluxogramas",
            "Manter o rigor nos passos"
        ],

        "Comunicação matemática": [
            "Usar vocabulário técnico",
            "Explicar em voz alta",
            "Estruturar respostas",
            "Legendar gráficos",
            "Justificar raciocínio",
            "Interpretar textos matemáticos",
            "Escrever resoluções passo a passo",
            "Debater estratégias com pares"
        ]
    },


    "História": {

        "Conhecimento e compreensão de conceitos": [
            "Revisitar termos históricos",
            "Relacionar eventos e épocas",
            "Identificar causas e consequências",
            "Analisar contextos sociais",
            "Consultar o glossário da unidade",
            "Diferenciar conceitos políticos e econômicos",
            "Explicar a importância de marcos históricos",
            "Contextualizar fontes primárias"
        ],

        "Pesquisa e comunicação": [
            "Diversificar as fontes de pesquisa",
            "Organizar referências bibliográficas",
            "Sintetizar as informações colhidas",
            "Melhorar a clareza textual",
            "Utilizar mapas e documentos de época",
            "Estruturar argumentos em ensaios",
            "Citar fontes corretamente",
            "Elaborar roteiros de investigação"
        ],

        "Pensamento crítico e cidadania": [
            "Analisar diferentes perspectivas",
            "Argumentar com base em evidências",
            "Relacionar o passado com o presente",
            "Participar de debates em sala",
            "Refletir sobre impactos sociais",
            "Avaliar o impacto de decisões históricas",
            "Debater direitos e deveres na história",
            "Reconhecer a pluralidade cultural"
        ]
    }
}


# ============================================================
# FUNÇÃO PARA GERAR O COMENTÁRIO
# ============================================================

def gerar_comentario(
    nome_aluno,
    disciplina,
    pontos_fortes,
    pontos_a_aprimorar,
    sugestoes
):

    system_instruction = """
Você é um professor experiente da Maple Bear, responsável pela
elaboração de comentários de Report Card para estudantes.

Sua tarefa é escrever um comentário individualizado, natural,
profissional, acolhedor e pedagogicamente útil.

REGRAS OBRIGATÓRIAS:

1. Escreva SOMENTE um único parágrafo.

2. NÃO utilize listas, tópicos, títulos ou marcadores.

3. O comentário deve parecer escrito por um professor que conhece
   o aluno, e não por uma inteligência artificial.

4. Ao falar sobre o desempenho que o aluno já demonstrou,
   utilize predominantemente o PASSADO:
   "demonstrou", "evidenciou", "apresentou", "desenvolveu",
   "mostrou", "foi capaz de", etc.

5. Ao apresentar recomendações para o futuro, utilize o PRESENTE:
   "Sugiro que...", "Recomendo que...", "É importante que...",
   "Pode continuar desenvolvendo...", etc.

6. NÃO repita o nome do aluno no início de todas as frases.

7. Comece destacando aspectos positivos quando houver pontos fortes.

8. As dificuldades devem ser apresentadas de maneira construtiva,
   sem utilizar linguagem negativa, punitiva ou desmotivadora.

9. As recomendações devem estar diretamente relacionadas aos
   critérios que precisam ser aprimorados.

10. NÃO invente comportamentos, notas, projetos, atividades ou
    características que não foram fornecidos.

11. Evite frases genéricas como:
    "O aluno teve um bom desempenho."
    "Continue assim."
    "Precisa melhorar."
    "Parabéns pelo esforço."

12. Varie a estrutura das frases para evitar que diferentes
    comentários fiquem excessivamente semelhantes.

13. O texto deve ter aproximadamente 80 a 130 palavras.

14. O tom deve ser semelhante ao de um professor escrevendo
    diretamente para um Report Card escolar internacional.

15. NÃO mencione que você recebeu informações, critérios,
    sugestões ou instruções para escrever o comentário.

16. NÃO mencione inteligência artificial, ChatGPT ou OpenAI.

17. O resultado final deve ser apenas o comentário.
"""


    # --------------------------------------------------------
    # ORGANIZAÇÃO DOS DADOS
    # --------------------------------------------------------

    pontos_fortes_texto = (
        ", ".join(pontos_fortes)
        if pontos_fortes
        else "Nenhum ponto forte específico foi selecionado."
    )

    pontos_aprimorar_texto = (
        ", ".join(pontos_a_aprimorar)
        if pontos_a_aprimorar
        else "Nenhum aspecto específico foi selecionado para aprimoramento."
    )

    sugestoes_texto = (
        ", ".join(sugestoes)
        if sugestoes
        else "Nenhuma sugestão específica foi selecionada."
    )


    user_instruction = f"""
Aluno: {nome_aluno}

Disciplina: {disciplina}

Critérios nos quais apresentou pontos fortes:
{pontos_fortes_texto}

Critérios que podem ser aprimorados:
{pontos_aprimorar_texto}

Sugestões de desenvolvimento:
{sugestoes_texto}

Com base exclusivamente nessas informações, escreva o comentário
final do Report Card seguindo rigorosamente todas as instruções.
"""


    # --------------------------------------------------------
    # CHAMADA À API - RESPONSES API
    # --------------------------------------------------------

    resposta = client.responses.create(
        model="gpt-4o-mini",
        instructions=system_instruction,
        input=user_instruction,
        temperature=0.6,
        max_output_tokens=250
    )

    return resposta.output_text.strip()


# ============================================================
# INTERFACE
# ============================================================

st.title("🐻 Gerador de Report Card - Maple Bear")

st.caption(
    "Versão 3.0 • High School & Middle Years"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Identificação")

    nome_aluno = st.text_input(
        "Nome do Aluno",
        placeholder="Digite o nome do aluno"
    )

    disc_selecionada = st.selectbox(
        "Disciplina",
        list(DADOS_DISCIPLINAS.keys())
    )

    senha_acesso = st.text_input(
        "Senha de Acesso",
        type="password"
    )

    st.divider()

    st.caption(
        "O comentário é gerado automaticamente com base "
        "nos critérios selecionados."
    )


# ============================================================
# VARIÁVEIS
# ============================================================

selecoes_pf = []
selecoes_nm = []
sugestoes_finais = []


# ============================================================
# CRITÉRIOS
# ============================================================

col1, col2 = st.columns(2)


for i, (crit, sugs) in enumerate(
    DADOS_DISCIPLINAS[disc_selecionada].items()
):

    target_col = col1 if i % 2 == 0 else col2

    with target_col:

        st.write(f"### {crit}")

        status = st.radio(
            f"Status - {crit}",
            [
                "Não avaliado",
                "Ponto Forte",
                "A aperfeiçoar"
            ],
            key=f"rad_{disc_selecionada}_{crit}",
            horizontal=True
        )


        # ----------------------------------------------------
        # PONTO FORTE
        # ----------------------------------------------------

        if status == "Ponto Forte":

            selecoes_pf.append(crit)


        # ----------------------------------------------------
        # A APERFEIÇOAR
        # ----------------------------------------------------

        elif status == "A aperfeiçoar":

            selecoes_nm.append(crit)

            st.markdown(
                "**Sugestões específicas:**"
            )

            for indice, s in enumerate(sugs):

                selecionada = st.checkbox(
                    s,
                    key=f"sug_{disc_selecionada}_{crit}_{indice}"
                )

                if selecionada:

                    sugestoes_finais.append(
                        f"{crit}: {s}"
                    )


        st.divider()


# ============================================================
# BOTÃO
# ============================================================

gerar = st.button(
    "✨ GERAR COMENTÁRIO HUMANIZADO",
    use_container_width=True,
    type="primary"
)


# ============================================================
# GERAÇÃO
# ============================================================

if gerar:

    # --------------------------------------------------------
    # VALIDAÇÕES
    # --------------------------------------------------------

    if not nome_aluno.strip():

        st.error(
            "⚠️ Por favor, preencha o nome do aluno."
        )

    elif senha_acesso != "MAPLE2026":

        st.error(
            "🔒 Senha incorreta."
        )

    elif not selecoes_pf and not selecoes_nm:

        st.warning(
            "⚠️ Selecione pelo menos um critério como "
            "'Ponto Forte' ou 'A aperfeiçoar'."
        )

    else:

        # ----------------------------------------------------
        # GERAÇÃO
        # ----------------------------------------------------

        with st.spinner(
            "✍️ Redigindo comentário individualizado..."
        ):

            try:

                texto = gerar_comentario(
                    nome_aluno=nome_aluno.strip(),
                    disciplina=disc_selecionada,
                    pontos_fortes=selecoes_pf,
                    pontos_a_aprimorar=selecoes_nm,
                    sugestoes=sugestoes_finais
                )


                # --------------------------------------------
                # SALVA NA SESSÃO
                # --------------------------------------------

                st.session_state["ultimo_comentario"] = texto


                # --------------------------------------------
                # RESULTADO
                # --------------------------------------------

                st.subheader(
                    "📝 Resultado Final"
                )

                st.success(texto)


                st.text_area(
                    "Comentário para copiar:",
                    value=texto,
                    height=180
                )


            # ------------------------------------------------
            # ERRO DE QUOTA / CRÉDITO
            # ------------------------------------------------

            except Exception as e:

                erro = str(e)

                if (
                    "429" in erro
                    or "insufficient_quota" in erro
                    or "credit_balance_exhausted" in erro
                ):

                    st.error(
                        "💳 A API da OpenAI está sem créditos "
                        "disponíveis para este projeto."
                    )

                    st.info(
                        "Verifique o saldo e a cobrança da API "
                        "da OpenAI. A assinatura do ChatGPT e "
                        "os créditos da API são separados."
                    )


                # --------------------------------------------
                # API KEY
                # --------------------------------------------

                elif (
                    "401" in erro
                    or "invalid_api_key" in erro
                    or "Incorrect API key" in erro
                ):

                    st.error(
                        "🔑 A chave da API da OpenAI é inválida "
                        "ou não está configurada corretamente."
                    )


                # --------------------------------------------
                # LIMITE DE REQUISIÇÕES
                # --------------------------------------------

                elif (
                    "rate_limit" in erro
                    or "Rate limit" in erro
                ):

                    st.warning(
                        "⏳ A API atingiu temporariamente o "
                        "limite de requisições. Aguarde alguns "
                        "segundos e tente novamente."
                    )


                # --------------------------------------------
                # OUTROS ERROS
                # --------------------------------------------

                else:

                    st.error(
                        "❌ Ocorreu um erro ao gerar o comentário."
                    )

                    st.code(
                        erro,
                        language="text"
                    )


# ============================================================
# MOSTRAR ÚLTIMO RESULTADO
# ============================================================

if (
    "ultimo_comentario" in st.session_state
    and not gerar
):

    st.subheader(
        "📝 Último comentário gerado"
    )

    st.success(
        st.session_state["ultimo_comentario"]
    )

    st.text_area(
        "Comentário para copiar:",
        value=st.session_state["ultimo_comentario"],
        height=180
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🐻 Gerador de Report Card • Maple Bear • Versão 3.0"
)
