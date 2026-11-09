import json
import os
import re
from io import BytesIO

import streamlit as st
from openai import OpenAI


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Gerador Maple Bear - Report Cards",
    page_icon="🐻",
    layout="wide",
)


# ============================================================
# CONFIGURAÇÕES E SEGURANÇA
# ============================================================

def get_secret(name, default=None):
    """Lê um segredo do Streamlit sem quebrar quando secrets.toml não existe."""
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.getenv(name, default)


api_key = get_secret("key_Blt0IvBeKyKdMnY1") or os.getenv("key_Blt0IvBeKyKdMnY1")
app_password = get_secret("maple2026") or os.getenv("maple2026")

if not api_key:
    st.error(
        "A chave OPENAI_API_KEY não foi encontrada. "
        "Configure-a nos Secrets do Streamlit Cloud."
    )
    st.stop()

if not app_password:
    st.error(
        "A senha compartilhada não foi configurada. "
        "Adicione APP_PASSWORD aos Secrets do Streamlit Cloud."
    )
    st.stop()

try:
    client = OpenAI(api_key=api_key)
except Exception as exc:
    st.error(f"Não foi possível inicializar a API da OpenAI: {exc}")
    st.stop()


# ============================================================
# DADOS PEDAGÓGICOS POR DISCIPLINA
# ============================================================

DADOS_DISCIPLINAS = {
    "Matemática": {
        "Compreensão de conceitos": [
            "Revisitar registros e definições teóricas",
            "Relacionar conceitos abstratos com situações cotidianas",
            "Explicar conceitos com as próprias palavras",
            "Estabelecer conexões entre diferentes tópicos",
            "Utilizar recursos visuais ou softwares gráficos",
        ],
        "Resolução de problemas": [
            "Aprimorar a interpretação de dados e enunciados",
            "Explorar diferentes estratégias de resolução",
            "Validar as estratégias e os resultados encontrados",
            "Utilizar esquemas visuais para modelar situações",
            "Identificar informações relevantes em problemas complexos",
        ],
        "Aplicação de procedimentos": [
            "Organizar as etapas de resolução",
            "Ter atenção aos sinais e às propriedades operatórias",
            "Praticar algoritmos e procedimentos matemáticos",
            "Conferir resultados parciais e finais",
            "Desenvolver maior rigor na escrita matemática",
        ],
        "Comunicação matemática": [
            "Utilizar vocabulário matemático com precisão",
            "Justificar o raciocínio utilizado",
            "Estruturar respostas de forma lógica e sequencial",
            "Empregar notação matemática adequadamente",
            "Interpretar e apresentar gráficos e tabelas",
        ],
        "Raciocínio lógico e representações": [
            "Identificar padrões e relações matemáticas",
            "Comparar diferentes representações de um conceito",
            "Relacionar expressões algébricas e representações gráficas",
            "Desenvolver estratégias de generalização",
        ],
    },
    "Matemática Aplicada": {
        "Compreensão de conceitos": [
            "Relacionar conceitos matemáticos a situações reais",
            "Explicar conceitos com as próprias palavras",
            "Identificar padrões em situações do cotidiano",
            "Comparar diferentes estratégias e modelos",
        ],
        "Resolução de problemas": [
            "Aprimorar a interpretação de dados",
            "Fragmentar problemas complexos em etapas",
            "Testar hipóteses e validar estratégias",
            "Analisar a coerência dos resultados obtidos",
        ],
        "Aplicação e modelagem": [
            "Construir modelos para representar situações reais",
            "Selecionar ferramentas matemáticas adequadas",
            "Interpretar as limitações de um modelo",
            "Aplicar conceitos em contextos variados",
        ],
        "Análise de dados e tomada de decisões": [
            "Interpretar tabelas, gráficos e indicadores",
            "Comparar informações quantitativas",
            "Justificar decisões com base em dados",
            "Avaliar possíveis consequências de diferentes escolhas",
        ],
        "Comunicação de resultados": [
            "Apresentar conclusões de forma clara",
            "Utilizar vocabulário técnico adequado",
            "Justificar escolhas e procedimentos",
            "Organizar relatórios e apresentações",
        ],
    },
    "História": {
        "Conhecimento e compreensão histórica": [
            "Revisitar conceitos e termos históricos",
            "Relacionar eventos e diferentes períodos",
            "Identificar causas e consequências",
            "Analisar contextos sociais, políticos e econômicos",
            "Contextualizar acontecimentos em seu período histórico",
        ],
        "Análise de fontes e pesquisa": [
            "Diversificar as fontes de pesquisa",
            "Analisar documentos e fontes primárias",
            "Distinguir evidências de interpretações",
            "Organizar referências bibliográficas",
            "Contextualizar a autoria e o contexto das fontes",
        ],
        "Pensamento crítico e interpretação": [
            "Analisar diferentes perspectivas históricas",
            "Argumentar com base em evidências",
            "Relacionar o passado com questões do presente",
            "Avaliar impactos de decisões históricas",
            "Reconhecer diferentes experiências e perspectivas",
        ],
        "Comunicação e argumentação": [
            "Melhorar a clareza e a organização textual",
            "Estruturar argumentos em textos e ensaios",
            "Utilizar evidências para sustentar interpretações",
            "Participar de debates de forma fundamentada",
            "Utilizar vocabulário histórico com precisão",
        ],
    },
}


