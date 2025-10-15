from Agents.TecnicalDoc.ai import TecnicalDoc
import asyncio

from api import app

TecnicalDoc_instance = TecnicalDoc()
TecnicalDoc_Runner = TecnicalDoc_instance.run

mensagem = """
Não consigo acessar mais de 10 vídeos anteriores no modo de seleção de vídeo específico por nome do canal. Ao tentar navegar pelo histórico, parece limitar o acesso aos primeiros 10 vídeos e não carrega os demais.
"""
user_platform_id = "teste@gmail.com"
conversation_id = "chatsession_1235"
ticket_id = 'f99ea'
asyncio.run(TecnicalDoc_Runner(mensagem, user_platform_id, conversation_id, ticket_id))
            