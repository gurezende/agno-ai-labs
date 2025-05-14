# Imports
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools

# Create individual specialized agents
writer = Agent(
    name="Marketer",
    role=dedent("""\
                Você é um experiente profissional de marketing digital especializado em posts do Instagram.
                Você sabe como escrever um post envolvente e otimizado para SEO.
                Você sabe tudo sobre vinhos, queijos, e comidas refinadas encontradas em empórios.
                Você também é um sommelie especializado em vinhos que sabe fazer recomendações.
                Escreva um conteúdo claro e envolvente, usando um tom neutro a divertido.
                Escreva uma legenda de Instagram sobre o {tópico} solicitado.
                Escreva um call to action curto ao final da mensagem.     
                \
                """),
    tools=[DuckDuckGoTools(), GoogleSearchTools()],
    expected_output=dedent("""\
                           Legenda para Instagram sobre o {tópico} solicitado.
                           \
                           """),
    model=Gemini(id="gemini-2.0-flash-lite", api_key=os.environ.get("GEMINI_API_KEY")),
    exponential_backoff=True,
    delay_between_retries=2
)

illustrator = Agent(
    name="Ilustrador",
    role=dedent("""\
                Você é um ilustrador especializado em ilustrar vinhos, queijos, e comidas refinadas encontradas em empórios.
                Baseado na legenda criada pelo Marketer, crie um prompt para gerar uma foto envolvente sobre o {tópico} solicitado.
                \
                """),
    expected_output= "Prompt para gerar foto",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    exponential_backoff=True,
    delay_between_retries=2
)

# Create a team with these agents
writing_team = Team(
    name="Instagram Team",
    mode="coordinate",
    members=[writer, illustrator],
    instructions=dedent("""\
                        Vocês são uma equipe de escritores que trabalham juntos para criar posts envolventes para o Instagram.
                        Primeiro, vocês peça ao Marketer para criar uma legenda para o {tópico} solicitado.
                        Depois, vocês peça ao Ilustrador para criar um prompt para gerar uma ilustração envolvente para o {tópico} solicitado.
                        Não utilize emojis na legenda.
                        Se encontrar erro de character encoding, remova o caracter antes de salvar o arquivo.
                        Use o modelo seguinte para gerar o output:
                        - Postagem
                        - Prompt para gerar uma ilustração
                        \
                        """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    tools=[FileTools()],
    expected_output="Um arquivo de texto 'post.txt' com o postagem e o prompt para gerar uma ilustração.",
    markdown=True,
    monitoring=True
)

# Run the team with a task
writing_team.print_response("Crie uma postagem sobre o tópico: 'Vinho Sterling Merlot e sugestão de acompanhamento'.")