LEARNING_BEHAVIOURS = {
    "Personal Management": (
        "Organização, autonomia, responsabilidade, gestão do tempo "
        "e cumprimento de tarefas."
    ),
    "Active Participation": (
        "Participação, concentração, envolvimento nas atividades "
        "e contribuição para as situações de aprendizagem."
    ),
    "Social Responsibility": (
        "Respeito, colaboração, escuta, convivência e responsabilidade "
        "nas interações com colegas e professores."
    ),
}

STATUS_ACADEMICO = [
    "Não avaliado",
    "Ponto forte",
    "Adequado",
    "A desenvolver",
]

STATUS_COMPORTAMENTAL = [
    "Não avaliado",
    "Ponto forte",
    "Adequado",
    "A desenvolver",
]


# ============================================================
# INSTRUÇÕES DA IA
# ============================================================

SYSTEM_INSTRUCTION = """
Você é um educador experiente da Maple Bear e redige comentários
de Report Card em português.

Produza um comentário individualizado, natural, profissional,
acolhedor, objetivo e pedagogicamente preciso.

REGRAS DE FIDELIDADE:
1. As observações individuais do professor são prioritárias.
2. Preserve todas as informações relevantes das observações.
3. Não omita fatos acadêmicos, comportamentais ou sociais.
4. Não substitua uma observação específica por uma recomendação vaga.
5. Transforme a linguagem em redação profissional sem alterar o sentido.
6. Não invente notas, comportamentos, projetos, resultados ou características.
7. Se houver uma dificuldade comportamental explícita, ela deve aparecer
   de maneira clara e respeitosa no comentário.
8. Se houver várias observações distintas, contemple cada uma.
9. As sugestões de desenvolvimento complementam os registros; não os substituem.

REGRAS PEDAGÓGICAS:
10. Diferencie desempenho acadêmico de Learning Behaviours.
11. Integre as duas dimensões naturalmente em um único parágrafo.
12. Considere os conteúdos trabalhados apenas como contexto; não presuma
    domínio de conteúdos que não foi informado.
13. Não transforme "Adequado" em elogio excepcional nem "A desenvolver"
    em uma afirmação de fracasso.
14. Use linguagem construtiva, mas não esconda a natureza de uma dificuldade.

REGRAS DE REDAÇÃO:
15. Escreva somente um parágrafo, sem título, lista ou marcadores.
16. Comece por aspectos positivos quando houver evidências de pontos fortes.
17. Use passado para descrever desempenhos demonstrados e presente/futuro
    para indicar aspectos a desenvolver.
18. Evite repetir o nome do aluno desnecessariamente.
19. Varie a construção das frases e evite elogios automáticos.
20. Não mencione inteligência artificial, ChatGPT ou OpenAI.
21. O resultado deve conter apenas o comentário.
"""


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def chamar_modelo(instrucoes, entrada, max_tokens=700):
    resposta = client.responses.create(
        model="gpt-4o-mini",
        instructions=instrucoes,
        input=entrada,
        temperature=0.3,
        max_output_tokens=max_tokens,
    )
    texto = (resposta.output_text or "").strip()
    if not texto:
        raise ValueError("A API retornou uma resposta vazia.")
    return texto


