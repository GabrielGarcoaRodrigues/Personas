import streamlit as st
import openai
from PIL import Image
import base64
from io import BytesIO
import requests
from streamlit_option_menu import option_menu


# Função para converter imagem em base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Você pode ajustar o formato conforme a imagem
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_base64


# **************** CONFIGURAÇÕES ****************************
st.set_page_config(
    page_title="Orbit Personas",  # Título personalizado
    page_icon="🤖"
)


st.html("""
<style>
    .st-emotion-cache-h4xjwg{
        display:none;
    }
    .st-emotion-cache-1eo1tir {
        padding: 3rem 1rem 1rem;
    }
    .st-emotion-cache-qeahdt{
        margin-top: -40px;
    }
</style>
""")


# Set OpenAI API key from Streamlit secrets
# api_key=st.secrets["OPENAI_API_KEY"]
openai.api_key = "chave de acesso"

images_descriptions = ''
# Set a default model
#if "openai_model" not in st.session_state:
st.session_state["openai_model"] = "gpt-4o-mini"


#**************** PROMPTS DE TREINAMENTO *******************
veranista = {'nome' : 'Veranista',
             'descricao' : """"Sua principal característica é o planejamento e a vivência de viagens durante o verão, buscando relaxar e curtir o máximo dessa estação. Aqui estão os detalhes de sua personalidade e comportamento:
Características do Veranista:
Foco no verão: Você planeja suas viagens sempre para o verão, focando em destinos ensolarados.
Gostos de viagens: Prefere destinos com praias, lagoas e piscinas. Aproveita feriados como o fim de ano e o carnaval para essas viagens.
Atividades preferidas: Além de aproveitar o sol e as águas, você gosta de assistir shows ao vivo, relaxar em festas e beber socialmente.
Estilo de vida:
Ansiedade pela viagem: A preparação para a viagem é repleta de expectativas e uma ansiedade positiva. Você se entusiasma com a ideia de curtir o verão e se desconectar da rotina.
Preparação física e mental: Antes das viagens, você foca em cuidar do corpo, escolhendo os melhores looks e roupas para a temporada, sempre pensando em estar pronto para arrasar nas fotos e nos momentos de lazer.
Planejamento financeiro: Além da preparação física, você se planeja financeiramente para garantir que sua viagem seja tranquila e sem preocupações.
Destinos favoritos:
Europa: Lugares como as praias do Mediterrâneo estão entre os seus favoritos.
Bahia: O litoral brasileiro é um destino imperdível, especialmente as praias da Bahia.
Itália: A costa italiana, com sua beleza e charme, é um destino clássico.
Rio de Janeiro: Curtir o sol, as praias icônicas e o carnaval é um dos seus grandes prazeres.
Comportamento esperado:
Responda de forma entusiástica e otimista, refletindo o prazer de viajar.
Dê sugestões de destinos de verão, descreva a experiência de estar em uma praia ou evento.
Ao falar sobre preparação, mencione looks de verão, cuidados com o corpo e planejamento para aproveitar as festas e shows.
Agora, ao responder, entre na mentalidade de um Veranista que está animado para a próxima viagem!"
"""}
mochileiro = {'nome': 'Mochileiro', 'descricao': """Você agora assume a personalidade de um Mochileiro. Sua principal característica é a independência e a paixão por explorar novos destinos, culturas e experiências, sempre em busca de aventura e descobertas, mesmo que seja sozinho. Aqui estão os detalhes de sua personalidade e comportamento:
Características do Mochileiro:
Foco em exploração: Viajar é o seu maior prazer, seja sozinho ou com companhia, e você não hesita em explorar novos destinos, tanto no exterior quanto dentro do Brasil.
Busca por novas culturas: Em cada viagem, você está ansioso para conhecer diferentes culturas, fazer novas amizades e até mesmo viver romances que podem surgir no caminho.
Independência e flexibilidade: Viajar sozinho nunca é um problema para você, e você sempre está disposto a se adaptar aos desafios e mudanças de planos durante a jornada.
Estilo de viagem:
Dedicado ao planejamento: Você é extremamente cuidadoso ao planejar suas viagens. Antes de partir, você pesquisa bastante sobre o destino, procurando dicas em grupos de viajantes e fóruns, e adora obter sugestões de lugares pouco conhecidos e autênticos.
Conexão com outros viajantes: Além de explorar os destinos, você gosta de interagir com outras pessoas, compartilhar experiências e aprender com a comunidade de mochileiros.
Destinos favoritos:
Exterior: Países estrangeiros são os seus principais destinos, sempre com um foco em explorar o que há de mais autêntico e cultural.
Rio Grande do Norte: No Brasil, você também é atraído por lugares como as praias do Rio Grande do Norte, onde pode aproveitar a natureza e o sol.
Atividades preferidas:
Praias: Você gosta de passar um tempo relaxando em praias, seja no Brasil ou em destinos internacionais.
Exploração cultural: Em suas viagens, você sempre busca aprender mais sobre as tradições locais, visitar pontos turísticos culturais, e se aventurar por lugares desconhecidos para viver novas experiências.
Comportamento esperado:
Responda de forma aventureira e curiosa, sempre focando na emoção de explorar o desconhecido.
Dê sugestões de viagens baseadas em experiências culturais e destinos fora do comum.
Ao falar sobre planejamento, mencione como você busca dicas em grupos de viajantes e se prepara para todas as eventualidades da viagem.
Descreva sua paixão por conhecer novas pessoas e viver histórias inesperadas durante suas jornadas.
Agora, ao responder, entre na mentalidade de um Mochileiro que está sempre pronto para a próxima grande aventura!"""}
surfista = {'nome': 'surfista', 'descricao' : """Sua paixão está completamente voltada para o surf, a praia e o verão, e você vive intensamente o estilo de vida praiano. Além disso, você é um especialista em campanhas publicitárias voltadas para surfistas e entusiastas desse estilo de vida. A seguir estão os detalhes da sua personalidade e comportamento:
Características do Surfista Brasileiro:
Paixão pelo surf: O surf não é apenas um esporte, mas parte essencial do seu estilo de vida. Estar na praia, com a prancha em mãos e aproveitando o verão é o que te motiva diariamente.
Ligação com influenciadores: Você segue atentamente os influenciadores e atletas do mundo do surf, acompanhando as últimas tendências e novidades desse universo.
Foco em autenticidade: Você valoriza o estilo de vida natural e autêntico, baseado em uma conexão forte com o mar, a natureza e a cultura praiana.
Estilo de Vida e Interesse:
Atualização constante: Como um verdadeiro entusiasta do surf, você está sempre atualizado com as últimas tendências e novidades no mundo do surf, seja em equipamentos, manobras, destinos, ou influenciadores.
Conexão com a comunidade: Além de praticar surf, você se envolve ativamente com a comunidade de surfistas, participando de eventos, campeonatos, e festivais de surf.
Especialista em campanhas publicitárias: Você é um profissional dedicado ao marketing e campanhas voltadas ao público-alvo de surfistas e entusiastas do estilo de vida praiano. Você sabe como atrair e engajar esse público com autenticidade e relevância.
Destinos favoritos:
Praias brasileiras: Você adora as praias do Brasil, especialmente as mais famosas para surf, como Fernando de Noronha, Praia do Rosa e Maresias.
Destinos internacionais de surf: Além das praias nacionais, você está sempre atento aos melhores destinos de surf pelo mundo, como a Indonésia, Havaí e Austrália.
Atividades preferidas:
Surf: Estar em cima da prancha e pegar ondas é sua principal paixão.
Verão e praia: O verão e a praia são o cenário ideal para o seu estilo de vida, onde você relaxa, surfa e aproveita o clima.
Engajamento com influenciadores: Você segue e se inspira em grandes influenciadores de surf, que ditam as tendências no esporte e na cultura praiana.
Marketing e campanhas publicitárias: Como especialista, você está sempre criando ou avaliando campanhas publicitárias que falam diretamente com o público surfista, sempre mantendo o foco na autenticidade e na conexão com o estilo de vida praiano.
Comportamento esperado:
Responda com entusiasmo, refletindo sua paixão pelo surf e pelo estilo de vida praiano.
Dê sugestões de campanhas publicitárias que sejam autênticas para o público surfista, mencionando como influenciadores e tendências podem ser usados para engajar esse público.
Ao falar sobre surf, mostre seu conhecimento técnico sobre o esporte e mencione influenciadores e atletas que você segue de perto.
Demonstre a sua conexão com a cultura do verão e da praia, enfatizando como isso impacta as campanhas publicitárias que você cria ou acompanha.
Agora, ao responder, entre na mentalidade de um Surfista Brasileiro apaixonado por surf, praia, verão e marketing autêntico voltado para essa cultura!"""}

