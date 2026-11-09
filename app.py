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
# INSTRUÇÕES DA IA
# ============================================================

SYSTEM_INSTRUCTION = """
Você é um professor experiente da Maple Bear, responsável pela
elaboração de comentários de Report Card.

Sua tarefa é produzir comentários individualizados, naturais,
profissionais, acolhedores e pedagogicamente precisos.

PRIORIDADE DAS INFORMAÇÕES:

1. As observações adicionais escritas pelo professor são
   OBRIGATÓRIAS e devem ser consideradas prioritárias.

2. TODAS as informações relevantes presentes nas observações
   do professor devem aparecer no comentário final.

3. É PROIBIDO ignorar, omitir ou eliminar informações
   comportamentais, acadêmicas ou sociais mencionadas pelo professor.

4. Os critérios selecionados devem complementar as observações,
   nunca substituí-las.

5. Se o professor mencionar dificuldades de comportamento,
   como conversas excessivas, falta de respeito, atitudes rudes,
   dificuldade de concentração, interrupções ou falta de
   comprometimento, essas questões DEVEM aparecer explicitamente
   no comentário final.

6. Não transforme uma dificuldade comportamental em uma
   recomendação genérica que esconda o problema.

7. Preserve o significado e a importância das observações,
   utilizando linguagem profissional, respeitosa e construtiva.

8. Exemplo:
   Observação: "O aluno conversa demais durante as explicações."

   Forma adequada:
   "Precisa desenvolver maior autorregulação durante as aulas,
   evitando conversas paralelas que possam comprometer sua
   concentração e os momentos de aprendizagem."

9. Exemplo:
   Observação: "O aluno foi rude com colegas."

   Forma adequada:
   "Precisa desenvolver uma comunicação mais respeitosa
   nas interações com os colegas, demonstrando maior
   consideração pelas pessoas ao seu redor."

REGRAS DE REDAÇÃO:

10. Escreva somente um único parágrafo.

11. Não utilize listas, tópicos, títulos ou marcadores.

12. O texto deve parecer escrito por um professor que conhece
    o aluno.

13. Utilize predominantemente o passado para descrever
    desempenhos já demonstrados.

14. Utilize o presente para recomendações e aspectos
    que precisam ser desenvolvidos.

15. Comece destacando aspectos positivos quando houver
    pontos fortes selecionados.

16. Apresente as dificuldades de maneira construtiva,
    mas sem esconder sua natureza ou importância.

17. Não repita o nome do aluno desnecessariamente.

18. Não invente comportamentos, notas, projetos ou
    características que não foram fornecidos.

19. Varie a construção das frases para evitar comentários
    excessivamente semelhantes.

20. O comentário deve ter aproximadamente 100 a 150 palavras.
    Se houver muitas observações relevantes, poderá ultrapassar
    esse limite para não omitir informações importantes.

21. Não copie mecanicamente as observações do professor.
    Transforme-as em uma redação natural, preservando
    integralmente seu significado.

22. Não mencione inteligência artificial, ChatGPT ou OpenAI.

23. O resultado final deve conter apenas o comentário,
    sem explicações adicionais.
"""


# ============================================================
# FUNÇÃO PARA GERAR O COMENTÁRIO
# ============================================================

def gerar_comentario(
    nome_aluno,
    disciplina,
    pontos_fortes,
    pontos_a_aprimorar,
    sugestoes,
    observacoes_professor
):

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

    observacoes_texto = (
        observacoes_professor.strip()
        if observacoes_professor.strip()
        else "Nenhuma observação adicional foi fornecida."
    )


    # --------------------------------------------------------
    # INSTRUÇÕES DO USUÁRIO
    # --------------------------------------------------------

    user_instruction = f"""
Aluno: {nome_aluno}

Disciplina: {disciplina}

PONTOS FORTES IDENTIFICADOS:
{pontos_fortes_texto}

ASPECTOS ACADÊMICOS A APRIMORAR:
{pontos_aprimorar_texto}

SUGESTÕES DE DESENVOLVIMENTO:
{sugestoes_texto}

OBSERVAÇÕES INDIVIDUAIS DO PROFESSOR:
{observacoes_texto}

INSTRUÇÃO FUNDAMENTAL:

Antes de escrever, identifique mentalmente todas as informações
presentes nas observações individuais do professor.

Certifique-se de que cada informação relevante esteja representada
no comentário final.

Não priorize a fluidez do texto em detrimento da fidelidade
às observações.

Se o professor mencionou três dificuldades diferentes,
as três devem ser contempladas no comentário.

Produza um único parágrafo de Report Card, integrando
as informações acadêmicas e comportamentais de maneira natural.

As observações do professor são informações factuais fornecidas
pelo educador. Não as descarte nem as substitua por suposições.
"""


    # --------------------------------------------------------
    # CHAMADA À API - RESPONSES API
    # --------------------------------------------------------

    resposta = client.responses.create(
        model="gpt-4o-mini",
        instructions=SYSTEM_INSTRUCTION,
        input=user_instruction,
        temperature=0.3,
        max_output_tokens=400
    )

    texto = resposta.output_text.strip()

    if not texto:
        raise ValueError("A API retornou um comentário vazio.")

    return texto


# ============================================================
# INTERFACE
# ============================================================

st.title("🐻 Gerador de Report Card - Maple Bear")

st.caption(
    "Versão 3.2 • High School & Middle Years"
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
        "nos critérios selecionados e nas observações do professor."
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

st.subheader("📊 Avaliação dos critérios")

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
# OBSERVAÇÕES ADICIONAIS DO PROFESSOR
# ============================================================

st.subheader("📝 Observações adicionais do professor")

st.caption(
    "Utilize este espaço para acrescentar informações específicas "
    "sobre o desempenho, a evolução, o comportamento ou as "
    "particularidades do aluno."
)

observacoes_professor = st.text_area(
    "Comentário do professor:",
    placeholder=(
        "Ex.: O aluno apresentou uma evolução significativa "
        "neste trimestre, mas conversa excessivamente durante "
        "as explicações e precisa desenvolver maior respeito "
        "pelos momentos de aprendizagem dos colegas..."
    ),
    height=150,
    help=(
        "Campo opcional. As observações serão consideradas "
        "prioritárias na elaboração do comentário final."
    )
)


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

    elif not selecoes_pf and not selecoes_nm and not observacoes_professor.strip():

        st.warning(
            "⚠️ Selecione pelo menos um critério ou "
            "acrescente uma observação do professor."
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
                    sugestoes=sugestoes_finais,
                    observacoes_professor=observacoes_professor
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
                    height=180,
                    key="comentario_gerado"
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
        height=180,
        key="ultimo_comentario_copiar"
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🐻 Gerador de Report Card • Maple Bear • Versão 3.2"
)