def gerar_comentario(
    nome_aluno,
    turma,
    ano_escolar,
    trimestre,
    disciplina,
    conteudos,
    pontos_fortes,
    aspectos_adequados,
    pontos_a_desenvolver,
    sugestoes,
    comportamentos,
    observacoes_professor,
    tamanho,
):
    dados = f"""
IDENTIFICAÇÃO
Aluno: {nome_aluno}
Turma: {turma or "Não informada"}
Ano escolar: {ano_escolar or "Não informado"}
Trimestre: {trimestre or "Não informado"}
Disciplina: {disciplina}

CONTEÚDOS TRABALHADOS
{conteudos or "Não informado."}

DESEMPENHO ACADÊMICO
Pontos fortes: {", ".join(pontos_fortes) if pontos_fortes else "Não foram selecionados."}
Desempenho adequado: {", ".join(aspectos_adequados) if aspectos_adequados else "Não foram selecionados."}
Aspectos a desenvolver: {", ".join(pontos_a_desenvolver) if pontos_a_desenvolver else "Não foram selecionados."}
Sugestões de desenvolvimento: {", ".join(sugestoes) if sugestoes else "Não foram selecionadas."}

LEARNING BEHAVIOURS
{json.dumps(comportamentos, ensure_ascii=False, indent=2)}

OBSERVAÇÕES INDIVIDUAIS DO PROFESSOR
{observacoes_professor.strip() if observacoes_professor.strip() else "Nenhuma observação adicional fornecida."}

TAMANHO DESEJADO
{tamanho}
"""
    pedido = """
Redija o comentário de Report Card em português, em um único parágrafo.
Integre o desempenho acadêmico e os Learning Behaviours, sem criar
uma lista de critérios. Dê prioridade às observações individuais.
Não invente informações. Respeite o tamanho solicitado, mas não omita
fatos relevantes apenas para atingir uma contagem de palavras.
"""
    return chamar_modelo(SYSTEM_INSTRUCTION, dados + "\n\n" + pedido)


def auditar_cobertura(observacoes, comentario):
    """
    Verifica se as informações das observações do professor aparecem
    no comentário. Retorna None se a resposta da auditoria não puder
    ser interpretada com segurança.
    """
    if not observacoes.strip():
        return {"all_covered": True, "missing": [], "notes": "Sem observações adicionais."}

    instrucoes = """
Você é um verificador de fidelidade de comentários escolares.
Compare as observações originais do professor com o comentário final.
Identifique cada fato, comportamento, avanço ou dificuldade distinto
nas observações e verifique se está representado no comentário.
Não exija as mesmas palavras: avalie a preservação do significado.
Não considere uma menção genérica suficiente quando a observação é específica.
Responda exclusivamente em JSON válido, neste formato:
{
  "all_covered": true,
  "missing": ["descrição objetiva do item omitido"],
  "notes": "breve justificativa"
}
Se nada relevante estiver faltando, use all_covered=true e missing=[].
"""
    entrada = f"""
OBSERVAÇÕES ORIGINAIS:
{observacoes}

COMENTÁRIO GERADO:
{comentario}
"""
    resultado = chamar_modelo(instrucoes, entrada, max_tokens=350)
    resultado = re.sub(r"^```(?:json)?\s*|\s*```$", "", resultado.strip(), flags=re.I)
    try:
        dados = json.loads(resultado)
        if not isinstance(dados, dict) or "all_covered" not in dados:
            return None
        dados.setdefault("missing", [])
        dados.setdefault("notes", "")
        return dados
    except (json.JSONDecodeError, TypeError):
        return None


def revisar_comentario(observacoes, comentario, itens_faltantes):
    instrucoes = SYSTEM_INSTRUCTION + """
Revise o comentário para incluir as informações indicadas como ausentes.
Preserve o que já está correto. Não acrescente fatos que não estejam
nas observações ou nos dados originais. Mantenha um único parágrafo.
"""
    entrada = f"""
OBSERVAÇÕES ORIGINAIS DO PROFESSOR:
{observacoes}

COMENTÁRIO ATUAL:
{comentario}

INFORMAÇÕES QUE PRECISAM SER CONTEMPLADAS:
{json.dumps(itens_faltantes, ensure_ascii=False)}

Revise o comentário sem omitir nenhum desses pontos.
"""
    return chamar_modelo(instrucoes, entrada, max_tokens=850)


def criar_docx(texto, nome_aluno, disciplina):
    from docx import Document
    from docx.shared import Pt

    documento = Document()
    documento.add_heading("Maple Bear - Report Card Comment", level=1)
    documento.add_paragraph(f"Aluno: {nome_aluno}")
    documento.add_paragraph(f"Disciplina: {disciplina}")
    paragrafo = documento.add_paragraph(texto)
    for run in paragrafo.runs:
        run.font.name = "Arial"
        run.font.size = Pt(11)

    arquivo = BytesIO()
    documento.save(arquivo)
    arquivo.seek(0)
    return arquivo.getvalue()