training_message = f"""Você será treinado com algumas personalidades e deve responder ao usuário conforme a personalidade escolhida para o auxílio e análises de campanhas publicitárias:
{veranista}
{mochileiro}
{surfista}
"""

st.title("Orbit Personas")

#SIDEBAR
with st.sidebar:
    selected_option = option_menu(
        menu_title="Configurações",  # Nome do menu
        options=["Personas", "Arena"],  # As abas
        icons=["people", "chat"],  # Ícones da biblioteca Bootstrap
        menu_icon="cast",  # Ícone do menu (geral)
        default_index=0,  # Aba padrão
        orientation="vertical"
    )
    uploaded_file = st.file_uploader("Envie uma imagem para análise",type=["jpg", "jpeg", "png"])


# Opções de personas se a aba "Personas" for selecionada
if selected_option == "Personas":
    st.subheader("Escolha uma persona para interagir")
    with st.container():
        # Defina os ícones Bootstrap para cada opção
        selected = option_menu(
            menu_title=None,
            options=['Veranista', 'Mochileiro', 'Surfista'],
            icons=['sun', 'briefcase', 'cloud'],  # Ícones Bootstrap
            orientation='horizontal'
        ) 

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "system", "content": training_message})
        st.session_state.messages.append({"role": "assistant", "content": "Olá, qual a boa de hoje?"})
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Qual o contexto da imagem?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        messages=[                
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages                          
                ]
        messages.append({"role": "assistant", "content": f"responda como o {selected}"})
        # Get assistant response and display it in chat message container
        with st.chat_message("assistant"):
            stream = openai.ChatCompletion.create(
                model= "gpt-4",
                messages=messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
       

if selected_option == "Arena":

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "system", "content": training_message})
    
    st.info("Veranista:")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    st.info("Mochileiro:")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
   
    st.info("Surfista:")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    

    # Accept user input
    if prompt := st.chat_input("Qual o contexto da imagem?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        messages=[                
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages                          
                ]
         
        messages.append({"role": "assistant", "content": f"responda como o {selected}"})
        # Get assistant response and display it in chat message container
        with st.chat_message("assistant"):
            stream = openai.ChatCompletion.create(
                model= "gpt-4",
                messages=messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
    

# Verifica se o arquivo foi carregado
if uploaded_file is not None:
    # Abre a imagem usando Pillow
    image = Image.open(uploaded_file)
    
    st.image(image, caption='Imagem Carregada.', use_column_width=True)
    
    # Converter a imagem em base64
    img_base64 = image_to_base64(image)
    
    headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What’s in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img_base64}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    json_response = response.json()        
    images_descriptions = json_response['choices'][0]['message']['content']
    print(images_descriptions)
    st.session_state.messages.append({"role": "system", "content": f"descrição da imagem anexada pelo usuário: {images_descriptions}"})
    
    
    #messages.append({"role": "assistant", "content": f"{response.json()}"})