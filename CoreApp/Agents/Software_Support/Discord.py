

# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT SoftwareAI Alfred
from softwareai.CoreApp.Agents.Software_Support.Alfred import Alfred
#########################################
name_app = "appx"
appfb = FirebaseKeysinit._init_app_(name_app)
key_openai = OpenAIKeysteste.keys()
client = OpenAIKeysinit._init_client_(key_openai)

class Discord:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True  # Ativa a intenção de conteúdo das mensagens
        self.client_Discord = commands.Bot(command_prefix="!", intents=self.intents)
        self.TelegramTOKEN = sys.argv[1]
        self.CHANNEL_ID = sys.argv[2]
        self.Discord_token = sys.argv[3]

        Alfredclass = Alfred()
        Alfred_NordVPN_Auto_Rotate = Alfredclass.NordVPN_Auto_Rotate(
                    appfb,
                    client,
                    self.TelegramTOKEN,
                    self.CHANNEL_ID,
                    self.Discord_token
                    )
        self.Alfred = Alfred_NordVPN_Auto_Rotate.Alfred


    async def send_image_to_discord(self, image_path, caption=None):
        """
        Envia uma imagem para o canal do Discord.
        :param image_path: Caminho ou URL da imagem a ser enviada.
        :param caption: Texto opcional para incluir como legenda.
        """
        try:
            channel = self.client.get_channel(self.CHANNEL_ID)
            await channel.send(content=caption, file=discord.File(image_path))
            print(f"Imagem enviada para o canal {self.CHANNEL_ID}.")
        except Exception as e:
            print(f"Erro ao enviar imagem para o canal: {e}")


    def main_discord(self):

        @self.client_Discord.event
        async def on_ready():
            print(f'Bot conectado como {self.client_Discord.user}')

        @self.client_Discord.event
        async def on_message(message):
            if message.author == self.client_Discord.user:
                return
            messagecontent = message.content
            Alfred_response, Deletemessage, Infractions, BanUser, total_tokens, prompt_tokens, completion_tokens = self.Alfred(messagecontent, message.author)

            # Deletar mensagem
            if Deletemessage:
                try:
                    await message.delete()
                except Exception as e:
                    print(f"Erro ao tentar deletar a mensagem: {e}")

            # Banir usuário
            if BanUser:
                await message.channel.send(Alfred_response)
                try:
                    await message.guild.ban(member=message.author)
                    print(f"Usuário {message.author} foi banido do servidor {message.guild.id}.")
                except Exception as e:
                    print(f"Erro ao tentar banir o usuário {message.author}: {e}")


            await message.channel.send(Alfred_response)

        @self.client_Discord.command()
        async def ping(ctx):
            await ctx.send("Pong!")

        Discord_tokenreplace = self.Discord_token.replace(" ", "")
        print(self.TelegramTOKEN)
        print(self.CHANNEL_ID)
        print(Discord_tokenreplace)
        print(self.Discord_token)
        print(f"{Discord_tokenreplace}")
        
        self.client_Discord.run(self.Discord_token)  # Discord



Discordclass = Discord()
print("Alfred Discord Status: On")
Discordclass.main_discord()