def limpar_resultado():
    for chave in ("comentario_atual", "auditoria_atual", "comentario_editor"):
        st.session_state.pop(chave, None)


# ============================================================
# AUTENTICAÇÃO COMPARTILHADA
# ============================================================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🐻 Gerador de Report Card - Maple Bear")
    st.subheader("Acesso dos professores")
    with st.form("form_login"):
        senha_digitada = st.text_input("Senha compartilhada", type="password")
        entrar = st.form_submit_button("Entrar", use_container_width=True)
    if entrar:
        if senha_digitada == app_password:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()


# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

st.title("🐻 Gerador de Report Card - Maple Bear")
st.caption("Versão 3.3 • High School & Middle Years")

with st.sidebar:
    st.header("Identificação do aluno")
    nome_aluno = st.text_input("Nome do aluno", placeholder="Nome completo")
    turma = st.text_input("Turma", placeholder="Ex.: Year 8A")
    ano_escolar = st.text_input("Ano escolar", placeholder="Ex.: Year 8")
    trimestre = st.selectbox("Período", ["1º trimestre", "2º trimestre", "3º trimestre"])
    disciplina = st.selectbox("Disciplina", list(DADOS_DISCIPLINAS.keys()))
    st.divider()
    if st.button("Sair", use_container_width=True):
        st.session_state["autenticado"] = False
        limpar_resultado()
        st.rerun()
    st.caption("Acesso compartilhado. Não insira dados pessoais sensíveis.")

st.subheader("1. Conteúdos trabalhados")
conteudos = st.text_area(
    "Registre os principais conteúdos abordados no período",
    placeholder="Ex.: função quadrática, propriedades das potências e função exponencial...",
    height=90,
)

st.divider()
st.subheader("2. Desempenho acadêmico")
st.caption("Selecione o status de cada critério. As sugestões aparecem quando o critério está marcado como 'A desenvolver'.")

pontos_fortes = []
aspectos_adequados = []
pontos_a_desenvolver = []
sugestoes_selecionadas = []

criterios = list(DADOS_DISCIPLINAS[disciplina].items())
colunas = st.columns(2)

for indice, (criterio, sugestoes) in enumerate(criterios):
    with colunas[indice % 2]:
        st.markdown(f"**{criterio}**")
        status = st.radio(
            "Avaliação",
            STATUS_ACADEMICO,
            index=0,
            key=f"status_{disciplina}_{criterio}",
            horizontal=False,
            label_visibility="collapsed",
        )
        if status == "Ponto forte":
            pontos_fortes.append(criterio)
        elif status == "Adequado":
            aspectos_adequados.append(criterio)
        elif status == "A desenvolver":
            pontos_a_desenvolver.append(criterio)
            with st.expander("Sugestões de desenvolvimento"):
                for i, sugestao in enumerate(sugestoes):
                    if st.checkbox(sugestao, key=f"sug_{disciplina}_{criterio}_{i}"):
                        sugestoes_selecionadas.append(f"{criterio}: {sugestao}")
        st.divider()

st.subheader("3. Learning Behaviours")
st.caption("Avalie os comportamentos de aprendizagem separadamente do desempenho acadêmico.")

comportamentos = {}
cols_beh = st.columns(3)
for indice, (nome, descricao) in enumerate(LEARNING_BEHAVIOURS.items()):
    with cols_beh[indice]:
        st.markdown(f"**{nome}**")
        st.caption(descricao)
        comportamentos[nome] = st.radio(
            "Status",
            STATUS_COMPORTAMENTAL,
            index=0,
            key=f"beh_{nome}",
            label_visibility="collapsed",
        )

st.divider()
st.subheader("4. Observações individuais do professor")
observacoes_professor = st.text_area(
    "Registre informações específicas que precisam aparecer no comentário",
    placeholder=(
        "Ex.: O aluno apresentou evolução na resolução de problemas, "
        "mas conversa frequentemente durante as explicações e precisa "
        "respeitar os momentos de fala dos colegas."
    ),
    height=150,
    help="As observações são prioritárias e serão comparadas com o comentário gerado.",
)

