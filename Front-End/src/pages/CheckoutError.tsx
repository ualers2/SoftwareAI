// src/components/CheckoutError.tsx
import React from "react";
import { Link } from "react-router-dom";

export default function CheckoutError(): JSX.Element {
  return (
    <div className="max-w-md mx-auto mt-20 bg-white rounded-2xl shadow-md p-6 text-center">
      <h2 className="text-3xl font-bold mb-4 text-red-600">Ocorreu um erro no pagamento</h2>
      <p className="text-gray-700 mb-6">
        Não foi possível processar sua assinatura. Por favor, tente novamente ou contate nosso suporte.
      </p>
      <Link
        to="/checkout"
        className="inline-block px-6 py-3 rounded-xl bg-gradient-to-r from-gray-700 to-gray-500 text-white font-semibold hover:from-gray-800 hover:to-gray-600 transition"
      >
        Voltar ao Checkout
      </Link>
    </div>
  );
}
