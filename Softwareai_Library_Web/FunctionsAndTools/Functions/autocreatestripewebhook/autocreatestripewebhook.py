#!/usr/bin/env python3
"""
Script para criar um Webhook Endpoint no Stripe.
Configura a URL do webhook e os eventos habilitados.
"""
import os
import sys
import argparse
import stripe
import logging
from stripe.error import StripeError
from typing_extensions import TypedDict
from agents import function_tool

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class Data(TypedDict):
    url: str
    events: str
    STRIPE_SECRET_KEY: str

@function_tool
def autostripecreatewebhook(data: Data):
    try:
        data_FINAL = data["data"]
        events = data_FINAL["events"].split()
        url = data_FINAL["url"]
        STRIPE_SECRET_KEY = data_FINAL["STRIPE_SECRET_KEY"]
    except Exception as e:
        logger.warning(f"Erro ao acessar 'data': {e}")
        events = data["events"].split()
        url = data["url"]
        STRIPE_SECRET_KEY = data["STRIPE_SECRET_KEY"]
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        # Cria o Webhook Endpoint usando a URL e eventos informados
        webhook = stripe.WebhookEndpoint.create(
            url=url,
            enabled_events=events
        )
        logger.info("✅ Webhook criado com sucesso!")
        logger.info(f"ID: {webhook.id}")
        
        # Exibe o segredo da assinatura do webhook
        if hasattr(webhook, 'secret') and webhook.secret:
            logger.info(f"🔑 Segredo da Assinatura do Webhook: {webhook.secret}")
            return {
                "webhook_id": webhook.id, 
                "webhook_secret": webhook.secret,
            }
        else:
            logger.warning("⚠️ Nenhum segredo retornado. Verifique suas permissões ou a documentação da Stripe.")
    except StripeError as e:
        msg = e.user_message or str(e)
        logger.error(f"❌ Falha ao criar webhook: {msg}")
        return {"erro": f"❌ Falha ao criar webhook: {msg}"}
    except Exception as e:
        logger.exception("❌ Erro inesperado:")
        return {"erro": f"❌ Erro inesperado: {e}"}