st.subheader("5. Preferências do comentário")
tamanho = st.selectbox(
    "Extensão desejada",
    [
        "Breve (60 a 90 palavras)",
        "Padrão (100 a 150 palavras)",
        "Detalhado (150 a 200 palavras)",
    ],
    index=1,
)

tem_avaliacao = bool(
    pontos_fortes or aspectos_adequados or pontos_a_desenvolver
    or any(v != "Não avaliado" for v in comportamentos.values())
)

gerar = st.button(
    "✨ GERAR E VERIFICAR COMENTÁRIO",
    type="primary",
    use_container_width=True,
)

if gerar:
    if not nome_aluno.strip():
        st.error("Preencha o nome do aluno.")
    elif not tem_avaliacao and not observacoes_professor.strip():
        st.warning("Avalie pelo menos um critério ou registre uma observação.")
    else:
        try:
            with st.spinner("Redigindo o comentário..."):
                comentario = gerar_comentario(
                    nome_aluno=nome_aluno.strip(),
                    turma=turma.strip(),
                    ano_escolar=ano_escolar.strip(),
                    trimestre=trimestre,
                    disciplina=disciplina,
                    conteudos=conteudos.strip(),
                    pontos_fortes=pontos_fortes,
                    aspectos_adequados=aspectos_adequados,
                    pontos_a_desenvolver=pontos_a_desenvolver,
                    sugestoes=sugestoes_selecionadas,
                    comportamentos=comportamentos,
                    observacoes_professor=observacoes_professor,
                    tamanho=tamanho,
                )

            auditoria = None
            if observacoes_professor.strip():
                with st.spinner("Verificando se as observações foram contempladas..."):
                    auditoria = auditar_cobertura(observacoes_professor, comentario)

                if auditoria and not auditoria.get("all_covered", False):
                    faltantes = auditoria.get("missing", [])
                    if faltantes:
                        with st.spinner("Ajustando o comentário para contemplar os pontos identificados..."):
                            comentario = revisar_comentario(
                                observacoes_professor,
                                comentario,
                                faltantes,
                            )
                        with st.spinner("Realizando a verificação final..."):
                            auditoria = auditar_cobertura(observacoes_professor, comentario)

            st.session_state["comentario_atual"] = comentario
            st.session_state["auditoria_atual"] = auditoria
            st.session_state["comentario_editor"] = comentario

        except Exception as exc:
            erro = str(exc)
            if any(x in erro for x in ("insufficient_quota", "credit_balance_exhausted")) or "429" in erro:
                st.error("A API da OpenAI está sem créditos ou atingiu um limite temporário. Verifique o saldo e os limites do projeto.")
            elif "401" in erro or "invalid_api_key" in erro:
                st.error("A chave da API da OpenAI é inválida ou não está configurada corretamente.")
            elif "rate_limit" in erro.lower():
                st.warning("A API atingiu temporariamente o limite de requisições. Aguarde e tente novamente.")
            else:
                st.error("Ocorreu um erro durante a geração ou verificação.")
                st.code(erro)


# ============================================================
# REVISÃO DO RESULTADO - TEMPORÁRIO NA SESSÃO
# ============================================================

if "comentario_atual" in st.session_state:
    st.divider()
    st.subheader("6. Revisão do comentário")

    auditoria = st.session_state.get("auditoria_atual")
    if auditoria is None:
        st.warning("Não foi possível concluir a auditoria automaticamente. Revise manualmente todas as observações.")
    elif auditoria.get("all_covered", False):
        st.success("A verificação não identificou omissões nas observações do professor.")
    else:
        st.warning("A verificação ainda identificou possíveis informações ausentes. Revise o texto antes de utilizá-lo.")
        for item in auditoria.get("missing", []):
            st.write(f"- {item}")

    comentario_editado = st.text_area(
        "Edite o comentário, se necessário:",
        key="comentario_editor",
        height=220,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "📄 Exportar para Word",
            data=criar_docx(comentario_editado, nome_aluno, disciplina),
            file_name=f"Report_Card_{re.sub(r'[^A-Za-z0-9_-]+', '_', nome_aluno.strip())}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with col_b:
        if st.button("🗑️ Limpar resultado", use_container_width=True):
            limpar_resultado()
            st.rerun()

    st.caption("O comentário fica disponível apenas temporariamente nesta sessão. Não há histórico permanente no aplicativo.")


# ============================================================
# RODAPÉ
# ============================================================

st.divider()
st.caption("🐻 Gerador de Report Card • Maple Bear • Versão 3.3")
