#!/usr/bin/env python3
"""
Script para criar um Webhook Endpoint no Stripe.
Configura a URL do webhook e os eventos habilitados.
"""
import os
import sys
import argparse
import stripe
from stripe.error import StripeError
from typing_extensions import TypedDict
from agents import function_tool

class Data(TypedDict):
    nome: str
    valor: str
    moeda: str
    intervalo: str
    STRIPE_SECRET_KEY: str

@function_tool
def autocreatestripeproduction(data: Data):
    try:
        data_FINAL = data["data"]
        nome = data_FINAL["nome"]
        valor = data_FINAL["valor"]
        moeda = data_FINAL["moeda"]
        intervalo = data_FINAL["intervalo"]
        STRIPE_SECRET_KEY = data_FINAL["STRIPE_SECRET_KEY"]
    except Exception as e:
        print(e)
        nome = data["nome"]
        valor = data["valor"]
        moeda = data["moeda"]
        intervalo = data["intervalo"]
        STRIPE_SECRET_KEY = data["STRIPE_SECRET_KEY"]
    # Converte o valor para centavos/integer
    try:
        valor_centavos = int(float(valor) * 100)
    except ValueError:
        print("Erro: valor inválido. Informe um número, por exemplo 19.99")
        sys.exit(1)

    try:
        stripe.api_key = STRIPE_SECRET_KEY
        # Cria o produto na Stripe
        product = stripe.Product.create(
            name=nome,
        )
        print(f"✅ Produto criado: {product.name} (ID: {product.id})")

        # Cria o preço (Price) recorrente associado ao produto
        price = stripe.Price.create(
            unit_amount=valor_centavos,
            currency=moeda.lower(),
            recurring={"interval": intervalo},
            product=product.id
        )
        print(f"✅ Preço de assinatura criado com sucesso!")
        print(f"ID do Price: {price.id}")
        data_return = {
            "product_name": product.name, 
            "product_id": product.id, 
            "price_id": price.id,
        }
        return data_return
    except StripeError as e:
        msg = e.user_message or str(e)
        print(f"\n❌ Falha ao criar produto/preço: {msg}")
        data_return = {
            "erro": f"❌ Falha ao criar produto/preço: {msg}", 
        }
        return data_return
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        data_return = {
            "erro": f"❌ Erro inesperado: {e}", 
        }
        return data_return




